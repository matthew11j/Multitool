from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from multitool import db, bcrypt
from multitool.golf.forms import Add_Round, Add_Course
from multitool.models import Golf_Round, Golf_Course

golf = Blueprint('golf', __name__)

@golf.route("/golftracker")
def golftracker():
    golf_rounds = Golf_Round.query.all()
    golf_courses = Golf_Course.query.all()
    return render_template('golftracker.html', title='Golf Tracker', golf_rounds=golf_rounds, golf_courses=golf_courses)

@golf.route("/golftracker/addround", methods=['GET', 'POST'])
def addround():
    form = Add_Round()
    golf_courses = Golf_Course.query.all()
    if form.validate_on_submit():
        # Calculating front, back, total Scores
        # Defaulting empty scores
        scores = []
        scores.extend((form.h1Score, form.h2Score, form.h3Score, form.h4Score, form.h5Score, form.h6Score, form.h7Score, form.h8Score,
                            form.h9Score, form.h10Score, form.h11Score, form.h12Score, form.h13Score, form.h14Score, form.h15Score, form.h16Score,
                            form.h17Score, form.h18Score))
        front = 0
        back = 0
        cnt = 0
        for score in scores:
            if not score.data:
                score.data = 0
            int_score = int(score.data)
            if cnt < 9:
                front = front + int_score
            else:
                back = back + int_score
            cnt = cnt + 1
        total = back + front

        # Defaulting empty putts
        putts = []
        putts.extend((form.h1Putt, form.h2Putt, form.h3Putt, form.h4Putt, form.h5Putt, form.h6Putt, form.h7Putt, form.h8Putt,
                            form.h9Putt, form.h10Putt, form.h11Putt, form.h12Putt, form.h13Putt, form.h14Putt, form.h15Putt, form.h16Putt,
                            form.h17Putt, form.h18Putt))
        for putt in putts:
            if not putt.data:
                putt.data = 0

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
                                        backScore=back, frontScore=front, totalScore=total, course_played=form.course_played.data)
        db.session.add(new_golf_round)
        db.session.commit()
        flash('Round added!', 'success')
        return jsonify(status='ok')
    return render_template('addround/add.html', form=form, golf_courses=golf_courses)

@golf.route("/golftracker/addcourse", methods=['GET', 'POST'])
def addcourse():
    form = Add_Course()
    if form.validate_on_submit():
        new_golf_course = Golf_Course(name=form.name.data)
        db.session.add(new_golf_course)
        db.session.commit()
        flash('Course added!', 'success')
        return jsonify(status='ok')
    return render_template('addcourse/add.html', form=form)