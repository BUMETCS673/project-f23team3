from flask import Blueprint

confirm_layout = Blueprint('confirm_layout', __name__)


@confirm_layout.route("/confirm")
def login_account():
    return "Confirm the order and transfer back to the database."
