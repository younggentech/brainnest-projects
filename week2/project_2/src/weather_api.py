# -*- coding: utf-8 -*-
""" This module was created to deal with response data from weather API

"""
from typing import Generator
from requests import Response


def get_weather_data(response_obj: Response, weather_data: list = None) -> Generator:
    """

    :param response_obj:
    :return:
    """
    if not weather_data:
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
    get_dict_item = [item for item in results if isinstance(item, dict)]
    rm_dict = (value for _, value in get_dict_item[0].items())
    results.extend(list(rm_dict))
    return (item for item in results if not isinstance(item, dict) and item)
