from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, DateField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange, Optional, Email
from datetime import datetime

class Seed(FlaskForm):
    seed_select = SelectField('Seed Select', choices=[("", ""), ('artist', 'Artist'), ('song', 'Song'), ('genre', 'Genre')] , coerce=str)
    seed_string = StringField('Seed String')

class Recommendation(FlaskForm):
    seeds = FieldList(FormField(Seed), min_entries=5,  max_entries=5)
    submit = SubmitField('Create')