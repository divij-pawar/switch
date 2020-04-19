from flask import Flask
from flask_bcrypt import Bcrypt

# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = '5756418bb0b13ty0c676dfde280ba245'
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True   
bcrypt = Bcrypt(app)

from forum import routes