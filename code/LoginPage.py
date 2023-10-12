from flask import Blueprint, Flask, render_template, url_for

login_layout = Blueprint('login_api', __name__)


@login_layout.route("/login")
def sign_up_page():
    return render_template("login.html")
