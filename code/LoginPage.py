from flask import Blueprint

login_layout = Blueprint('login_api', __name__)


@login_layout.route("/login")
def login_account():
    return "Log into account"
