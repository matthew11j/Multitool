from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_wtf import Form
from wtforms.fields.html5 import DateField
from multitool import db, bcrypt
from multitool.golf.forms import Round, Course
from flask_login import current_user
from datetime import datetime, date
from multitool.golf.utils import submit_round, get_par_averages
from multitool.models import Golf_Round, Golf_Course
import json

golf = Blueprint('golf', __name__)

@golf.route("/golftracker/<username>")
def golftracker(username):
    #golf_rounds = Golf_Round.query.all()
    #if current_user.is_authenticated and current_user.username == username:
    if current_user.is_authenticated:
        if current_user.username != username:
            usernameCreated = username
        else:
            usernameCreated = current_user.username
    else: 
        usernameCreated = ''
    
    golf_rounds = Golf_Round.query.filter_by(created_by=usernameCreated)
    golf_courses = Golf_Course.query.all()

    Dict = {}
    GCCnt = 0;
    BCCnt = 0
    AFCnt = 0
    MiscCnt = 0
    if golf_rounds.count() > 1:
        for golf_round in golf_rounds:
            course = golf_round.course_played
            if (course == 'Green Crest'):
                GCCnt += 1
            elif (course == 'Beech Creek'):
                BCCnt += 1
            elif (course == 'Avon Fields'):
                AFCnt += 1
            else:
                MiscCnt += 1
        Dict['avgPars'] = get_par_averages(golf_courses, golf_rounds)

    Dict['GCCnt'] = GCCnt
    Dict['BCCnt'] = BCCnt
    Dict['AFCnt'] = AFCnt
    Dict['MiscCnt'] = MiscCnt

    return render_template('golftracker.html', title='Golf Tracker', golf_rounds=golf_rounds, golf_courses=golf_courses, payloadJS=json.dumps(Dict), payload=Dict, usernameCreated=usernameCreated)

@golf.route("/golftracker/<username>/addround", methods=['GET', 'POST'])
def addround(username):
    form = Round()
    golf_courses = Golf_Course.query.all()
    form.course_played.choices = [(course.name, course.name) for course in golf_courses]
    form.submit.label.text = "Add Round"
    if form.validate():
        if current_user.is_authenticated:
            if current_user.username == username:
                form = submit_round(form)
                new_golf_round = Golf_Round(description=form.description.data, h1Score=form.h1Score.data, h2Score=form.h2Score.data,
                                                h3Score=form.h3Score.data, h4Score=form.h4Score.data, h5Score=form.h5Score.data,
                                                h6Score=form.h6Score.data, h7Score=form.h7Score.data, h8Score=form.h8Score.data,
                                                h9Score=form.h9Score.data, h10Score=form.h10Score.data, h11Score=form.h11Score.data,
                                                h12Score=form.h12Score.data, h13Score=form.h13Score.data, h14Score=form.h14Score.data,
                                                h15Score=form.h15Score.data, h16Score=form.h16Score.data, h17Score=form.h17Score.data,
                                                h18Score=form.h18Score.data, h1Putt=form.h1Putt.data, h2Putt=form.h2Putt.data,
                                                h3Putt=form.h3Putt.data, h4Putt=form.h4Putt.data, h5Putt=form.h5Putt.data,
                                                h6Putt=form.h6Putt.data, h7Putt=form.h7Putt.data, h8Putt=form.h8Putt.data,
                                                h9Putt=form.h9Putt.data, h10Putt=form.h10Putt.data, h11Putt=form.h11Putt.data,
                                                h12Putt=form.h12Putt.data, h13Putt=form.h13Putt.data, h14Putt=form.h14Putt.data,
                                                h15Putt=form.h15Putt.data, h16Putt=form.h16Putt.data, h17Putt=form.h17Putt.data,
                                                h18Putt=form.h18Putt.data, date_played=form.date_played.data,
                                                backScore=form.backScore.data, frontScore=form.frontScore.data,
                                                totalScore=form.totalScore.data, course_played=form.course_played.data, created_by=current_user.username)
                db.session.add(new_golf_round)
                db.session.commit()
                flash('Round added!', 'success')
            else :
                flash('User not authenticated', 'danger')
        else:
            flash('Cannot create round. Please create an account before tracking golf data', 'danger')
        return jsonify(status='ok')
    return render_template('dialogs/round/add.html', form=form, golf_courses=golf_courses, action="add")

@golf.route("/golftracker/<username>/addcourse", methods=['GET', 'POST'])
def addcourse(username):
    form = Course()
    if form.validate_on_submit():
        if current_user.username == username:
            new_golf_course = Golf_Course(name=form.name.data, h1Par=form.h1Par.data, h2Par=form.h2Par.data, h3Par=form.h3Par.data,
                                            h4Par=form.h4Par.data, h5Par=form.h5Par.data, h6Par=form.h6Par.data, h7Par=form.h7Par.data,
                                            h8Par=form.h8Par.data, h9Par=form.h9Par.data, h10Par=form.h10Par.data, h11Par=form.h11Par.data,
                                            h12Par=form.h12Par.data, h13Par=form.h13Par.data, h14Par=form.h14Par.data, h15Par=form.h15Par.data,
                                            h16Par=form.h16Par.data, h17Par=form.h17Par.data, h18Par=form.h18Par.data)
            db.session.add(new_golf_course)
            db.session.commit()
            flash('Course added!', 'success')
        else :
            flash('User not authenticated', 'danger')
        return jsonify(status='ok')
    return render_template('dialogs/course/add.html', form=form)

@golf.route("/golftracker/<username>/editround/<int:round_id>", methods=['GET', 'POST'])
def editround(username, round_id):
    golf_courses = Golf_Course.query.all()
    golf_round = db.session.query(Golf_Round).filter(Golf_Round.id == round_id).one_or_none()
    form = Round(obj=golf_round)
    form.course_played.choices = [(course.name, course.name) for course in golf_courses]
    form.submit.label.text = "Save"
    if form.validate():
        if current_user.username == username:
            form = submit_round(form)
            form.populate_obj(golf_round)
            db.session.commit()
            flash('Round updated!', 'success')
        else :
            flash('User not authenticated', 'danger')
        return jsonify(status='ok')
    return render_template('dialogs/round/add.html', form=form, golf_round=golf_round, golf_courses=golf_courses, action='edit', usernameCreated=username)

@golf.route("/golftracker/<username>/deleteround/<int:round_id>", methods=['POST'])
def deleteround(username, round_id):
    print('here1')
    if current_user.username == username:
        print('here')
        Golf_Round.query.filter_by(id=round_id).delete()
        db.session.commit()
        flash('Round deleted!', 'success')
        return redirect(url_for('golf.golftracker', username=current_user.username))
    else :
        flash('User not authenticated', 'danger')
        return redirect(url_for('golf.golftracker', username=username))
    
