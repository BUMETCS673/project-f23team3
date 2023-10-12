from flask import Blueprint, Flask, render_template, url_for
import flask_sqlalchemy as alchemy
from LoginPage import login_layout
from RegiserPage import register_layout
from MenuPage import menu_layout
from CartPage import cart_layout
from ConfirmPage import confirm_layout


app = Flask(__name__)
app.register_blueprint(login_layout)
app.register_blueprint(register_layout)
app.register_blueprint(menu_layout)
app.register_blueprint(cart_layout)
app.register_blueprint(confirm_layout)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
