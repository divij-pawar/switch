from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, NumberRange, Length

class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(max=100)])
    picture = FileField('Upload Picture',validators=[FileAllowed(['jpg','png','jpeg'])])
    price = DecimalField('Price (₹)',rounding=None, places=2,validators=[DataRequired(), NumberRange(min=0,max=10000,message="Invalid Price,please add between 0 and 10000")])
    content = TextAreaField('Content',validators=[DataRequired(),Length(max=400)])
    submit = SubmitField('Post')
