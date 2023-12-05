from Models import *


def get_orders_from_staff(staff_id):
    # Find all dining tables served by the given staff member
    tables_served = DiningTable.query.filter_by(server=staff_id).all()

    table_ids = [table.id for table in tables_served]

    orders = Order.query.filter(Order.table_id.in_(table_ids)).all()

    return orders


def find_name_from_id(user_id):
    # Check if the id is in the Customers table
    customer = Customer.query.filter_by(id=user_id).first()
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
    order = Order.query.get(order_id)
    if order:
        table_id = order.table_id
        dining_table = DiningTable.query.get(table_id)
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
    work = DiningTable.query.filter_by(server=user_id)
    if work is None:
        # Staff not working on any table, show customer order
        return False
    return True


def clear_cart(table_id):
    # Query the Cart model for items with the specified table_id
    carts = Cart.query.filter_by(table_id=table_id).all()

    # Iterate over the queried items and delete each one
    for cart in carts:
        db.session.delete(cart)

    # Commit the changes to the database
    db.session.commit()


def lookup_table_id(order_id):
    # Query the Order model for the specified order_id
    order = Order.query.get(order_id)

    # Check if the order exists
    if order is not None:
        # Query the Party model for the customer_id associated with the order
        party = Party.query.filter_by(customer_id=order.customer_id).first()

        # Check if the party exists
        if party is not None:
            return party.table_id
        else:
            # Party not found
            return False
    else:
        # Order not Found
        return False


def clear_party(table_id):
    parties = Party.query.filter_by(table_id=table_id).all()

    # Iterate over the queried items and delete each one
    for party in parties:
        db.session.delete(party)

    # Commit the changes to the database
    db.session.commit()


def join_party(user_id, table_id, passphrase):
    dining_table = DiningTable.query.filter_by(id=table_id, passphrase=passphrase).first()
    if dining_table is not None:
        # Create a new Party entry with the user_id and table_id
        new_party = Party(table_id=table_id, customer_id=user_id)

        db.session.add(new_party)
        db.session.commit()

        return True
    else:
        return False


def get_cart_total(table_id):
    carts = Cart.query.filter_by(table_id=table_id).all()
    if carts is None:
        return 0
    # Calculate the total cost
    total_cost = sum([Dish.query.get(cart.dish_id).cost * cart.quantity for cart in carts])

    return total_cost


def party_check(user_id):
    # Query the Party model for the specified user_id
    party = Party.query.filter_by(customer_id=user_id).first()

    # Check if the user is in a table
    if party is not None:
        return True
    else:
        return False

