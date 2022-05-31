from flask import render_template

from app import app


@app.route('/')
def home() -> str:
    return render_template('index.html')


@app.route('/signup')
def signup() -> str:
    return render_template('signup.html')


@app.route('/profile')
def profile() -> str:
    return render_template('profile.html')