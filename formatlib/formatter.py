import json
from .utils import *


class Formatter:
    def __init__(self, data):
        self.data = json.loads(data)

    def convert_dates(self, column_names, input_formats):
        if len(column_names) != len(input_formats):
            raise Exception("column names and formats doesn't match")
        # Update every column in json to the result of the date_formatter.
        for x in range(len(column_names)):
            self.data = self.convert_date(column_names[x], input_formats[x])
            # json_data[column_names[x]] = date_formatter(column_names[x], input_formats[x])
        return self.data

    def convert_date(self, column_name, input_format):
        formatted_result = date_to_timestamp(self.data[column_name], input_format)
        self.data[column_name] = formatted_result
        return self.data

    def get_data(self):
        return self.data

    def set_data(self, new_data):
        self.data = new_data
        return self.data






