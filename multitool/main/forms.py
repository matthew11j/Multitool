from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, DateField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange, Optional, Email
from datetime import datetime

class ModuleForm(FlaskForm):
    title = StringField('Title')
    url = StringField('URL')
    image_file = StringField('Image File')
    description = StringField('Description')
    submit = SubmitField('Create')
