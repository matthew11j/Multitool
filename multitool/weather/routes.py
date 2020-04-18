from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from multitool import db, bcrypt
from datetime import date, datetime, timedelta
import json

from multitool.static.scripts.getWeatherData import run

weather = Blueprint('weather', __name__)

@weather.route("/weather")
def weatherDash():
    json_obj = run()
    weather_data = json_obj['weather_data']
    # data = weather_data[0]
    # for key in data.keys():
    #     print(key)
    # print(json.dumps(weather_data, indent=2, sort_keys=True))
    return render_template('weather.html', title='Weather Dashboard', weather_data=weather_data)
    