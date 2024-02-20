from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

# define a form for user registration
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])  # input for username
    email = StringField('Email',
                        validators=[DataRequired(), Email()])  #input for email
    password = PasswordField('Password', validators=[DataRequired()])  # input for password
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])  # confirm password input
    submit = SubmitField('Sign Up')  # submit button

    # validate if username already exists
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()  # query user by username
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')  # raise error if username taken

    # validate if email already exists
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()  # query user by email
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')  # raise error if email taken

# define a form for user login
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])  # input for email
    password = PasswordField('Password', validators=[DataRequired()])  # input for password
    remember = BooleanField('Remember Me')  # checkbox for remember me
    submit = SubmitField('Login')  # submit button

# define a form for updating account information
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])  # input for new username
    email = StringField('Email',
                        validators=[DataRequired(), Email()])  # input for new email
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])  # input for profile picture
    submit = SubmitField('Update')  # submit button

    # validate if the new username is already taken by another user
    def validate_username(self, username):
        if username.data != current_user.username:  # check if username has been changed
            user = User.query.filter_by(username=username.data).first()  # query user by new username
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')  # raise error if username taken

    # validate if the new email is already taken by another user
    def validate_email(self, email):
        if email.data != current_user.email:  # check if email has been changed
            user = User.query.filter_by(email=email.data).first()  # query user by new email
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')  # raise error if email taken
            
# define a form for creating a new post
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])  # input for post title
    content = TextAreaField('Content', validators=[DataRequired()])  # textarea for post content
    submit = SubmitField('Post')  # submit button
