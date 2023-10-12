from flask import Blueprint, Flask, render_template, url_for

cart_layout = Blueprint('cart_layout', __name__)


@cart_layout.route("/cart")
def list_menu():
    return render_template("cart.html")
