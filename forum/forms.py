from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, NumberRange, Optional
from forum.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=3, max=15),
                            Regexp('^\w+$', message="Username must contain only letters numbers or underscore")])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=3, max=15),
                            Regexp('^\w+$', message="Username must contain only letters numbers or underscore")])
    email = StringField('Email',validators=[DataRequired(), Email()])
    fname = StringField('First Name',validators=[Optional(), Length(min=0, max=50), Regexp('^\w+$', message="name must contain only letters numbers")])
    lname = StringField('Last Name',validators=[Optional(), Length(min=0, max=50), Regexp('^\w+$', message="name must contain only letters numbers")])
    picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Save Changes')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(max=100)])
    picture = FileField('Upload Picture',validators=[FileAllowed(['jpg','png','jpeg'])])
    price = DecimalField('Price (₹)',rounding=None, places=2,validators=[DataRequired(), NumberRange(min=0,max=10000,message="Invalid Price,please add between 0 and 10000")])
    content = TextAreaField('Content',validators=[DataRequired(),Length(max=400)])
    submit = SubmitField('Post')

class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')