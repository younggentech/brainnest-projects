# -*- coding: utf-8 -*-
""" This module was created to deal with response data from weather API

"""
from typing import NamedTuple
from pathlib import Path
import pandas as pd
from requests import exceptions as ReqExcept
from requests import Response, request


# Creates file structure for saving weather related figures and icons
FileStructure = NamedTuple(
    "FileStructure",
    [
        ("abs_path_to_parent_dir", str),
        ("abs_path_to_subdir_icons", str),
        ("abs_path_to_subdir_figs", str),
    ],
)

data_path_files = FileStructure("./data", "./data/icons", "./data/figs")


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
        print("Directory is missing", e)
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


def weather_stats(weather_data: dict) -> pd.Series:
    s_weather_data = pd.Series(weather_data)
    index_selector = [
        "lat",
        "lon",
        "localtime",
        "feelslike_c",
        "wind_kph",
        "pressure_mb",
        "wind_degree",
        "wind_dir",
        "precip_mm",
        "humidity",
        "cloud",
        "name",
        "country",
        "icon",
        "text"
    ]
    weather_data_stats = s_weather_data[index_selector]
    return weather_data_stats.to_dict()


def get_icon(weather_data: dict) -> None:
    try:
        url_link = weather_data.get("icon", None)
        if not url_link:
            raise (ValueError("No link to icon missing!"))

        img_data = request("GET", url=url_link, stream=True)
        img_data.raise_for_status()
    except ValueError as error0:
        print("Link not found: ", error0)
    except ReqExcept.Timeout as error1:
        print("Icon not found:,", error1)
    except ReqExcept.ConnectionError as error2:
        print("Icon could not be download connection issues: ", error2)
    except ReqExcept.InvalidURL as error3:
        print("Icon link broken:", error3)
    else:
        name_file = f"{weather_data['text']}.png"
        img_file = Path(data_path_files.abs_path_to_subdir_icons) / name_file
        with img_file.open(mode="wb") as img_f:
            img_f.write(img_data.content)
        return img_file


def create_weather_figures(weather_stat: dict) -> None:
    # TODO: Place holder function intended for future endeavours
    pass


def data_parser(response_obj: Response):
    all_weather_data = get_weather_data(response_obj)
    data_stats = weather_stats(all_weather_data)
    return data_stats
