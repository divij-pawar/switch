from flask import render_template, url_for, flash, redirect,session
import mysql.connector
from forum import app, bcrypt, login_required
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

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        print("______________Session:",session)
        return redirect(url_for('home'))    
    form = LoginForm()
    if form.validate_on_submit():
        print("__________________VALIDATED__________________")
        #if form.email.data == 'admin@blog.com' and form.password.data == 'password':
        cur.execute("SELECT * FROM user where email=%s LIMIT 1",(form.email.data,))
        rows = cur.fetchall()
        if rows and bcrypt.check_password_hash(rows[0][4],form.password.data):
            print("__________________Account Auth Successfull__________________")
            session["user_id"] = rows[0][0]
            session["username"] = rows[0][1]
            flash(f'Welcome {rows[0][1]}!', 'success')
            #flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    print("__________________NOT VALIDATED__________________")
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if session.get("user_id"):
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        print(f"__________________{form.username.data} {form.email.data}__________________")
        cur.execute("INSERT INTO user (username,name,email,password) VALUES(%s,'Users Name', %s, %s)",
                    (form.username.data, form.email.data,hashed_password))
        con.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    print("__________________Session Flushed__________________")
    # Redirect user to login form
    return redirect(url_for('login'))
