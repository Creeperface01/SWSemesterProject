import json
import os

from flask import render_template, flash, redirect, url_for, Response
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename

from app import app
from app.forms import *
from app.models import *

current_user: User


@app.template_filter('datetime')
def format_datetime(value, date_format: str = "%d %b %Y %I:%M %p") -> str:
    if value is None:
        return ""
    return value.strftime(date_format)


def render_products_listing(products) -> str:
    return render_template('product_listing.html', data=products)


@app.context_processor
def inject_global_variables():
    return dict(
        login_form=LoginForm(),
        search_form=SearchForm(),
        render_products_listing=render_products_listing,
    )


@app.route('/')
def home() -> str:
    return render_template('homepage.html', products=Product.query.all())


@app.route('/search')
def search() -> str:
    return render_template('searchresult.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup() -> str | Response:
    form = SignUpForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user is None:
            user = User(
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
            )

            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()

            login_user(user)

            flash('You have been successfully registered', 'success')
            return redirect(url_for('home'))

        flash('This email has been already registered by a different user', 'danger')

    return render_template('signup.html', form=form)


@app.route('/login', methods=['POST'])
def login() -> Response:
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(password=form.password.data):
            login_user(user)
            flash('You have been successfully logged in', 'success')
            return redirect(url_for('home'))

    flash('Incorrect username or password', 'danger')
    return redirect(url_for('home'))


@app.route('/logout', methods=['GET'])
@login_required
def logout() -> Response:
    logout_user()
    flash('You have been successfully logged out', 'success')
    return redirect(url_for('home'))


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


@app.route('/product/new', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()

    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            user=current_user
        )

        for file in form.images.data:
            filename = secure_filename(file.filename)

            file.save(
                os.path.join(app.config['UPLOAD_FOLDER'], filename)
            )

            product_image = ProductImage()
            product_image.path = filename

            product.images.append(product_image)

        keywords = json.loads(form.keywords.data)

        for kw in keywords:
            keyword = Keyword.query.filter(Keyword.name == kw['value']).first()

            if keyword is None:
                keyword = Keyword()
                keyword.name = kw['value']

            product.keywords.append(keyword)

        db.session.add(product)
        db.session.commit()

        flash('Product has been published', 'success')

    return render_template('product.html', form=form)


@app.route('/product/<product_id>')
def product_show(product_id: int) -> str | Response:
    product: Product = Product.query.get(product_id)

    if product is None:
        return Response('Invalid product', status=400)

    return render_template('product_show.html', product=product)


@app.route('/product/edit/<product_id>')
@login_required
def edit_product(product_id: int) -> str | Response:
    product: Product = Product.query.get(product_id)

    if product is None:
        return Response('Invalid product', status=400)

    if product.user != current_user:
        return Response('Access denied', status=403)

    return render_template('product.html')


@app.route('/product/sell/<product_id>')
@login_required
def sell_product(product_id: int) -> Response:
    product: Product = Product.query.get(product_id)

    if product is None:
        return Response('Invalid product', status=400)

    if product.user != current_user:
        return Response('Access denied', status=403)

    product.sold = True
    db.session.commit()

    return redirect(url_for('product_show', product_id=product_id))


@app.route('/product/delete/<product_id>')
@login_required
def delete_product(product_id: int) -> Response:
    product: Product = Product.query.get(product_id)

    if product is None:
        return Response('Invalid product', status=400)

    if product.user != current_user:
        return Response('Access denied', status=403)

    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('product_show', product_id=product_id))
