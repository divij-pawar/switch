from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
import mysql.connector

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
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=15),Regexp('^\w+$', message="Username must contain only letters numbers or underscore")])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        cur.execute("SELECT username FROM user where username=%s LIMIT 1",(username.data,))
        rows = cur.fetchall()
        print(f"username checking...{rows}")
        if rows:
            raise ValidationError('That username is taken.Please choose a different one.')

    def validate_email(self, email):
        cur.execute("SELECT email FROM user where email=%s LIMIT 1",(email.data,))
        rows = cur.fetchall()
        print(f"email checking...{rows}")
        if rows:
            raise ValidationError('That email is taken.Please choose a different one.')
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')