from app import db

Base = db.Model


class Order(Base):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey('dining_tables.id'))
    date = db.Column(db.Text)
    status = db.Column(db.Text)
    total = db.Column(db.Integer)
    request = db.Column(db.Text)


class Party(Base):
    __tablename__ = 'parties'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    customer_id = db.Column(db.Text, db.ForeignKey('customers.id'), primary_key=True)


class Cart(Base):
    __tablename__ = 'carts'
    table_id = db.Column(db.Integer, db.ForeignKey('dining_tables.id'), primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), primary_key=True)
    quantity = db.Column(db.Integer)
    special = db.Column(db.Text)


class Reviews(Base):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('Order.id'))
    customer_id = db.Column(db.Text, db.ForeignKey('Customer.id'))
    feedback = db.Column(db.Text)


class Customer(Base):
    __tablename__ = 'customers'
    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)


class Composition(Base):
    __tablename__ = 'compositions'
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)


class Dish(Base):
    __tablename__ = 'dishes'
    id = db.Column(db.Integer, primary_key=True)
    general_dish_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    cost = db.Column(db.REAL)
    pic_url = db.Column(db.Text)
    num_left = db.Column(db.Integer)


class DishType(Base):
    __tablename__ = 'dish_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    pic_url = db.Column(db.Text)


class Requests(Base):
    __tablename__ = 'requests'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), primary_key=True)
    quantity = db.Column(db.Integer)
    special = db.Column(db.Text)


class DiningTable(Base):
    __tablename__ = 'dining_tables'
    id = db.Column(db.Integer, primary_key=True)
    server = db.Column(db.Integer, db.ForeignKey('staff.id'))
    status = db.Column(db.Text)
    capacity = db.Column(db.Integer)


class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    cost = db.Column(db.REAL)
    expiration_date = db.Column(db.Text)
    quantity_left = db.Column(db.REAL)


class Staff(Base):
    __tablename__ = 'staffs'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text)
    role = db.Column(db.Text)
    status = db.Column(db.Text)
