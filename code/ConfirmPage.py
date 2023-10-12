from flask import Blueprint, Flask, render_template, url_for

confirm_layout = Blueprint('confirm_layout', __name__)


@confirm_layout.route("/confirm")
def login_account():
    return render_template("confirm.html")