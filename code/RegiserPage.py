from flask import Blueprint, Flask, render_template, url_for

register_layout = Blueprint('register_api', __name__)


@register_layout.route("/register")
def sign_up_page():
    return render_template("signup.html")
