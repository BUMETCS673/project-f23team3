from app import db

Base = db.Model


class Orders(Base):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey('dining_tables.id'))
    customer_id = db.Column(db.Text, db.ForeignKey('customers.id'))
    date = db.Column(db.Text)
    status = db.Column(db.Text)
    payment = db.Column(db.Integer)
    request = db.Column(db.Text)


class Ingredients(Base):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    cost = db.Column(db.REAL)
    expiration_date = db.Column(db.Text)
    quantity_left = db.Column(db.REAL)


class Reviews(Base):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('Order.id'))
    customer_id = db.Column(db.Text, db.ForeignKey('Customer.id'))
    feedback = db.Column(db.Text)


class Customers(Base):
    __tablename__ = 'customers'
    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)


class Compositions(Base):
    __tablename__ = 'compositions'
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)


class Dishes(Base):
    __tablename__ = 'dishes'
    id = db.Column(db.Integer, primary_key=True)
    main_dish_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    cost = db.Column(db.REAL)
    pic_url = db.Column(db.Text)
    num_left = db.Column(db.Integer)


class General_dishes(Base):
    __tablename__ = 'general_dishes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    pic_url = db.Column(db.Text)


class Requests(Base):
    __tablename__ = 'requests'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), primary_key=True)
    quantity = db.Column(db.Integer)
    special_requests = db.Column(db.Text)


class Cart(Base):
    __tablename__ = 'cart'
    user_id = db.Column(db.Integer, db.ForeignKey('customers.id'), primary_key=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), primary_key=True)
    quantity = db.Column(db.Integer)
    special = db.Column(db.Text)


class DiningTables(Base):
    __tablename__ = 'dining_tables'
    id = db.Column(db.Integer, primary_key=True)
    server = db.Column(db.Integer, db.ForeignKey('staff.id'))
    status = db.Column(db.Text)
    capacity = db.Column(db.Integer)


class Staff(Base):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text)
    role = db.Column(db.Text)
    status = db.Column(db.Text)
