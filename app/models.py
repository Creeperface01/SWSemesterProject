from __future__ import annotations

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

product_keywords = db.Table(
    "product_keywords",
    db.Column("product_id", db.ForeignKey("product.id"), nullable=False),
    db.Column("keyword_id", db.ForeignKey("keyword.id"), nullable=False),

    db.UniqueConstraint('product_id', 'keyword_id', name='product_keyword_unique'),
)

user_follows = db.Table(
    "user_follows",
    db.Column("user_id", db.ForeignKey("user.id"), nullable=False),
    db.Column("followee_id", db.ForeignKey("user.id"), nullable=False),

    db.UniqueConstraint('user_id', 'followee_id', name='user_followee_unique'),
)


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)

    email = db.Column(db.String(256))
    password = db.Column(db.String(256))

    products = db.relationship('Product', backref='user', lazy='dynamic')

    followees = db.relationship(
        'User',
        secondary=user_follows,
        lazy='dynamic',
        primaryjoin=user_follows.c.user_id == id,
        secondaryjoin=user_follows.c.followee_id == id,
        backref='followers'
    )

    def set_password(self, password):
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Keyword(db.Model):
    __tablename__ = 'keyword'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)

    name = db.Column(db.String(256), nullable=False)

    products = db.relationship(
        'Product',
        secondary=product_keywords,
        lazy='dynamic',
        backref=db.backref('keyword', lazy='dynamic')
    )


class ProductImage(db.Model):
    __tablename__ = 'product_image'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product: Product

    path = db.Column(db.String(256))


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user: User

    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text())
    sold = db.Column(db.Boolean(), nullable=False, default=False)

    images = db.relationship('ProductImage', backref='product', lazy='dynamic')

    keywords = db.relationship(
        'Keyword',
        secondary=product_keywords,
        lazy='dynamic',
        backref=db.backref('product', lazy='dynamic')
    )
