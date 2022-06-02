from flask import Response, redirect, url_for

from app import login_manager
from app.models import *


@login_manager.user_loader
def load_user(user_id: int | None) -> User | None:
    if user_id is not None:
        return User.query.get(user_id)

    return None


@login_manager.unauthorized_handler
def unauthorized() -> Response:
    return redirect(url_for('home'))
