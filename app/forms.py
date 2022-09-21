# app > forms.py

from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, StringField, IntegerField, DecimalField, PasswordField, RadioField, MultipleFileField
from wtforms.validators import InputRequired, Email, EqualTo, Length
from wtforms.widgets import TextArea

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
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=32), EqualTo(
        'confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')


class UserUpdate(UserForm, FlaskForm):
    '''Form for user update'''


class NewProjectForm(FlaskForm):
    '''Form for submitting new project car'''

    model_id = HiddenField('model_id', validators=[])
    name = StringField('Project Name', validators=[Length(max=32)])
    description = StringField('Description', validators=[
                              Length(max=500)], widget=TextArea())
    private = RadioField('Visibility', default=1,
                         choices=PrivacyStatus.choices, coerce=PrivacyStatus.coerce)

    horsepower = IntegerField('Horsepower', default=0)
    torque = IntegerField('Torque(ft/lb)', default=0)
    weight = IntegerField('Weight(lb)', default=0)
    drivetrain = SelectField('Drivetrain', choices=Drivetrain.choices,
                             coerce=Drivetrain.coerce)
    engine_size = DecimalField('Engine Size(L)')

    # WIP - pictures = MultipleFileField()
