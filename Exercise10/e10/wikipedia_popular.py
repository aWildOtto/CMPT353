import sys
from pyspark.sql import SparkSession, functions, types
import re

spark = SparkSession.builder.appName('wikipedia popular').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

wiki_schema = types.StructType([
    types.StructField('lang', types.StringType()),
    types.StructField('title', types.StringType()),
    types.StructField('views', types.LongType()),
    types.StructField('bytes', types.LongType()),
])

def search_date(path):
	date = re.search('[0-9]{8}\-[0-9]{2}', path)
	return date.group(0)

def main(in_directory, out_directory):
	data = spark.read.csv(in_directory, schema=wiki_schema, sep=' ').withColumn('filename', functions.input_file_name())
	#data.show()

	data = data.filter(data['lang'] == 'en')
	data = data.filter(data['title'] != 'Main_Page')
	data = data.filter(data.title.startswith('Special:') != True)
	#data.show()

	path_to_hour = functions.udf(lambda path: search_date(path), returnType=types.StringType())
	data = data.withColumn('time', path_to_hour(data.filename))
	data = data.cache()
	#data.show()

	groups = data.groupBy('time')
	max_views = groups.agg(functions.max(data['views']).alias('views'))
	#max_views.show()

	data_join = max_views.join(data, on=['views','time'])
	#data_join.show()


	output = data_join.drop('lang', 'bytes', 'filename')
	output = output.select('time', 'title', 'views')
	#output.show()

	output = output.sort('time','title')
	#output.show()

	output.write.csv(out_directory + '-wikipedia', mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
