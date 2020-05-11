import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from forum import mail

def save_profile_picture(form_picture):
    random_hex= secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,'static/profile_pics',picture_fn)

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

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset',
                   sender='workdivij@gmail.com',
                   recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('users.reset_token',token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made
'''
    mail.send(msg)