from flask import Blueprint, Flask, render_template, url_for, request
import firesecure

login_layout = Blueprint('login_api', __name__)


@login_layout.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        # Handle form submission
        email = request.form.get("inputEmail")
        password = request.form.get("inputPassword")
        # Actual Registration are handled in local file firesecure.py
        try:
            user = firesecure.login_with_email(email, password)
            return render_template("login.html", success=True)
        except ValueError as err:
            return render_template("login.html", success=False, error=err)
    else:
        # Handle initial GET request to render the registration page
        return render_template("login.html")
