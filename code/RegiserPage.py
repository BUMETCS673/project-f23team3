from flask import Blueprint, render_template, request, session
import CloudOP

register_layout = Blueprint('register_api', __name__)


@register_layout.route("/register", methods=["GET", "POST"])
def sign_up_page():
    if request.method == "POST":
        # Handle form submission
        email = request.form.get("inputEmail")
        password = request.form.get("inputPassword")
        # Actual Registration are handled in local file CloudOP.py
        try:
            user = CloudOP.register_with_email(email, password)
            session['user'] = user
            return render_template("signup.html", success=True)
        except ValueError as err:
            return render_template("signup.html", success=False, error=err)
    else:
        # Handle initial GET request to render the registration page
        return render_template("signup.html")
