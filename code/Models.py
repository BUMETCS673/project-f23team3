from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Base = db.Model


class Orders(Base):
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Text, db.ForeignKey('DiningTable.id'))
    customer_id = db.Column(db.Text, db.ForeignKey('Customer.id'))
    date = db.Column(db.Text)
    status = db.Column(db.Text)
    payment = db.Column(db.Integer)
    request = db.Column(db.Text)


class Ingredients(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    cost = db.Column(db.REAL)
    expiration_date = db.Column(db.Text)
    quantity_left = db.Column(db.REAL)


class Reviews(Base):
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('Order.id'))
    customer_id = db.Column(db.Text, db.ForeignKey('Customer.id'))
    feedback = db.Column(db.Text)


class Customers(Base):
    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)


class Compositions(Base):
    dish_id = db.Column(db.Integer, db.ForeignKey('Dish.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('Ingredient.id'), primary_key=True)


class Dish_Label(Base):
    dish_id = db.Column(db.Integer, db.ForeignKey('Dish.id'), primary_key=True)
    label = db.Column(db.Text, primary_key=True)


class Menu_dishes(Base):
    id = db.Column(db.Integer, primary_key=True)
    main_dish_id = db.Column(db.Integer, db.ForeignKey('Menu_main_dishes.id'))
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    cost = db.Column(db.REAL)
    pic_url = db.Column(db.Text)
    num_left = db.Column(db.Integer)


class Menu_main_dishes(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    pic_url = db.Column(db.Text)


class Requests(Base):
    order_id = db.Column(db.Integer, db.ForeignKey('Order.id'), primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('Dish.id'), primary_key=True)
    quantity = db.Column(db.Integer)
    special_requests = db.Column(db.Text)


class Cart(Base):
    user_id = db.Column(db.Text, db.ForeignKey('Customer.id'), primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('Dish.id'), primary_key=True)
    quantity = db.Column(db.Integer)
    special_requests = db.Column(db.Text)


class Dining_tables(Base):
    id = db.Column(db.Integer, primary_key=True)
    server = db.Column(db.Text, db.ForeignKey('Staff.id'))
    status = db.Column(db.Text)
    capacity = db.Column(db.Integer)


class Staffs(Base):
    id = db.Column(db.Text, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text)
    role = db.Column(db.Text)
    status = db.Column(db.Text)
