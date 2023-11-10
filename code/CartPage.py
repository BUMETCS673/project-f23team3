from flask import Blueprint, Flask, render_template, request, jsonify
from Models import db, Orders, Cart, Dishes

cart_layout = Blueprint('cart_layout', __name__)

#TODO: get user ID
uid = 1

@cart_layout.route("/cart", methods=['POST', 'GET'])
def cart():
    if request.method == 'POST':
        dish_name = request.form.get('dish_name')
        quantity = request.form.get('quantity')
        new_order = Cart(user_id=uid, dish_id=int(dish_name), quantity=quantity, special=" ")
        db.session.add(new_order)
        db.session.commit()
        return render_template("cart.html")
        #return jsonify({'message': 'Order placed and paid', 'order_id': new_order.dish_id})
    else:
        cart_items = Cart.query.filter_by(user_id=uid).all()
        return render_template("cart.html", cart_items=cart_items)
        #return render_template("cart.html")

@cart_layout.route("/cart/order", methods=['POST', 'GET'])
def cart_order():
    if request.method == 'POST':
        return jsonify({'message': 'Order placed'})
    else:
        return render_template("cart.html")

@cart_layout.route('/cart/delete/<int:id>')
def delete(id):
    item = Cart.query.filter_by(dish_id=id, user_id=uid).first()
    db.session.delete(item)
    db.session.commit()
    return render_template("cart.html")
