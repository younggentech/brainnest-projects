# -*- coding: utf-8 -*-
""" This module was created to deal with response data from weather API

"""
from requests import Response


def get_weather_data(response_obj: Response) -> list:
    """

    :param response_obj:
    :return:
    """
    weather_data = [
        "name",
        "country",
        "localtime",
        "temp_c",
        "feelslike_c",
        "humidity",
        "condition",
    ]
    results = []
    for key in response_obj:
        for item in weather_data:
            results.append(response_obj[key].get(item, None))

    return (item for item in results if item)
