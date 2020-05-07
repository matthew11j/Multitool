from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from multitool.models import Module
from multitool.static.scripts.arduino_switch import run

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    modules = Module.query.all()
    return render_template('home.html', modules=modules)

@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route('/about/arduino_switch/<action>', methods=['POST', 'GET'])
def arduino_switch(action):
    run(action)
    flash('Success!', 'success')
    return redirect(url_for('main.about'))
