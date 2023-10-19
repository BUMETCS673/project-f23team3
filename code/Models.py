from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dish_name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    status = db.Column(db.String(100), default="Pending")


class MainMenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    full_menus = db.relationship('FullMenu', backref='main_menu', lazy='dynamic')


class FullMenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_menu_id = db.Column(db.Integer, db.ForeignKey('main_menu.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)

