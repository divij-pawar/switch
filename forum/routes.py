import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
import mysql.connector
from forum import app, bcrypt, login_required,session
from forum.forms import RegistrationForm, LoginForm, UpdateAccountForm

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
            session["name"] = rows[0][2]
            session["email"] = rows[0][3]
            session["image_file"] = rows[0][5]
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

def save_picture(form_picture):
    random_hex= secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)

    i = Image.open(form_picture)
    width, height = i.size   # Get dimensions

    if width>height: 
        left = (width - height)/2
        top = 0 
        right = (width + height)/2
        bottom = (height + height)/2
        i = i.crop((left, top, right, bottom))
    elif height>width:
        left = 0
        top = (height - width)/2
        right = (width + width)/2
        bottom = (height + width)/2
        i = i.crop((left, top, right, bottom))

    output_size = (125, 125)
    # Crop the center of the image
 
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            print(f'______________________PICTURE UPDATE____________________{picture_file}')
            cur.execute("UPDATE user set image_file = %s where id = %s",(picture_file,session.get("user_id")))
            con.commit()
        cur.execute("UPDATE user set username = %s, email = %s where id = %s",(form.username.data,form.email.data,session.get("user_id")))
        con.commit()
        flash('Your account has been updated','success')
        session["username"] = form.username.data
        session["email"] = form.email.data
        session["image_file"] = picture_file
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = session.get("username")
        form.email.data = session.get("email")
    image_file = url_for('static',filename='profile_pics/'+session.get("image_file"))
    return render_template('account.html', title='Account', image_file=image_file,form=form)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    print("__________________Session Flushed__________________")
    # Redirect user to login form
    return redirect(url_for('login'))
