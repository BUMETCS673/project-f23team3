from flask import Blueprint, render_template, redirect, url_for, session,jsonify
from Models import db, Cart

cart_service = Blueprint('cart_service', __name__)
def calculate_cart_total(user_id):
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    total_price = sum(item.menu_dishes.price * item.quantity for item in cart_items)
    return  total_price


@cart_service.route('/add_to_cart/<int:dish_id>')
def add_to_cart(dish_id):
    user_id = 1
    existing_item = Cart.query.filter_by(user_id=user_id, dish_id=dish_id).first()

    if existing_item:
        existing_item.quantity += 1
    else:
        new_item = Cart(dish_id=dish_id, user_id=user_id, quantity=1)
        db.session.add(new_item)

    db.session.commit()

    return jsonify({'success': True})

@cart_service.route('/get_cart_total/<int:user_id>')
def get_cart_total(user_id):
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    cart_total = sum(5 * item.quantity for item in cart_items) #item.menu_dishes.price
    return jsonify(cart_total=cart_total)


@cart_service.route('/cart')
def view_cart():
    cart_items = Cart.query.all()
    #total_price = sum(item.menu_dishes.price * item.quantity for item in cart_items)
   # return render_template('cart.html', cart_items=cart_items, total_price=total_price)
    return render_template('Cart/cart.html', cart_items=cart_items)


@cart_service.route('/remove_from_cart/<int:cart_item_id>')
def remove_from_cart(cart_item_id):
    cart_item = Cart.query.get(cart_item_id)
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
    return redirect(url_for('view_cart'))
