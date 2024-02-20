import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# define routes for the home page, displaying all posts
@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()  # get all posts from the database
    return render_template('home.html', posts=posts)  # render the home page with posts

# define the route for the about page
@app.route("/about")
def about():
    return render_template('about.html', title='About')  # render the about page

# define the route for user registration, handling both get and post requests
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # check if user is already logged in
        return redirect(url_for('home'))  # redirect to home if logged in
    form = RegistrationForm()
    if form.validate_on_submit():  # check if form submission is valid
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # hash the password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)  # create new user
        db.session.add(user)  # add user to database
        db.session.commit()  # commit changes to database
        flash('Your account has been created! You are now able to log in', 'success')  # flash success message
        return redirect(url_for('login'))  # redirect to login page
    return render_template('register.html', title='Register', form=form)  # render registration form

# define the route for user login, handling both get and post requests
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # check if user is already logged in
        return redirect(url_for('home'))  # redirect to home if logged in
    form = LoginForm()
    if form.validate_on_submit():  # check if form submission is valid
        user = User.query.filter_by(email=form.email.data).first()  # find user by email
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # check if password is correct
            login_user(user, remember=form.remember.data)  # log in user
            next_page = request.args.get('next')  # get the next page to navigate to, if any
            return redirect(next_page) if next_page else redirect(url_for('home'))  # redirect to next page or home
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')  # flash error message
    return render_template('login.html', title='Login', form=form)  # render login form

# define the route for user logout
@app.route("/logout")
def logout():
    logout_user()  # log out user
    return redirect(url_for('home'))  # redirect to home page

# function to save user's profile picture
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)  # generate random hex for file name
    _, f_ext = os.path.splitext(form_picture.filename)  # get file extension from uploaded file
    picture_fn = random_hex + f_ext  # create new file name
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)  # define file path

    output_size = (125, 125)  # set output size for picture
    i = Image.open(form_picture)  # open image
    i.thumbnail(output_size)  # resize image
    i.save(picture_path)  # save resized image

    return picture_fn  # return filename of saved picture

# define the route for the account page, handling both get and post requests
@app.route("/account", methods=['GET', 'POST'])
@login_required  # require user to be logged in to access this route
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():  # check if form submission is valid
        if form.picture.data:  # check if a picture was uploaded
            picture_file = save_picture(form.picture.data)  # save uploaded picture
            current_user.image_file = picture_file  # update current user's profile image
        current_user.username = form.username.data  # update username
        current_user.email = form.email.data  # update email
        db.session.commit()  # commit changes to database
        flash('Your account has been updated!', 'success')  # flash success message
        return redirect(url_for('account'))  # redirect back to account page
    elif request.method == 'GET':  # if request is get, pre-populate form with current user's info
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)  # get url for profile image
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)  # render account page

# define the route for creating new posts, handling both get and post requests
@app.route("/post/new", methods=['GET', 'POST'])
@login_required  # require user to be logged in to access this route
def new_post():
    form = PostForm()
    if form.validate_on_submit():  # check if form submission is valid
        post = Post(title=form.title.data, content=form.content.data, author=current_user)  # create new post
        db.session.add(post)  # add post to database
        db.session.commit()  # commit changes to database
        flash('Your post has been created!', 'success')  # flash success message
        return redirect(url_for('home'))  # redirect to home page
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')  # render post creation form

# define the route for displaying a specific post
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)  # get post by id or return 404 error if not found
    return render_template('post.html', title=post.title, post=post)  # render post page

# define the route for updating a post, handling both get and post requests
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required  # require user to be logged in and the author of the post to access this route
def update_post(post_id):
    post = Post.query.get_or_404(post_id)  # get post by id or return 404 error if not found
    if post.author != current_user:  # check if current user is the author of the post
        abort(403)  # return forbidden error if not the author
    form = PostForm()
    if form.validate_on_submit():  # check if form submission is valid
        post.title = form.title.data  # update post title
        post.content = form.content.data  # update post content
        db.session.commit()  # commit changes to database
        flash('Your post has been updated!', 'success')  # flash success message
        return redirect(url_for('post', post_id=post.id))  # redirect to updated post
    elif request.method == 'GET':  # if request is get, pre-populate form with post's current info
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')  # render post update form

# define the route for deleting a post, handling post requests only
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required  # require user to be logged in and the author of the post to access this route
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)  # get post by id or return 404 error if not found
    if post.author != current_user:  # check if current user is the author of the post
        abort(403)  # return forbidden error if not the author
    db.session.delete(post)  # delete post from database
    db.session.commit()  # commit changes to database
    flash('Your post has been deleted!', 'success')  # flash success message
    return redirect(url_for('home'))  # redirect to home page
