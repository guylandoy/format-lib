from datetime import datetime, timezone
import utm
from pyproj import Proj, CRS, Transformer
import math

wgs84 = CRS("EPSG:4326")  # LatLon with WGS84 datum used by GPS unit
UTM36N = CRS("EPSG:32636")
utm_transformer = Transformer.from_crs(UTM36N, wgs84)


# Convert tuple of (latitude, longitude) to object
def get_lat_lon_object_from_tuple(lat_lon_tuple):
    return {'latitude': round_half_up(lat_lon_tuple[0], 6), 'longitude': round_half_up(lat_lon_tuple[1], 6)}


# convert Date to timestamp of UTC timezone according to format given (format of datetime.strptime)
def date_to_timestamp(date, input_format):
    return int(datetime.strptime(date, input_format).replace(tzinfo=timezone.utc).timestamp())


# Convert utm easting and northing coordinates to Latitude and Longitude using utm package.
def utm_to_lat_long(easting, northing):
    lat_lon = utm.to_latlon(easting, northing, 36, 'N')
    return get_lat_lon_object_from_tuple(lat_lon)


# Use pyproj.Proj to get latitude and longitude
# based on given projection (proj) and ellipsoid (ellps) with 2 coordinates
def coordinates_proj(proj, ellps, coordinate1, coordinate2):
    if proj == 'utm':
        p = Proj(proj='utm', zone=36, ellps=ellps, preserve_units=False)
        (lng, lat) = p(coordinate1, coordinate2, inverse=True)
        return get_lat_lon_object_from_tuple((lat, lng))


# Convert utm easting and northing using pyproj.Transformer from UTM Zone 36N, to WGS84 latitude and longitude.
def utm_to_wgs84(easting, northing):
    return get_lat_lon_object_from_tuple(utm_transformer.transform(easting, northing))


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier


# Gets UTM location data and returns [easting, northing]
def utm_parser(data):
    result = [None, None]
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, int) or isinstance(value, float):
                result = update_utm(result, value)
            elif isinstance(value, str):
                value = float(value)
                result = update_utm(result, value)

    elif isinstance(data, list):
        for value in data:
            if isinstance(value, int) or isinstance(value, float):
                result = update_utm(result, value)
            elif isinstance(value, str):
                value = float(value)
                result = update_utm(result, value)
    return result


# check number of digits before decimal point. if its 6 digits long it is probably northing.
# if it is 6 digits long, it is probably easting.
def update_utm(arr, value):
    if len(str(int(value))) == 7:
        arr[1] = float(value)
    elif len(str(int(value))) == 6:
        arr[0] = float(value)
    return arr




