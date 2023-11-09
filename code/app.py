from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from Models import db
from LoginPage import login_layout
from RegiserPage import register_layout
from FullMenu import full_menu
from MainMenu import main_menu
from CartPage import cart_layout
from ConfirmPage import confirm_layout
from OrderPage import order_layout


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db.init_app(app)
app.register_blueprint(login_layout)
app.register_blueprint(register_layout)
app.register_blueprint(full_menu)
app.register_blueprint(cart_layout)
app.register_blueprint(confirm_layout)
app.register_blueprint(main_menu)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
