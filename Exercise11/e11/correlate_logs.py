import sys
from pyspark.sql import SparkSession, functions, types, Row
import re
from pprint import pprint
import math

spark = SparkSession.builder.appName('correlate logs').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

line_re = re.compile(r"^(\S+) - - \[\S+ [+-]\d+\] \"[A-Z]+ \S+ HTTP/\d\.\d\" \d+ (\d+)$")


def line_to_row(line):
    """
    Take a logfile line and return a Row object with hostname and bytes transferred. Return None if regex doesn't match.
    """
    m = line_re.match(line)
    if m:
        # TODO
        hostName = m.group(1)
        numBytes = m.group(2)
        return Row(hostname = hostName, numbytes = numBytes)


    else:
        return None


def not_none(row):
    """
    Is this None? Hint: .filter() with it.
    """
    return row is not None


def create_row_rdd(in_directory):
    log_lines = spark.sparkContext.textFile(in_directory)
    # TODO: return an RDD of Row() objects
    rows = log_lines.map(line_to_row)
    rows = rows.filter(not_none)
    return rows


def main(in_directory):
    logs = spark.createDataFrame(create_row_rdd(in_directory))
    #logs.show()

    # TODO: calculate r.
    count_requests = logs.groupby('hostname').agg(functions.count('hostname').alias("countRequests"))
    #count_requests.show()
    sum_requests_bytes = logs.groupby('hostname').agg(functions.sum('numbytes').alias("sumRequestsBytes"))
    #sum_requests_bytes.show()
    calc_logs = count_requests.join(sum_requests_bytes, 'hostname')
    #calc_logs.show()

    # Produce 1, x, x^2, y, y^2, xy
    calc_logs = calc_logs.select(
        calc_logs['countRequests'].alias("x"),
        (calc_logs['countRequests']*calc_logs['countRequests']).alias("x^2"),
        calc_logs['sumRequestsBytes'].alias("y"),
        (calc_logs['sumRequestsBytes']*calc_logs['sumRequestsBytes']).alias("y^2"),
        (calc_logs['countRequests']*calc_logs['sumRequestsBytes']).alias("xy"))
    #calc_logs.show()

    x_sum = calc_logs.agg(functions.sum('x')).first()[0]
    x2_sum = calc_logs.agg(functions.sum('x^2')).first()[0]
    y_sum = calc_logs.agg(functions.sum('y')).first()[0]
    y2_sum = calc_logs.agg(functions.sum('y^2')).first()[0]
    xy_sum = calc_logs.agg(functions.sum('xy')).first()[0]
    n = calc_logs.count()
    #print(n)

    r1 = (n * xy_sum) - (x_sum * y_sum)
    r2 = (math.sqrt((n * x2_sum) - (x_sum)**2)) * (math.sqrt((n * y2_sum) - (y_sum)**2))

    r = r1/r2 # TODO: it isn't zero.
    print("r = %g\nr^2 = %g" % (r, r**2))


if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)
