#!/usr/bin/env python

import os
import json
import firebase_admin

from firebase_admin import credentials
from firebase_admin import db
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    cred = credentials.Certificate(key=authenticate())
    firebase = firebase_admin.initialize_app(cred, {'databaseURL': 'https://rudy-b5e54.firebaseio.com'})

    req = request.get_json(silent=True, force=True)
    print('Request from client:')
    print(json.dumps(req, indent=4))

    print(db.reference('degrees').child('Bachelor of Applied Science').get())

    return make_response(req)


def authenticate():
    key = {'type': os.environ['type'],
           'project_id': os.environ['project_id'],
           'private_key_id': os.environ['private_key_id'],
           'private_key': os.environ['private_key'],
           'client_email': os.environ['client_email'],
           'client_id': os.environ['client_id'],
           'auth_uri': os.environ['auth_uri'],
           'token_uri': os.environ['token_uri'],
           'auth_provider_x509_cert_url': os.environ['auth_provider_x509_cert_url'],
           'client_x509_cert_url': os.environ['client_x509_cert_url']}
    return key


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
