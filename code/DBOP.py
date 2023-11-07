from Models import *
from flask import jsonify


def get_orders_from_staff(staff_id):
    # Find all dining tables served by the given staff member
    tables_served = Dining_tables.query.filter_by(server_id=staff_id).all()

    table_ids = [table.id for table in tables_served]

    orders = Orders.query.filter(Orders.table_id.in_(table_ids)).all()

    # Format the orders for JSON response
    orders_data = [{
        'order_id': order.id,
        'table_id': order.table_id,
        'customer_id': order.customer_id,
        'date': order.date,
        'status': order.status,
        'payment': order.payment,
        'requests': order.requests
    } for order in orders]

    return jsonify(orders_data)

