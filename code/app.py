from flask import Flask, render_template, redirect, session
from datetime import timedelta
from Models import db
from LoginPage import login_layout
from RegiserPage import register_layout
from FullMenu import full_menu
from MainMenu import main_menu
from CartPage import cart_layout
from ConfirmPage import confirm_layout
from ServerPage import server_layout
import os


app = Flask(__name__)
# Generate a random secret key
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
db.init_app(app)
app.register_blueprint(login_layout)
app.register_blueprint(register_layout)
app.register_blueprint(full_menu)
app.register_blueprint(cart_layout)
app.register_blueprint(confirm_layout)
app.register_blueprint(main_menu)
app.register_blueprint(server_layout)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
