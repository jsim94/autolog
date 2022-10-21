# app > forms.py

from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, StringField, IntegerField, DecimalField, PasswordField, RadioField, MultipleFileField
from wtforms.validators import InputRequired, Email, EqualTo, Length
from wtforms.widgets import TextArea, TextInput

from app.models.enums import Drivetrain, PrivacyStatus


class LoginForm(FlaskForm):
    """Form for user login"""

    username = StringField('Username', validators=[
                           InputRequired()])
    password = PasswordField('Password', validators=[
                             InputRequired()])


class SignupForm(FlaskForm):
    """Form for user signup"""

    email = StringField('E-mail', validators=[InputRequired(), Email()])
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=20)])
    password = PasswordField('New Password', validators=[InputRequired(), Length(min=8, max=32), EqualTo(
        'confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat New Password')


class UserEdit(SignupForm, FlaskForm):
    '''Form for user update'''
    old_password = PasswordField('Old Password')


class NewProjectForm(FlaskForm):
    '''Form for submitting new project car'''

    year = HiddenField('year')
    make = HiddenField('make')
    model = HiddenField('model')
    model_id = HiddenField('model_id')
    name = StringField('Project Name', validators=[
                       InputRequired(), Length(min=4, max=32)])
    description = StringField('Description', validators=[
        Length(max=500)], widget=TextArea())
    private = RadioField('Visibility', default='PUBLIC',
                         choices=PrivacyStatus.choices)

    horsepower = IntegerField('Horsepower', default=0)
    torque = IntegerField('Torque(ft/lb)', default=0)
    weight = IntegerField('Weight(lb)', default=0)
    drivetrain = SelectField('Drivetrain', choices=Drivetrain.choices)
    engine_size = DecimalField('Engine Size(L)', default=0)


class EditProjectForm(NewProjectForm, FlaskForm):
    '''Form for editing a project car'''
    year = IntegerField('Year', widget=TextInput())
    make = StringField('Make', validators=[Length(max=40)])
    model = StringField('Model', validators=[Length(max=40)])


class AddModForm(FlaskForm):
    '''Form for adding a mod to a project'''
    mod = StringField('Describe Mod', validators=[
                      Length(max=50), InputRequired()], render_kw={'autocomplete': 'off'})


class UpdateForm(FlaskForm):
    '''Form for adding an update to a project'''
    title = StringField('Title', validators=[Length(
        max=60)], render_kw={'autocomplete': 'off'})
    content = StringField('Post your new update',
                          widget=TextArea(), validators=[Length(max=750), InputRequired()], render_kw={'autocomplete': 'off'})


class CommentForm(FlaskForm):
    '''Form for adding a comment to a project'''
    content = StringField('', validators=[
                          Length(max=250), InputRequired()], render_kw={'placeholder': 'Comment', 'autocomplete': 'off'})
    user_id = HiddenField('user_id')
