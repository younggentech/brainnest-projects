# -*- coding: utf-8 -*-
"""
Model module to parse data
"""
from datetime import timedelta


def validate_form(func) -> tuple:
    """
    Attempts to validate received inputs.
    """

    def parse_form(*args, **kwargs):
        values = func(*args, **kwargs)

        try:
            parsed_values = [int(v) for v in values.values()]
        except (ValueError, TypeError, AttributeError) as error:
            print(f"Input error {error}")
            return False
        else:
            return tuple(parsed_values)

    return parse_form


def timer_converter(func):
    """Converts input to seconds expected HH:MM:SS"""

    def time_parser(*args, **kwargs):
        time_tuple = func(*args, **kwargs)
        if not time_tuple:
            return time_tuple
        hours, minutes, secs = time_tuple
        total_time = (hours * 3600) + (minutes * 60) + secs
        while total_time >= 0:
            new_time = timedelta(seconds=total_time)
            total_time -= 1
            yield str(new_time)

    return time_parser


@timer_converter
@validate_form
def get_time(f_rsp: dict):
    """Returns either None or generator object that can
    be converted to list
    """
    return f_rsp
