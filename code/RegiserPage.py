from flask import Blueprint, Flask, render_template, url_for, request
import firesecure

register_layout = Blueprint('register_api', __name__)


@register_layout.route("/register", methods=["GET", "POST"])
def sign_up_page():
    if request.method == "POST":
        # Handle form submission
        email = request.form.get("inputEmail")
        password = request.form.get("inputPassword")
        print(email)
        print(password)
        # Actual Registration are handled in local file firesecure.py
        try:
            firesecure.register_with_email(email, password)
            return render_template("signup.html", success=True)
        except ValueError as err:
            return render_template("signup.html", success=False, error=err)
    else:
        # Handle initial GET request to render the registration page
        return render_template("signup.html")
