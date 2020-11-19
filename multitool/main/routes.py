import logging
from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_wtf import Form
from wtforms.fields.html5 import DateField
from multitool import db, bcrypt
from multitool.golf.forms import Round, Course
from flask_login import current_user
from datetime import datetime, date
from multitool.models import Module
from multitool.static.scripts.arduino_switch import run
from multitool.main.forms import ModuleForm

main = Blueprint('main', __name__)
# logging.basicConfig(filename='multitool_log.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')
# logger = logging.getLogger('Multitool')

@main.route("/")
# @main.route("/home")
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

@main.route("/addmodule", methods=['GET', 'POST'])
def addmodule():
    form = ModuleForm()
    if form.validate():
        if current_user.is_authenticated:
            # if not form.image_file.data:
            #     form.image_file.data = 'default.jpg'

            new_module = Module(title=form.title.data, description=form.description.data, image_file=form.image_file.data, url=form.url.data)
            db.session.add(new_module)
            db.session.commit()
            flash('Module added!', 'success')
        else:
            flash('Failed to create new module', 'danger')
        return jsonify(status='ok')
    return render_template('dialogs/module/add.html', form=form, action='add')

@main.route("/editmodule/<int:module_id>", methods=['GET', 'POST'])
def editmodule(module_id):
    modules = Module.query.all()
    module = db.session.query(Module).filter(Module.id == module_id).one_or_none()
    form = ModuleForm(obj=module)
    form.submit.label.text = "Save"
    if form.validate():
        if current_user.is_authenticated:
            form.populate_obj(module)
            db.session.commit()
            flash('Module updated!', 'success')
        else :
            flash('User not authenticated', 'danger')
        return jsonify(status='ok')
    return render_template('dialogs/module/add.html', form=form, module=module, action='edit')

@main.route("/deletemodule/<int:module_id>", methods=['POST'])
def deletemodule(module_id):
    if current_user.is_authenticated:
        Module.query.filter_by(id=module_id).delete()
        db.session.commit()
        flash('Module deleted!', 'success')
        return redirect(url_for('main.home'))
    else :
        flash('User not authenticated', 'danger')
        return redirect(url_for('main.home'))
