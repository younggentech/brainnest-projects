# -*- coding: utf-8 -*-
""" This module was created to deal with response data from weather API

"""
from typing import NamedTuple
from pathlib import Path
import pandas as pd
import matplotlib as plt
import requests
from requests import Response


# Creates file structure for saving weather related figures and icons
FileStructure = NamedTuple(
    "FileStructure", [
        ("abs_path_to_parent_dir", str),
        ("abs_path_to_subdir_icons", str),
        ("abs_path_to_subdir_figs", str)
    ]
)

data_path_files= FileStructure("./data", "./data/icons",
                               "./data/figs")


def create_data_file_structure(abs_path_obj: FileStructure) -> str:
    """

    :param abs_path_obj:
    :return:
    """
    if not all(abs_path_obj._fields):
        raise ValueError("All fields in NamedTuple needs to be populated ")
    parent_dir = Path(abs_path_obj.abs_path_to_parent_dir)
    sub_icon = Path(abs_path_obj.abs_path_to_subdir_icons)
    sub_figs = Path(abs_path_obj.abs_path_to_subdir_figs)
    print(sub_figs.cwd())
    try:
        parent_dir.mkdir(parents=True)
        sub_figs.mkdir(parents=False)
        sub_icon.mkdir(parents=False)
    except FileExistsError as e:
        print("Structure exists at:", e)
    except FileNotFoundError as e:
        print("Directory is missing",e)
    else:
        return "Structure created"








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


def weather_stats(weather_data: dict)-> pd.Series:
    s_weather_data = pd.Series(weather_data)
    index_selector = [
        "lat", "lon", "localtime", "temp_f", "feelslike_c" ,"is_day",
        "wind_kph", "pressure_mb", "wind_degree", "wind_dir",
        "precip_mm", "humidity", "cloud"
    ]
    weather_data_stats = s_weather_data[index_selector]
    return weather_data_stats



def get_icon(weather_data: dict) -> None:
    try:
        url_link = weather_data.get("icon", None)
        if not url_link:
            raise(ValueError("No link to icon missing!"))

        img_data = requests.request("GET", url=url_link, stream=True)
        img_data.raise_for_status()
    except ValueError as error0:
        print("Link not found: ", error0)
    except requests.exceptions.Timeout as error1:
        print("Icon not found:,", error1)
    except requests.exceptions.ConnectionError as error2:
        print("Icon could not be download connection issues: ", error2)
    except requests.exceptions.InvalidURL as error3:
        print("Icon link broken:", error3)
    else:
        name_file = f"{weather_data['text']}.png"
        img_file = Path(data_path_files.abs_path_to_subdir_icons) / name_file
        with img_file.open(mode="wb") as img_f:
            img_f.write(img_data.content)
        return img_file


def create_weather_figures(weather_stat: pd.Series)-> str:
    pass






# Testing purposes
#if __name__ == "__main__":
#    response_obj = {'location': {'name': 'New York', 'region': 'New York', 'country': 'United States of America', 'lat': 40.71, 'lon': -74.01, 'tz_id': 'America/New_York', 'localtime_epoch': 1674909586, 'localtime': '2023-01-28 7:39'}, 'current': {'last_updated_epoch': 1674909000, 'last_updated': '2023-01-28 07:30', 'temp_c': 1.1, 'temp_f': 34.0, 'is_day': 1, 'condition': {'text': 'Overcast', 'icon': '//cdn.weatherapi.com/weather/64x64/day/122.png', 'code': 1009}, 'wind_mph': 9.4, 'wind_kph': 15.1, 'wind_degree': 200, 'wind_dir': 'SSW', 'pressure_mb': 1022.0, 'pressure_in': 30.18, 'precip_mm': 0.0, 'precip_in': 0.0, 'humidity': 67, 'cloud': 100, 'feelslike_c': -3.8, 'feelslike_f': 25.1, 'vis_km': 16.0, 'vis_miles': 9.0, 'uv': 1.0, 'gust_mph': 17.7, 'gust_kph': 28.4}}
#    data_w = get_weather_data(response_obj)
#    data_stats = weather_stats(data_w)
#    file_icon = get_icon(data_w)
#    #create_data_file_structure(data_path_files)
