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
    req = request.get_json(silent=True, force=True)
    print('Request from client:')
    print(json.dumps(req, indent=4))
    print(app.config.from_envvar('type'))
    return make_response(req)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0,0,0,0')
