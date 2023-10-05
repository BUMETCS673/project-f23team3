from flask import Blueprint

register_layout = Blueprint('register_api', __name__)


@register_layout.route("/register")
def create_account():
    return "Register an account"
