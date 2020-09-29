import json
from .utils import *


class Formatter:
    def __init__(self, data):
        if type(data) == str:
            self.data = json.loads(data)
        else:
            self.data = json.load(data)

    # Convert keys to timestamp UTC tz.
    def convert_dates(self, key_names, input_formats):
        if type(key_names) != list or type(input_formats) != list \
                or len(key_names) != len(input_formats) or len(key_names) <= 0:
            raise Exception("key names and formats are not correct")
        # Update every key in json to the result of the date_formatter.
        for x in range(len(key_names)):
            self.data = self.convert_date(key_names[x], input_formats[x])
        return self.data

    # Convert a key to timestamp UTC tz.
    def convert_date(self, key_name, input_format):
        formatted_result = date_to_timestamp(self.data[key_name], input_format)
        self.save_formatted(key_name, formatted_result)
        return self.data

    def convert_utm(self, key_name):
        key_data = self.data[key_name]
        utm_data = utm_parser(key_data)
        formatted_result = utm_to_wgs84(utm_data[0], utm_data[1])
        self.save_formatted(key_name, formatted_result)
        return self.data

    def get_data(self):
        return self.data

    def set_data(self, new_data):
        self.data = new_data
        return self.data

    def save_formatted(self, key_name, formatted_result):
        new_key_name = key_name + '_formatted'
        self.data[new_key_name] = formatted_result





