from datetime import datetime, timezone


def date_to_timestamp(date, input_format):
    return datetime.strptime(date, input_format).replace(tzinfo=timezone.utc).timestamp()
