from flask import Flask,redirect,session,flash
from flask_session import Session
from flask_bcrypt import Bcrypt
from tempfile import mkdtemp
from functools import wraps

# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = '5756418bb0b13ty0c676dfde280ba245'
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True   
bcrypt = Bcrypt(app)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash('Please log in to access this page', 'info')
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

from forum import routes