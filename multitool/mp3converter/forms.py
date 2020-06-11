from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, DateField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange, Optional, Email
from datetime import datetime

class Song_Url(FlaskForm):
    download_file_path = StringField('Download File Path')
    url_string = StringField('URL String', validators=[DataRequired()])
    submit = SubmitField('Convert')
