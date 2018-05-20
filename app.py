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
    print(app.config.from_envvar('type'))


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0,0,0,0')
