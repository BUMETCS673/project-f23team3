import requests
from Config import firebase_config as config


def firebase_request(url, email, password):
    data = {
        'email': email,
        'password': password,
        'returnSecureToken': True
    }
    response = requests.post(url, data=data)
    if response.ok:
        return response.json()
    else:
        # Handle error if response is not ok
        error = response.json()['error']['message']
        print(error)
        raise ValueError(error) from None


def register_with_email(email, password):
    url = 'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=' + config["apiKey"]
    return firebase_request(url, email, password)


def login_with_email(email, password):
    url = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=' + config["apiKey"]
    return firebase_request(url, email, password)
