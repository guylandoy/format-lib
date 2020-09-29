import json
from .utils import *
from benedict import benedict


class Formatter:
    def __init__(self, data):
        if type(data) == str:
            self.data = benedict(json.loads(data))
        else:
            self.data = benedict(json.load(data))

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
        formatted_result = date_to_timestamp(self.get_key_data(key_name), input_format)
        self.save_formatted(key_name, formatted_result)
        return self.data

    def convert_utm(self, key_name):
        key_data = self.get_key_data(key_name)
        utm_data = parser(key_data, update_utm)
        if check_none(utm_data):
            return self.data
        formatted_result = utm_to_wgs84(utm_data[0], utm_data[1])
        self.save_formatted(key_name, formatted_result)
        return self.data

    def convert_wgs(self, key_name):
        key_data = self.get_key_data(key_name)
        wgs_data = parser(key_data, update_wgs)
        if check_none(wgs_data):
            return self.data
        formatted_result = get_lat_lon_object_from_tuple(wgs_data)
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

    # Get the data of key given. key is a string and can be nested with '.' . example: 'geometry.coordinates'
    def get_key_data(self, key_string):
        return self.data[key_string]

    def flatten_json(self):
        sep = '_'
        out = dict()
        def flatten(the_obj: (list, dict, str), name: str=''):
            if type(the_obj) is dict:
                for nested in the_obj:
                    flatten(the_obj[nested], f'{name}{nested}{sep}')
            elif type(the_obj) is list:
                counter = 0
                for nested in the_obj:
                    flatten(nested, f'{name}{counter}{sep}')
                    counter += 1
            else:
                out[name[:-1]] = the_obj

        flatten(self)
        return out
