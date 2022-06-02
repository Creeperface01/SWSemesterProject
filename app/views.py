from flask import render_template, flash, redirect, url_for, Response
from flask_login import login_required, current_user, login_user

from app import app
from app.forms import *
from app.models import *

search_form = SearchForm()

login_form = LoginForm()
signup_form = SignUpForm()

current_user: User


@app.route('/')
def home() -> str:
    return render_template('index.html')


@app.route('/search')
def search() -> str:
    return render_template('index.html')


@app.route('/signup')
def signup() -> str:
    return render_template('signup.html')


@app.route('/login', methods=['POST'])
def login() -> str | Response:
    form = LoginForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user is None:
            user = User(
                email=form.email.data,
            )

            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()

            login_user(user)

            return redirect(url_for('home'))

        flash('This email has been already registered by a different user')

    return render_template('signup.html')


@app.route('/logout', methods=['GET'])
def logout() -> Response:
    return redirect('home')


@app.route('/profile')
def profile() -> str:
    return render_template('profile.html')


@app.route('/follow-user/<user_id>')
@login_required
def follow_user(user_id: int) -> Response:
    user: User = User.get(user_id)

    if user is None:
        return Response('Invalid user', status=400)

    if user == current_user:
        return Response('Invalid user', status=400)

    current_user.followees.append(user)

    db.session.commit()


@app.route('/product/new')
@login_required
def add_product():
    return render_template('product.html')


@app.route('/product/edit/<product_id>')
@login_required
def edit_product(product_id: int) -> str | Response:
    product: Product = Product.get(product_id)

    if product is None:
        return Response('Invalid product', status=400)

    if product.user != current_user:
        return Response('Illegal access', status=403)

    return render_template('product.html')
