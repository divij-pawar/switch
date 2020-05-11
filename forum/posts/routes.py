from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from forum import db
from forum.models import Post
from forum.posts.forms import PostForm
from forum.posts.utils import save_post_picture

posts = Blueprint('posts',__name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_post_picture(form.picture.data)
            print(f'______________________PICTURE ADDED TO POST____________________{picture_file}')
        else:
            picture_file=""
        post = Post(title=form.title.data,image_file = picture_file, price = form.price.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!",'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',form=form,
                             legend= 'New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_post_picture(form.picture.data)
            print(f'______________________PICTURE UPDATE____________________{picture_file}')
            post.image_file = picture_file
        post.title = form.title.data
        post.price = form.price.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('posts.post',post_id=post_id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.price.data = post.price
    return render_template('create_post.html', title='Update Post',
                            form=form, legend= 'Update Post' )


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('main.home'))