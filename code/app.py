from flask import Flask, render_template, request, session

from flask_sqlalchemy import SQLAlchemy
from Models import db
from LoginPage import login_layout
from RegiserPage import register_layout
from FullMenu import full_menu
from MainMenu import main_menu
from CartPage import cart_layout
from ConfirmPage import confirm_layout


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db.init_app(app)
app.register_blueprint(login_layout)
app.register_blueprint(register_layout)
app.register_blueprint(full_menu)
app.register_blueprint(cart_layout)
app.register_blueprint(confirm_layout)
app.register_blueprint(main_menu)

# isLoggedIn变量，前端脚本会使用这个变量来显示或隐藏购物车链接
@app.route('/')
def home_page():
    is_logged_in = 'user_id' in session  # session来跟踪登录状态
    return render_template('home.html', isLoggedIn=is_logged_in)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
