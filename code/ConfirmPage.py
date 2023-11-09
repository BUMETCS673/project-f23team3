from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from Models import *

confirm_layout = Blueprint('confirm_layout', __name__)


@confirm_layout.route("/confirm", methods=['GET', 'POST'])
def confirm_page():
    if request.method == "POST":
        # Get the form data from the request
        dish_name = request.form.get('dish_name')
        quantity = request.form.get('quantity')
        # Create a new Order object using the extracted data
        new_order = Orders(dish_name=dish_name, quantity=quantity)
        # Adds the newly created Order object to the database session
        db.session.add(new_order)
        # Submit session to save the new Order object to the database
        db.session.commit()
        # Returns a JSON response containing a message about the order and the ID of the newly created order
        return jsonify({'message': 'Order placed and paid', 'order_id': new_order.id})
    else:
        return render_template('order_confirm.html')

