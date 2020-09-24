from datetime import datetime, timezone
import utm
from pyproj import Proj, transform, CRS

wgs84 = CRS("EPSG:4326")  # LatLon with WGS84 datum used by GPS unit
UTM36N = CRS("EPSG:32636")


# Convert tuple of (latitude, longitude) to object
def get_lat_lon_object_from_tuple(lat_lon_tuple):
    return {'latitude': lat_lon_tuple[0], 'longitude': lat_lon_tuple[1]}


# convert Date to timestamp of UTC timezone according to format given (format of datetime.strptime)
def date_to_timestamp(date, input_format):
    return datetime.strptime(date, input_format).replace(tzinfo=timezone.utc).timestamp()


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


# Convert utm easting and northing using pyproj.transform from UTM Zone 36N, to WGS84 latitude and longitude.
def utm_to_wgs84(easting, northing):
    return get_lat_lon_object_from_tuple(transform(UTM36N, wgs84, easting, northing))

