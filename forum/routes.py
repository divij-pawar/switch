import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
import mysql.connector
from forum import app, bcrypt, login_required,session
from forum.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm

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

@app.route("/")
@app.route("/home")
def home():
    cur.execute("SELECT * FROM post")
    rows = cur.fetchall()
    print(rows)
    return render_template('home.html', title='Home', posts=rows)


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

def save_profile_picture(form_picture):
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
            picture_file = save_profile_picture(form.picture.data)
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


def save_post_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/post_pics', picture_fn)

    i = Image.open(form_picture)
    i.save(picture_path,optimize=True)

    return picture_fn

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    print(f'______________________PICTURE ADDED TO POST 1____________________{form.picture.data}')
    if form.validate_on_submit():
        if form.picture.data:
            print(f'______________________PICTURE ADDED TO POST____________________')
            picture_file = save_post_picture(form.picture.data)
            print(f'______________________PICTURE ADDED TO POST____________________{picture_file}')
        else:
            picture_file=""
        cur.execute("INSERT into post(title,image,author,p_descript,price,author_img) VALUES(%s,%s,%s,%s,%s,%s)",
                    (form.title.data,picture_file,session.get("username"),form.content.data,500,session.get("image_file")))
        con.commit()
        flash("Your post has been created!",'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',form=form,
                             legend= 'New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    cur.execute("SELECT * FROM post where p_id=%s",(post_id,))
    post = cur.fetchall()
    if not post:
        return ("<h1>404 Not Found</h1>")
    return render_template('post.html',title=post[0][1],post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    cur.execute("SELECT * FROM post where p_id=%s",(post_id,))
    post = cur.fetchall()
    if not post:
        return ("<h1>404 Not Found</h1>")
    print("____________________________",post[0][7])
    if post[0][6] != session.get("username"):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_post_picture(form.picture.data)
            print(f'______________________PICTURE UPDATE____________________{picture_file}')
            cur.execute("UPDATE post set image = %s where p_id = %s",
                    (picture_file, post_id))            
            con.commit()
        cur.execute("UPDATE post set title = %s, p_descript = %s where p_id = %s",
                    (form.title.data, form.content.data, post_id))
        con.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('post',post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post[0][1]
        form.content.data = post[0][5]
    return render_template('create_post.html', title='Update Post',
                            form=form, legend= 'Update Post' )


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    cur.execute("SELECT * FROM post where p_id=%s",(post_id,))
    post = cur.fetchall()
    if not post:
        return ("<h1>404 Not Found</h1>")
    print("____________________________",post[0][7])
    if post[0][6] != session.get("username"):
        abort(403)
    cur.execute("DELETE from post where p_id=%s",(post_id,))
    con.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('home'))
'''
@app.route("/user/<str:username>")
def user_posts(username):
    cur.execute("SELECT * FROM post where author=%s LIMIT 1",(username,))
    posts = cur.fetchall()
    if not post:
        return ("<h1>404 Not Found</h1>")
    print("____________________________",post[0][7])
    print(rows)
    return render_template('user.html', title='Home', posts=posts)
'''