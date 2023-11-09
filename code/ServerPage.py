from flask import Blueprint, render_template, session, redirect
from sqlalchemy import event
from Models import *
from DataOP import *

server_layout = Blueprint('server_layout', __name__)


def refresh_orders(mapper, connection, target):
    try:
        user_id = session['user']['localId']
    except KeyError:
        # User Not Logged in, or expired, in this situation
        return redirect('/login')
    if active_worker(user_id):
        orders_data = get_orders_from_staff(session['user']['localId'])
        return render_template("server.html", orders=orders_data)


event.listen(Orders, 'after_insert', refresh_orders)


@server_layout.route("/server", methods=['POST', 'GET'])
def server():
    try:
        user_id = session['user']['localId']
    except KeyError:
        # User Not Logged in
        return redirect('/login')
    if active_worker(user_id):
        # Get the Newest list of all orders related to that Server ID
        orders_data = get_orders_from_staff(user_id)
        return render_template("server.html", orders=orders_data, name=find_name_from_id(user_id))
    else:
        # Not worker or not on duty (include manager and kitchen), return to order page.
        return render_template('staff.html', name=find_name_from_id(user_id))


@server_layout.route('/completed-orders')
def completed_orders():
    completed_orders = Orders.query.filter_by(status='completed').all()
    return render_template('completed_orders.html', orders=completed_orders)
# list all the completed orders