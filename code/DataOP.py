from Models import *


def get_orders_from_staff(staff_id):
    # Find all dining tables served by the given staff member
    tables_served = DiningTables.query.filter_by(server=staff_id).all()

    table_ids = [table.id for table in tables_served]

    orders = Orders.query.filter(Orders.table_id.in_(table_ids)).all()

    return orders


def find_name_from_id(user_id):
    # Check if the id is in the Customers table
    customer = Customers.query.filter_by(id=user_id).first()
    if customer:
        return customer.preferred_name
    # Check if the id is in the Staffs table
    staff = Staff.query.filter_by(id=user_id).first()
    if staff:
        return staff.first_name + " " + staff.last_name
    # If the id is not found in either table, return None
    return None


def find_requests_from_order_id(order_id):
    # Query the Requests table for all requests with the given order_id
    requests = Requests.query.filter_by(order_id=order_id).all()
    # Return a list of requests
    return requests


def get_staff_from_order(order_id):
    order = Orders.query.get(order_id)
    if order:
        table_id = order.table_id
        dining_table = DiningTables.query.get(table_id)
        if dining_table:
            return dining_table.server
    return None


def is_staff(user_id):
    # Check if ID is Staff or not, return is first row.
    staff = Staff.query.filter_by(id=user_id).first()
    if staff is None:
        # ID not Staff, show customer order
        return False
    return True


def active_worker(user_id):
    # Check if ID is Staff or not, return is first row.
    staff = Staff.query.filter_by(id=user_id).first()
    if staff is None:
        # ID not Staff, show customer order
        return False
    work = DiningTables.query.filter_by(server=user_id)
    if work is None:
        # Staff not working on any table, show customer order
        return False
    return True
