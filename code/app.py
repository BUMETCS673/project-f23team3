from flask import Flask, render_template, request
from Models import db
from LoginPage import login_layout
from RegiserPage import register_layout
from Menu_Dishes import menu_dishes
from Menu_MainDishes import main_dishes
from CartPage import cart_layout
from ConfirmPage import confirm_layout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db.init_app(app)
app.register_blueprint(login_layout)
app.register_blueprint(register_layout)
app.register_blueprint(menu_dishes)
app.register_blueprint(cart_layout)
app.register_blueprint(confirm_layout)
app.register_blueprint(main_dishes)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
