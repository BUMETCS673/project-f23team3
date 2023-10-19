from flask import Blueprint, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import db

confirm_layout = Blueprint('confirm_layout', __name__)


@confirm_layout.route('/confirm')
def index():
    return render_template('confirm.html')
