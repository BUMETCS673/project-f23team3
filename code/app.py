from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os
#import test


app = Flask(__name__)
# Generate a random secret key
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
    #test.TestCartFunctionality()
app.config.from_object(__name__)

# Do not edit the below import, it is by design.
import views

