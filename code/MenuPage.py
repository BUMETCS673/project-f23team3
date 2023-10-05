from flask import Blueprint

menu_layout = Blueprint('menu_layout', __name__)


@menu_layout.route("/menu")
def list_menu():
    return "List out the menu."
