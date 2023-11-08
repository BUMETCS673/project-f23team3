import pyrebase, requests, json
from Config import firebase_config as config

# Initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


def register_with_email(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        return user
    except requests.exceptions.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        raise ValueError(error) from None


def login_with_email(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except requests.exceptions.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        print(error)
        raise ValueError(error) from None
