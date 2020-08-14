from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError

from blog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('That username is already taken. Try another one ')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('That username is already taken. Try another one ')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])

    submit = SubmitField('Update')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if username.data !=current_user.username:
            if user:
                raise ValidationError('That username is already taken. Try another one ')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if email.data !=current_user.email:
            if user:
                raise ValidationError('That username is already taken. Try another one ')