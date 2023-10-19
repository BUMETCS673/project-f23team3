from flask import Blueprint, Flask, render_template, url_for, request

cart_layout = Blueprint('cart_layout', __name__)


@cart_layout.route("/cart", methods=['POST', 'GET'])
def list_menu():
    return render_template("cart.html")
