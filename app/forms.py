from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, FieldList, IntegerField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange
)


class SignUpForm(FlaskForm):
    first_name = StringField(
        'First name',
        validators=[
            DataRequired()
        ]
    )

    last_name = StringField(
        'Last name',
        validators=[
            DataRequired()
        ]
    )

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
            DataRequired()
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

    price = IntegerField(
        'Price',
        validators=[
            NumberRange(min=1)
        ]
    )

    description = TextAreaField(
        'Description',
        validators=[
            DataRequired(),
            Length(min=50, message='Describe your product by at least 50 characters')
        ]
    )

    images = FieldList(
        FileField(
            'Image',
            validators=[
                # DataRequired(),
                FileAllowed(images, 'Only image formats are allowed')
            ],
            # render_kw={'multiple': True}
        ),
        min_entries=1
    )

    keywords = StringField(
        'Keywords',
        validators=[
            DataRequired(),
        ]
    )

    submit = SubmitField('Add new product')
