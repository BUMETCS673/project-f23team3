from flask import Blueprint

login_api = Blueprint('login_api', __name__)


@login_api.route("/login")
def login_account():
    return "Log into account"
