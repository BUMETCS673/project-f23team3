from flask import Blueprint

cart_layout = Blueprint('cart_layout', __name__)


@cart_layout.route("/cart")
def list_menu():
    return "List out the cart."
