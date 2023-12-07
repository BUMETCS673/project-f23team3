from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)
# Generate a random secret key
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
app.config.from_object(__name__)


# Do not edit the below import, it is by design.
import views


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
    socketio.run(app)
