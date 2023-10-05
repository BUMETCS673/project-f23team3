from flask import Flask
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

@app.route("/")
def hello():
    return "Home Page!"


if __name__ == "__main__":
    app.run()
