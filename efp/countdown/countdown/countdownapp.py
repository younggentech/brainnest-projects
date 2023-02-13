# -*- coding: utf-8 -*-
"""
Counter app
"""

from model import get_time
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """
    Landing page
    """
    return render_template("index.html")


@app.route("/start", methods=["GET", "POST"])
def get_form():
    """
    Form page and redirection to it
    """
    if request.method == "POST":
        data = request.form.to_dict()
        if not set(data.values()).intersection({""}):
            new_data = list(get_time(data))
            return render_template("start.html", data=new_data)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=False)
