# app > forms.py

from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, StringField, IntegerField, DecimalField, PasswordField, RadioField, MultipleFileField
from wtforms.validators import InputRequired, Email, EqualTo, Length
from wtforms.widgets import TextArea, TextInput

from app.models.enums import Drivetrain, PrivacyStatus


class LoginForm(FlaskForm):
    """Form for user login"""

    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=32)])


class UserForm(LoginForm, FlaskForm):
    """Form for user signup"""

    email = StringField('E-mail', validators=[InputRequired(), Email()])
    password = PasswordField('New Password', validators=[InputRequired(), Length(min=8, max=32), EqualTo(
        'confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat New Password')


class UserUpdate(UserForm, FlaskForm):
    '''Form for user update'''
    old_password = PasswordField('Old Password')


class NewProjectForm(FlaskForm):
    '''Form for submitting new project car'''

    year = HiddenField('year')
    make = HiddenField('make')
    model = HiddenField('model')
    model_id = HiddenField('model_id')
    name = StringField('Project Name', validators=[
                       InputRequired(), Length(max=32)])
    description = StringField('Description', validators=[
        Length(max=500)], widget=TextArea())
    private = RadioField('Visibility', default='PUBLIC',
                         choices=PrivacyStatus.choices)

    horsepower = IntegerField('Horsepower', default=0)
    torque = IntegerField('Torque(ft/lb)', default=0)
    weight = IntegerField('Weight(lb)', default=0)
    drivetrain = SelectField('Drivetrain', choices=Drivetrain.choices)
    engine_size = DecimalField('Engine Size(L)', default=0)

    # WIP - pictures = MultipleFileField()


class EditProjectForm(NewProjectForm, FlaskForm):
    '''Form for editing a project car'''
    year = IntegerField('Year', widget=TextInput())
    make = StringField('Make', validators=[Length(max=40)])
    model = StringField('Model', validators=[Length(max=40)])
