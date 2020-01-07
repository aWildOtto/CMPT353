import sys
import pandas as pd
import numpy as np
from xml.dom.minidom import parse, parseString
from pykalman import KalmanFilter

def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')

def get_data(data_filename):
    data = parse(data_filename)
    parse_result = data.getElementsByTagName("trkpt")
    points_df = pd.DataFrame(columns=['lat', 'lon'])

    for element in parse_result:
        lat = element.getAttribute('lat')
        lon = element.getAttribute('lon')
        points_df = points_df.append(pd.DataFrame({"lat":[lat], "lon":[lon]}), ignore_index = True)

    #print(points_df)

    return points_df

# Helper function for distance, function mimics haversine formula
def haversine(lat1, lon1, lat2, lon2):
    a = np.sin((np.deg2rad(lat2-lat1))/2)*np.sin((np.deg2rad(lat2-lat1))/2)
    b = np.cos(np.deg2rad(lat1))*np.cos(np.deg2rad(lat2))
    c = np.sin((np.deg2rad(lon2-lon1))/2)*np.sin((np.deg2rad(lon2-lon1))/2)
    return 12742*np.arcsin(np.sqrt(a+b*c))*1000

def distance(data):
    points = pd.DataFrame()
    points["lat"] = data["lat"]
    points["lon"] = data["lon"]
    points["lat2"] = points["lat"].shift(1)
    points["lon2"] = points["lon"].shift(1)

    points["lat"]= points["lat"].astype(float)
    points["lon"]= points["lon"].astype(float)
    points["lat2"]= points["lat2"].astype(float)
    points["lon2"]= points["lon2"].astype(float)

    points["distance"] = points.apply(lambda row: haversine(row['lat'], row['lon'], row['lat2'], row['lon2']), axis = 1)
    total_distance = points["distance"].sum()

    #print(points)
    return total_distance

def smooth(points):

    initial_state = points.iloc[0]
    observation_covariance = np.diag([0.9, 0.9]) ** 2
    transition_covariance = np.diag([0.6, 0.6]) ** 2
    transition = [[1, 0], [0, 1]]

    kf = KalmanFilter(
    initial_state_mean=initial_state,
    initial_state_covariance=observation_covariance,
    observation_covariance=observation_covariance,
    transition_covariance=transition_covariance,
    transition_matrices=transition
    )

    smooth_points = points
    smooth_points["lat"]= smooth_points["lat"].astype(float)
    smooth_points["lon"]= smooth_points["lon"].astype(float)

    smooth_points2, _ = kf.smooth(smooth_points)
    smooth_df = pd.DataFrame(smooth_points2)
    smooth_df = smooth_df.rename(columns={0: "lat", 1: "lon"})

    return smooth_df

def main():
    points = get_data(sys.argv[1])
    print('Unfiltered distance: %0.2f' % (distance(points)))
    
    smoothed_points = smooth(points)
    print('Filtered distance: %0.2f' % (distance(smoothed_points)))
    output_gpx(smoothed_points, 'out.gpx')

    #points = pd.DataFrame({'lat': [49.28, 49.26, 49.26], 'lon': [123.00, 123.10, 123.05]})
    #print(distance(points))

if __name__ == '__main__':
    main()