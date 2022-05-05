from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user,logout_user,current_user,login_required
from datetime import datetime


app = Flask(__name__)

app.config['SECRET_KEY'] ='webdev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager=LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from ttg import routes