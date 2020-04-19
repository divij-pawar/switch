from flask import render_template, url_for, flash, redirect
import mysql.connector
from forum import app, bcrypt
from forum.forms import RegistrationForm, LoginForm

con = mysql.connector.connect(
    host = "localhost",
    user = "dev",
    password = "password",
    database = "forum",
    port = 3306
)
print("__________________Connected to Database__________________")
#cursor
cur = con.cursor()

posts = [
    {
        'op': 'Divij Pawar',
        'title': 'BEE book',
        'content': 'BEE book',
        'date_posted': 'April 20, 2018'
    },
    {
        'op': 'Prince Sah',
        'title': 'Drafter',
        'content': 'Drafter for ED',
        'date_posted': 'April 21, 2018'
    },
    {
        'op': 'Janhavi Patil',
        'title': 'Mechanics',
        'content': 'Dalal Mechanics book first year engineering',
        'date_posted': 'April 30, 2018'
    }
]
def load_user(user_id):


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login user"""
    # Forget any user-id
    '''session.clear()'''

    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash('form.password.data').decode('utf-8')
        print("__________________%s %s__________________",form.username.data, form.email.data)
        cur.execute("INSERT INTO user (username,name,email,password) VALUES(%s,'Users Name', %s, %s)",
                    (form.username.data, form.email.data,hashed_password))
        con.commit()
        cur.close()
        con.close()
        print("__________________Disconnected to Database__________________")
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
