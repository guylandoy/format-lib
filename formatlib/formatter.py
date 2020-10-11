import json
from benedict import benedict
from formatlib.utilities.standardize import standardize
from formatlib.utils import *
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class Formatter:
    def __init__(self, data):
        if type(data) == str:
            try:
                self.data = benedict(json.loads(data))
                logging.info("Successfully loaded json file")
            except json.JSONDecodeError:
                raise Exception("The data is not a valid json object")
        else:
            try:
                self.data = benedict(json.load(data))
                logging.info("Successfully loaded json file")
            except json.JSONDecodeError:
                raise Exception("The data is not a valid json object")

    # Convert keys to timestamp UTC tz.
    def convert_dates(self, key_names, input_formats):
        if type(key_names) != list or type(input_formats) != list \
                or len(key_names) != len(input_formats) or len(key_names) <= 0:
            raise Exception("key names and formats are not correct")
        # Update every key in json to the result of the date_formatter.
        for x in range(len(key_names)):
            self.data = self.convert_date(key_names[x], input_formats[x])
        logging.info("Successfully converted dates")
        return self.data

    # Convert Date data in key_name with format of 'input_format' to timestamp UTC timezone.
    def convert_date(self, key_name, input_format):
        formatted_result = date_to_timestamp(self.get_key_data(key_name), input_format)
        self.save_formatted_result(key_name, formatted_result)
        logging.info("Successfully converted date")
        return self.data

    # Convert UTM data in key_name to WGS84 Latitude/Longitude.
    def convert_utm(self, key_name):
        key_data = self.get_key_data(key_name)
        utm_data = find_coordinates(key_data, update_coordinate_utm)
        if check_none(utm_data):
            logging.info("Coordinates not found")
            return self.data
        formatted_result = utm_to_wgs84(utm_data[0], utm_data[1])
        self.save_formatted_result(key_name, formatted_result)
        logging.info("Successfully converted UTM to WGS84")
        return self.data

    # Convert WGS data in key_name to WGS84 Latitude/Longitude.
    def convert_wgs(self, key_name):
        key_data = self.get_key_data(key_name)
        wgs_data = find_coordinates(key_data, update_coordinate_wgs)
        if check_none(wgs_data):
            logging.info("Coordinates not found")
            return self.data
        formatted_result = get_lat_lon_object_from_tuple(wgs_data)
        self.save_formatted_result(key_name, formatted_result)
        logging.info("Successfully converted WGS84 to UTM")
        return self.data

    # Return the data.
    def get_data(self):
        return self.data

    # Set new data
    def set_data(self, new_data):
        if type(new_data) == str:
            self.data = benedict(json.loads(new_data))
        else:
            self.data = benedict(json.load(new_data))
        return self.data

    # Save formatted result in a new key.
    def save_formatted_result(self, key_name, formatted_result):
        new_key_name = key_name + '_formatted'
        self.data[new_key_name] = formatted_result

    # Get the data of key given. key is a string and can be nested with '.' . example: 'geometry.coordinates'
    def get_key_data(self, key_string):
        return self.data[key_string]

    # Flatten data - Arrays not being flattened.
    def flatten(self):
        self.data = self.data.flatten()
        logging.info("Successfully flattened data")
        return self.data

    # Change key names to be lower case and underscore between words.
    def standardize(self):
        standardize(self.data)
        logging.info("Successfully standardized data")
        return self.data

    # Flatten data including arrays
    def flatten_json(self):
        sep = '_'
        out = dict()

        def flatten(the_obj: (list, dict, str), name: str=''):
            if isinstance(the_obj, dict):
                for nested in the_obj:
                    flatten(the_obj[nested], f'{name}{nested}{sep}')
            elif isinstance(the_obj, list):
                counter = 0
                for nested in the_obj:
                    flatten(nested, f'{name}{counter}{sep}')
                    counter += 1
            else:
                out[name[:-1]] = the_obj

        flatten(self.data)
        self.data = out
        logging.info("Successfully flattened json")
        return self.data
