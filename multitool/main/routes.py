from flask import render_template, request, Blueprint
from multitool.models import Module

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    modules = Module.query.all()
    return render_template('home.html', modules=modules)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
