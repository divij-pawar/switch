from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = '5756418bb0b13ty0c676dfde280ba245'
#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
#For hashing passwords
bcrypt = Bcrypt(app)
#Setup Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

from forum import routes