import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect,request
from blog import app, db, bcrypt
from blog.forms import RegistrationForm, LoginForm,UpdateAccountForm
from blog.models import User, Post
from flask_login import login_user,current_user,logout_user,login_required

#dummy data
posts = [
    {
        'author': 'Sandip',
        'age': 27,
        'title': 'Blog Post 1'
    },
    {
        'author': 'Spectra',
        'age': 28,
        'title': 'Blog Post 2'
    }
]


#Home Page
@app.route('/')
def main():
    return render_template('index.html', posts=posts)

#About Site
@app.route('/about')
def about():
    return render_template('about.html')

#Registration Form
@app.route('/register', methods=['GET', 'POST'])
def register():
    #Since has successfully registered then they redirected to the home page i.e.,they can't register again
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #generate hash password
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        #Instnce of User() with the info
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        #Adding the user
        db.session.add(user)
        #Commiting to the database
        db.session.commit()
        #message
        flash(
            f'Account created for {form.username.data}! You are now able to log in', 'success')
        #redirects us to login to the page after registering successfully
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

#Login Form
@app.route('/login', methods=['GET', 'POST'])
def login():
    #Check whether the current user has provided the valid credentials
    #Since has successfully logged in then they redirected to the home page i.e.,they can't login again

    if current_user.is_authenticated:
        #If logged in then it redirects to the Home Page
        return redirect(url_for('home'))
    #An instance of LoginForm()
    form=LoginForm()
    #Checks whether the form has a POST or GET request or both
    if form.validate_on_submit():
        #Fetches the user with the email if its there in the database
        user=User.query.filter_by(email=form.email.data).first()
        #Compares the hashed password with the entered password 
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            #if the condition is true then it logins in the user with the following attribute
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            #redirect to the nextpage if nextpage exists but if its none or false then return to the main page
            return redirect(next_page) if next_page else redirect (url_for('main'))
        else:
            flash('Login Unsuccessful. Please check your email or password and try again ','danger')
    return render_template('login.html',form=form)

#Logout Option
@app.route('/logout')
def logout():
    #A method that log's out the current user
    logout_user()
    #After logging out then it redirects the user to the Home Page
    return redirect(url_for('main'))

#Saves users uploaded image from the file system
def save_picture(form_picture):
    #to avoid match of profile pic name
    #generating random hexa characters
    random_hex=secrets.token_hex(8)
    #function returns 2 values :- it returns the filename without the extension and it returns the extension itself
    #the filename of the picture we are uploading is mentioned as the parameter
    #We use underscore to avoid variable name
    _,f_ext=os.path.splitext(form_picture.filename)
    #Combining the random hex with the file extension
    picture_fn=random_hex+f_ext
    #To get the full path where the image will be saved so tht Python can know where we are saving it
    #In order to this we will use root path attribute which will gives us the path all the way to our directory
    #picturepath-><app.root_path>/<static/img>/<picture_fn>
    picture_path=os.path.join(app.root_path,'static/img',picture_fn)
    #Setting the dimension for resizing the image 
    output_size=(125,125)
    #Opening the image 
    i=Image.open(form_picture)
    #Resizing the image
    i.thumbnail(output_size)
    #Saving the image to our static folder
    i.save(picture_path)
    return picture_fn


#Account Info
@app.route('/account',methods=['GET','POST'])
#Mandatory login required
@login_required
def account():
    #Creating an instance
    form=UpdateAccountForm()
    #validate_on_submit() checks whether the is ready for either GET or POST request or both
    if form.validate_on_submit():
        if form.picture.data:
            #getting the filename
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file

        #Changing and commiting  the current user variable with the entered value 
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        #A  message displayed on success
        flash('Your Account has been updated !!!','success')
        #redirecting to the account page . Redirecting is done here to avoid Confirm Resubmission pop up message
        return redirect(url_for('account'))
    #To display the current username and email    
    elif request.method =='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email

        
    image_file=url_for('static',filename='img/'+current_user.image_file)
    return render_template('account.html',image_file=image_file,form=form) 