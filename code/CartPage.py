from flask import Blueprint, Flask, render_template, request, jsonify, redirect, url_for
from Models import db, Orders, Cart

cart_layout = Blueprint('cart_layout', __name__)

'''@cart_layout.route("/cart", methods=['POST', 'GET'])
def cart():
    if request.method == 'POST':
        dish_name = request.form.get('dish_name')
        quantity = request.form.get('quantity')
        new_order = Order(dish_name=dish_name, quantity=quantity)
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message': 'Order placed and paid', 'order_id': new_order.id})
    else:
        return render_template("cart.html")'''

@cart_layout.route('/cart')
def view_cart():
    cart_items = Cart.query.all()
    total_price = sum(item.menu_dishes.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)
    return render_template('Cart/cart.html', cart_items=cart_items)

@cart_layout.route('/add_to_cart/<int:dish_id>')
def add_to_cart(dish_id):
    # Check if the item is already in the cart
    existing_item = Cart.query.filter_by(user_id = 1,dish_id=dish_id).first()

    if existing_item:
        existing_item.quantity += 1
    else:
        new_item = Cart(dish_id=dish_id,user_id =1, quantity=1)
        db.session.add(new_item)

    db.session.commit()
    return redirect(url_for('view_cart'))


@cart_layout.route('/remove_from_cart/<int:cart_item_id>')
def remove_from_cart(cart_item_id):
    cart_item = Cart.query.get(cart_item_id)
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
    return redirect(url_for('view_cart'))
