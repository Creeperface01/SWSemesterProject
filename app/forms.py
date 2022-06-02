from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
)


class SignUpForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            Email(message='Enter a valid email.'),
            DataRequired()
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8, message='Password must contain at least 8 characters')
        ]
    )

    password2 = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Entered wrong password')
        ]
    )

    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired()
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
        ]
    )

    submit = SubmitField('Login')


class SearchForm(FlaskForm):
    query = StringField(
        'Query',
        validators=[
            DataRequired(),
        ]
    )

    submit = SubmitField('Search')


images = UploadSet('images', IMAGES)


class ProductForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=8, message='Product name must be at least 8 characters long')
        ]
    )

    description = TextAreaField(
        'Description',
        validators=[
            DataRequired(),
            Length(min=50, message='Describe your product by at least 50 characters')
        ]
    )

    images = FileField(
        'Images',
        validators=[
            DataRequired(),
            FileRequired(),
            FileAllowed(images, 'Only image formats are allowed')
        ]
    )

    keywords = StringField(
        'Kexwords',
        validators=[
            DataRequired(),
        ]
    )