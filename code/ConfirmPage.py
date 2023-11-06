from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
confirm_layout = Blueprint('confirm_layout', __name__)


@confirm_layout.route("/confirm")
def login_account():
    return "Confirm the order and transfer back to the database."


app = Flask(__name__)
# Configure the database URI of the application to specify the use of SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
# Initialize an SQLAlchemy instance that is associated with the previously created Flask application
db = SQLAlchemy(app)


class Order(db.Model):
    # Define a column named 'id' to be used as the primary key
    id = db.Column(db.Integer, primary_key=True)
    # Define a column called 'dish_name' with a maximum length of 100
    dish_name = db.Column(db.String(100))
    # Define a column called 'quantity',which is an integer column that stores the number of items in the order
    quantity = db.Column(db.Integer)
    # Define a column named 'status' with a maximum length of 100
    # If the status is not explicitly specified when creating a new order, the default value is "Pending"
    status = db.Column(db.String(100), default="Pending")


@app.route('/')
def index():
    # Use Flask's render_template function to render an HTML template named 'order_confirm.html'
    # When this view function is called, it returns the contents of the HTML template
    return render_template('order_confirm.html')


@app.route('/submit_order', methods=['POST'])
def submit_order():
    # Get the form data from the request and extract the values for the 'dish_name' and 'quantity' fields
    dish_name = request.form.get('dish_name')
    quantity = request.form.get('quantity')
    # Create a new Order object using the extracted data
    new_order = Order(dish_name=dish_name, quantity=quantity)
    # Adds the newly created Order object to the database session
    db.session.add(new_order)
    # Submit session to save the new Order object to the database
    db.session.commit()
    # Returns a JSON response containing a message about the order and the ID of the newly created order
    return jsonify({'message': 'Order placed and paid', 'order_id': new_order.id})


@app.route('/home')
def home():
    # Use Flask's render_template function to render an HTML template called 'HomePage.html'
    # When this view function is called, it returns the contents of the HTML template
    return render_template('HomePage.html')


if __name__ == '__main__':
    # Use the context of the application to ensure that we can access and manipulate the database
    with app.app_context():
      # Use SQLAlchemy's create_all method to create all uncreated database tables
       db.create_all()
    # Start the Flask app
    # Any code changes will cause the app to reload automatically, and errors will show details
    app.run(debug=True)
