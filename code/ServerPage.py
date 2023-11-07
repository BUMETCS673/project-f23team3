from flask import Blueprint, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from Models import db, Staffs
from DBOP import *

server_layout = Blueprint('server_layout', __name__)


@server_layout.route("/server", methods=['POST', 'GET'])
def server():
    if not session['Token']:
        # Not Logged in, return to login page
        return render_template('login.html')
    staff = Staffs.query.filter_by(id=session['ID']).first()
    if not staff:
        # ID not Staff, show customer order
        return render_template('confirm.html')
    else:
        # Get the Newest list of all orders related to that Server ID
        orders_data = get_orders_from_staff(session['ID'])
        return render_template("server.html", orders=orders_data)
