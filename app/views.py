from flask import render_template

from app import app


@app.route('/')
def home() -> str:
    return render_template('index.html')
