from flask import Blueprint, Flask, render_template, request, jsonify
from Models import db, Orders

cart_layout = Blueprint('cart_layout', __name__)


@cart_layout.route("/cart", methods=['POST', 'GET'])
def cart():
    if request.method == 'POST':
        dish_name = request.form.get('dish_name')
        quantity = request.form.get('quantity')
        new_order = Orders(dish_name=dish_name, quantity=quantity)
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message': 'Order placed and paid', 'order_id': new_order.id})
    else:
        return render_template("cart.html")

@cart_layout.route("/cart/order", methods=['POST', 'GET'])
def cart_order():
    if request.method == 'POST':
        return jsonify({'message': 'Order placed'})
    else:
        return render_template("cart.html")