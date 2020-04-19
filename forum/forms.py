from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import mysql.connector

con = mysql.connector.connect(
    host = "localhost",
    user = "dev",
    password = "password",
    database = "forum",
    port = 3306
)
print("Connected to Database")
#cursor
cur = con.cursor()

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        cur.execute("SELECT * FROM user where username=%s LIMIT 1",(username.data,))
        rows = cur.fetchall()
        if rows:
            raise ValidationError('That username is taken.Please choose a different one.')
    
    def validate_email(self, email):
        cur.execute("SELECT * FROM user where email=%s LIMIT 1",(email.data,))
        rows = cur.fetchall()
        if rows:
            raise ValidationError('That email is taken.Please choose a different one.')
        
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')