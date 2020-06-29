import json
import logging
from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from multitool import db, bcrypt
from datetime import date, datetime, timedelta
from multitool.static.scripts.get_weather_data import run

weather = Blueprint('weather', __name__)
logging.basicConfig(filename='multitool.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')
logger = logging.getLogger('Multitool')

@weather.route("/weather")
def weather_dash():
    json_obj = run()
    weather_data = json_obj['weather_data']
    # data = weather_data[0]
    # for key in data.keys():
    #     print(key)
    # print(json.dumps(weather_data, indent=2, sort_keys=True))
    return render_template('weather.html', title='Weather Dashboard', weather_data=weather_data)
    