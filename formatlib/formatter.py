import json
from .utils import *


class Formatter:
    def __init__(self, data):
        self.data = json.loads(data)

    # Convert columns to timestamp UTC tz.
    def convert_dates(self, column_names, input_formats):
        if type(column_names) != list or type(input_formats) != list \
                or len(column_names) != len(input_formats) or len(column_names) <= 0:
            raise Exception("column names and formats are not correct")
        # Update every column in json to the result of the date_formatter.
        for x in range(len(column_names)):
            self.data = self.convert_date(column_names[x], input_formats[x])
        return self.data

    # Convert a column to timestamp UTC tz.
    def convert_date(self, column_name, input_format):
        formatted_result = date_to_timestamp(self.data[column_name], input_format)
        self.data[column_name] = formatted_result
        return self.data

    def get_data(self):
        return self.data

    def set_data(self, new_data):
        self.data = new_data
        return self.data






