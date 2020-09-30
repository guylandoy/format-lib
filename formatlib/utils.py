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


# Convert Date to timestamp of UTC timezone according to format given (format of datetime.strptime)
def date_to_timestamp(date, input_format):
    return int(datetime.strptime(date, input_format).replace(tzinfo=timezone.utc).timestamp())


# Convert utm easting and northing coordinates to Latitude and Longitude using utm package.
# def utm_to_lat_long(easting, northing):
#     lat_lon = utm.to_latlon(easting, northing, 36, 'N')
#     return get_lat_lon_object_from_tuple(lat_lon)


# Use pyproj.Proj to get latitude and longitude
# based on given projection (proj) and ellipsoid (ellps) with 2 coordinates
# def coordinates_proj(proj, ellps, coordinate1, coordinate2):
#     if proj == 'utm':
#         p = Proj(proj='utm', zone=36, ellps=ellps, preserve_units=False)
#         (lng, lat) = p(coordinate1, coordinate2, inverse=True)
#         return get_lat_lon_object_from_tuple((lat, lng))


# Convert utm easting and northing using pyproj.Transformer from UTM Zone 36N, to WGS84 latitude and longitude.
def utm_to_wgs84(easting, northing):
    return get_lat_lon_object_from_tuple(utm_transformer.transform(easting, northing))


# Round number up if higher than half ('decimals' digits after decimal point).
def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier


# UTM Coordinate checker. Figure out if value is easting (index 0) or northing (index 1)
def update_coordinate_utm(arr, value):
    try:
        first_six = len(str(int(arr[0]))) == 6
    except Exception:
        first_six = False

    if len(str(int(value))) == 7:
        arr[1] = float(value)
    elif len(str(int(value))) == 6 and not first_six:
        arr[0] = float(value)
    elif len(str(int(value))) == 6 and first_six:
        if arr[0] > value:
            arr[1] = 3000000 + value
            return arr
        return [arr[1], 3000000 + arr[0]]
    return arr


# WGS Coordinate checker. Figure out if value is latitude or longitude.
# Latitude is between 29 and 33 (index 0). Longitude is 34 or 35 (index 1).
def update_coordinate_wgs(arr, value):
    if 34 <= int(value) <= 35:
        arr[1] = value
    elif 29 <= int(value) < 34:
        arr[0] = value
    return arr


# Find relevant coordinates needed for formatting location.
def find_coordinates(data, update_coordinate):
    try:
        result = [None, None]
        if isinstance(data, dict):
            data = list(data.values())

        if isinstance(data, list):
            for value in data:
                if isinstance(value, str):
                    value = float(value)
                if isinstance(value, int) or isinstance(value, float):
                    result = update_coordinate(result, value)
        return result
    except Exception as e:
        print("Error parsing", e)
        return [None, None]


# Check if coordinates not found.
def check_none(data):
    if data is None:
        return True
    elif isinstance(data, list) and len(data) != 2:
        return True
    elif data[0] is None or data[1] is None:
        return True
    else:
        return False

