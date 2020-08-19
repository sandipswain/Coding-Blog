from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
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
    
    #This method checks whether there is already a person registered
    def validate_username(self,username):
        #Searching if the user exist from the database
        user=User.query.filter_by(username=username.data).first()

        #if exist then it will raise an error
        if user:
            raise ValidationError('That username is already taken. Try another one ')

    #This method checks whether the email already exists
    def validate_email(self,email):
        #Searches for the name in the database
        user=User.query.filter_by(email=email.data).first()

        #If there then it raises an error message
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

    picture=FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
    
    submit = SubmitField('Update')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        #if the entered username is different from the current username
        if username.data !=current_user.username:
            #Checking whether the other user already exists except the current user
            if user:
                #if exists then it raises an error 
                raise ValidationError('That username is already taken. Try another one ')

    def validate_email(self,email):
        #Searches for the entered email
        user=User.query.filter_by(email=email.data).first()
        #If the entered email is not equal to the current email
        if email.data !=current_user.email:
            #if the user is present then it raises an exception
            if user:
                raise ValidationError('That username is already taken. Try another one ')

class PostForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    content=TextAreaField('Content',validators=[DataRequired()])
    submit=SubmitField('Post')
