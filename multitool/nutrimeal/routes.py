import logging
from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify, current_app
from flask_wtf import Form
from multitool import db, bcrypt
from datetime import date, datetime, timedelta
from flask_login import current_user
from subprocess import call

nutrimeal = Blueprint('nutrimeal', __name__)
# logging.basicConfig(filename='multitool_log.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')
# logger = logging.getLogger('Multitool')

@nutrimeal.route("/nutrimeal")
def home():
    return render_template('nutrimeal_dashboard.html', title='Nutrimeal')

@nutrimeal.route("/nutrimeal/profile")
def profile():
    return render_template('nutrimeal_profile.html', title='Nutrimeal Profile')

@nutrimeal.route("/nutrimeal/explore")
def explore():
    return render_template('nutrimeal_explore.html', title='Nutrimeal Explore')

@nutrimeal.route("/nutrimeal/edit")
def edit():
    return render_template('nutrimeal_edit.html', title='Nutrimeal Edit Schedule')