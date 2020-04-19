from flask import render_template, url_for, flash, redirect
from flask_mysqldb import MySQL
import yaml
from forum import app, bcrypt
from forum.forms import RegistrationForm, LoginForm

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

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
        cur = mysql.connection.cursor()
        print("%s %s",form.username.data, form.email.data)
        cur.execute("INSERT INTO user (username,name,email,password) VALUES(%s,'Users Name', %s, %s)",
                    (form.username.data, form.email.data,hashed_password))
        mysql.connection.commit()
        cur.close()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
