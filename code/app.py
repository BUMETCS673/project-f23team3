from flask import Flask
from LoginPage import login_api
from RegiserPage import register_api

app = Flask(__name__)
app.register_blueprint(login_api)
app.register_blueprint(register_api)


@app.route("/")
def hello():
    return "Home Page!"


if __name__ == "__main__":
    app.run()
