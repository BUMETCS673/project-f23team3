from flask import Blueprint, render_template, request, session
import CloudOP
import DataOP

login_layout = Blueprint('login_api', __name__)


@login_layout.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        # Handle form submission
        email = request.form.get("inputEmail")
        password = request.form.get("inputPassword")
        # Actual login are handled in local file CloudOP.py
        try:
            user = CloudOP.login_with_email(email, password)
            session['user'] = user
            if DataOP.is_staff(user['localId']):
                return render_template('staff.html', name=DataOP.find_name_from_id(user['localId']))
            return render_template("login.html", success=True)
        except ValueError as err:
            return render_template("login.html", success=False, error=err)
    else:
        # Handle GET request to render the login page
        try:
            user_id = session['user']['localId']
        except KeyError:
            # User Not Logged in
            return render_template("login.html")
        name = DataOP.find_name_from_id(user_id)
        err = "You are Logged in as " + name + " already."
        if DataOP.is_staff(user_id):
            return render_template('staff.html', name=DataOP.find_name_from_id(user_id))
        return render_template("login.html", success=False, error=err)
