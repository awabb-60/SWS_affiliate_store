from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)

bc = Bcrypt(app)

login_manager = LoginManager(app)

# if you try to go to a restricted route and you are not logedin this is the view that will show
login_manager.login_view = 'home'

# to but a category in the flashed message
login_manager.login_message_category = 'info'





app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'e390b1ae1db6eb464e3867db560d3cb42f03fe2a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///afs.db'



db = SQLAlchemy(app)

from affiliate_store import routes
