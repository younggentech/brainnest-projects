# -*- coding: utf-8 -*-
from pathlib import Path
from configparser import ConfigParser
from requests import post
from weather_api import data_parser
from flask import Flask, render_template, request

app = Flask(__name__)
config = ConfigParser()
path_to_config = Path("config.ini")  # Reason file bug
config.read(f"{path_to_config}")
apiKey = config["weatherAPI"]["apiKey"]
apiURL = config["weatherAPI"]["apiURL"]
POST = "POST"
GET = "GET"


def get_error_message(error: dict):
    """this dictionary is for error message based on the error code from the api
    :param error: a dictionary which will hold error description.
    """
    error_messages = {
        1003: "Enter City name.",
        1006: "No City matched the given name.",
        2008: "API key has been disabled.",
    }
    return error_messages[int(error.get("code"))]


@app.route("/", methods=[POST, GET])
def index():
    if request.method == GET:
        return render_template("index.html", result={})
    elif request.method == POST:
        if not apiKey:
            result = dict(error_message="No API key is provided.")
            return render_template("index.html", result=result)
        city = request.form.to_dict().pop("city")
        result = post(f"{apiURL}?key={apiKey}&q={city}")
        if result.status_code == 200:
            result = result.json()
            result = data_parser(result)
            return render_template("index.html", result=result)
        else:
            result = dict(error_message=get_error_message(result.json().get("error")))
            return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
