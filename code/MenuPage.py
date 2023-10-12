from flask import Blueprint, Flask, render_template, url_for

menu_layout = Blueprint('menu_layout', __name__)


@menu_layout.route("/menu")
def list_menu():
    return render_template("menu.html")
