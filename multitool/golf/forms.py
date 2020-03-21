from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange, Optional
from flask_login import current_user
from datetime import datetime
from multitool.models import Golf_Round, Users

class Round(FlaskForm):
    h1Score = IntegerField('Hole 1 Score', validators=[NumberRange(0, 15), Optional()])
    h2Score = IntegerField('Hole 2 Score', validators=[NumberRange(0, 15), Optional()])
    h3Score = IntegerField('Hole 3 Score', validators=[NumberRange(0, 15), Optional()])
    h4Score = IntegerField('Hole 4 Score', validators=[NumberRange(0, 15), Optional()])
    h5Score = IntegerField('Hole 5 Score', validators=[NumberRange(0, 15), Optional()])
    h6Score = IntegerField('Hole 6 Score', validators=[NumberRange(0, 15), Optional()])
    h7Score = IntegerField('Hole 7 Score', validators=[NumberRange(0, 15), Optional()])
    h8Score = IntegerField('Hole 8 Score', validators=[NumberRange(0, 15), Optional()])
    h9Score = IntegerField('Hole 9 Score', validators=[NumberRange(0, 15), Optional()])
    h10Score = IntegerField('Hole 10 Score', validators=[NumberRange(0, 15), Optional()])
    h11Score = IntegerField('Hole 11 Score', validators=[NumberRange(0, 15), Optional()])
    h12Score = IntegerField('Hole 12 Score', validators=[NumberRange(0, 15), Optional()])
    h13Score = IntegerField('Hole 13 Score', validators=[NumberRange(0, 15), Optional()])
    h14Score = IntegerField('Hole 14 Score', validators=[NumberRange(0, 15), Optional()])
    h15Score = IntegerField('Hole 15 Score', validators=[NumberRange(0, 15), Optional()])
    h16Score = IntegerField('Hole 16 Score', validators=[NumberRange(0, 15), Optional()])
    h17Score = IntegerField('Hole 17 Score', validators=[NumberRange(0, 15), Optional()])
    h18Score = IntegerField('Hole 18 Score', validators=[NumberRange(0, 15), Optional()])
    h1Putt = IntegerField('Hole 1 Putt', validators=[NumberRange(0, 6), Optional()])
    h2Putt = IntegerField('Hole 2 Putt', validators=[NumberRange(0, 6), Optional()])
    h3Putt = IntegerField('Hole 3 Putt', validators=[NumberRange(0, 6), Optional()])
    h4Putt = IntegerField('Hole 4 Putt', validators=[NumberRange(0, 6), Optional()])
    h5Putt = IntegerField('Hole 5 Putt', validators=[NumberRange(0, 6), Optional()])
    h6Putt = IntegerField('Hole 6 Putt', validators=[NumberRange(0, 6), Optional()])
    h7Putt = IntegerField('Hole 7 Putt', validators=[NumberRange(0, 6), Optional()])
    h8Putt = IntegerField('Hole 8 Putt', validators=[NumberRange(0, 6), Optional()])
    h9Putt = IntegerField('Hole 9 Putt', validators=[NumberRange(0, 6), Optional()])
    h10Putt = IntegerField('Hole 10 Putt', validators=[NumberRange(0, 6), Optional()])
    h11Putt = IntegerField('Hole 11 Putt', validators=[NumberRange(0, 6), Optional()])
    h12Putt = IntegerField('Hole 12 Putt', validators=[NumberRange(0, 6), Optional()])
    h13Putt = IntegerField('Hole 13 Putt', validators=[NumberRange(0, 6), Optional()])
    h14Putt = IntegerField('Hole 14 Putt', validators=[NumberRange(0, 6), Optional()])
    h15Putt = IntegerField('Hole 15 Putt', validators=[NumberRange(0, 6), Optional()])
    h16Putt = IntegerField('Hole 16 Putt', validators=[NumberRange(0, 6), Optional()])
    h17Putt = IntegerField('Hole 17 Putt', validators=[NumberRange(0, 6), Optional()])
    h18Putt = IntegerField('Hole 18 Putt', validators=[NumberRange(0, 6), Optional()])
    frontScore = StringField('Front Score')
    backScore = StringField('Back Score')
    totalScore = StringField('Total Score')
    description = TextAreaField('Description')
    date_played = DateField('Date Played', format='%Y-%m-%d', validators=[Optional()])
    # course_played = StringField('Course Played')
    course_played = SelectField('Course Played', coerce=str)
    submit = SubmitField('')

class Course(FlaskForm):
    name = StringField('Course Name', validators=[DataRequired()])
    h1Par = IntegerField('Hole 1 Par', validators=[NumberRange(0, 6), Optional()])
    h2Par = IntegerField('Hole 1 Par', validators=[NumberRange(0, 6), Optional()])
    h3Par = IntegerField('Hole 1 Par', validators=[NumberRange(0, 6), Optional()])
    h4Par = IntegerField('Hole 1 Par', validators=[NumberRange(0, 6), Optional()])
    h5Par = IntegerField('Hole 1 Par', validators=[NumberRange(0, 6), Optional()])
    h6Par = IntegerField('Hole 1 Par', validators=[NumberRange(0, 6), Optional()])
    h7Par = IntegerField('Hole 1 Par', validators=[NumberRange(0, 6), Optional()])
    h8Par = IntegerField('Hole 1 Par', validators=[NumberRange(0, 6), Optional()])
    h9Par = IntegerField('Hole 1 Par', validators=[NumberRange(0, 6), Optional()])
    h10Par = IntegerField('Hole 1 Par', validators=[NumberRange(0, 6), Optional()])
    h11Par = IntegerField('Hole 1 Par', validators=[NumberRange(0, 6), Optional()])
    h12Par = IntegerField('Hole 1 Par', validators=[NumberRange(0, 6), Optional()])
    h13Par = IntegerField('Hole 1 Par', validators=[NumberRange(0, 6), Optional()])
    h14Par = IntegerField('Hole 1 Par', validators=[NumberRange(0, 6), Optional()])
    h15Par = IntegerField('Hole 1 Par', validators=[NumberRange(0, 6), Optional()])
    h16Par = IntegerField('Hole 1 Par', validators=[NumberRange(0, 6), Optional()])
    h17Par = IntegerField('Hole 1 Par', validators=[NumberRange(0, 6), Optional()])
    h18Par = IntegerField('Hole 1 Par', validators=[NumberRange(0, 6), Optional()])
    submit = SubmitField('Add Course')