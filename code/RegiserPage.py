from flask import Blueprint

register_api = Blueprint('register_api', __name__)


@register_api.route("/register")
def create_account():
    return "Register an account"
