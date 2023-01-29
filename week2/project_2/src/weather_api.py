# -*- coding: utf-8 -*-
""" This module was created to deal with response data from weather API

"""
from requests import Response


def get_weather_data(response_obj: Response) -> dict:
    """

    :param response_obj:
    :return:
    """
    # Generator to save some memory
    url_link_stem = "https:"
    data = (k_i for k_p in response_obj for k_i in response_obj[k_p].items())
    data_w = dict(data)
    find_nested_dict = (k for k, v in data_w.items() if isinstance(v, dict))
    new_dict = data_w.pop("".join(find_nested_dict))
    data_w.update(new_dict)
    fix_link = f"{url_link_stem}{data_w.get('icon')}"
    data_w["icon"] = fix_link
    return data_w
