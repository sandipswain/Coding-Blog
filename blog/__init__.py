from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
# Secret Key
app.config['SECRET_KEY'] = 'd7c46b7abd2a614a2e818454706d03d9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
#login_view denotes to the function name of the route here and it performs the same as url_for function  
login_manager.login_view='login'
#Displays the message while accessing a content while not logged in 
login_manager.login_message_category='info'
from blog import routes
