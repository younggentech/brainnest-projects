# -*- coding: utf-8 -*-
import json
from pathlib import Path
from configparser import ConfigParser
from requests import post
from weather_api import get_weather_data
from flask import Flask, render_template, request

app = Flask(__name__)
config = ConfigParser()
path_to_config = Path("config.ini")  # Reason file bug
config.read(f"{path_to_config}")
apiKey = config["weatherAPI"]["apiKey"]
apiURL = config["weatherAPI"]["apiURL"]
POST = "POST"
GET = "GET"


@app.route("/", methods=[POST, GET])
def index():
    if request.method == GET:
        return render_template("index.html", result={})
    elif request.method == POST:
        city = request.form.to_dict().pop("city")
        result = post(f"{apiURL}?key={apiKey}&q={city}")
        if result.status_code == 200:
            result = result.json()
            result = get_weather_data(result)
            return render_template("index.html", result=result)
        else:
            # TODO: Error if API-key is missing -> else does not cover
            #  exception
            error: dict = result.json().get("error")
            if int(error.get("code")) == 1006:
                _result = dict(error_message="No City matched the given name.")
                return render_template("index.html", result=_result)
        return render_template("index.html", result={})


if __name__ == "__main__":
    app.run(debug=True)
