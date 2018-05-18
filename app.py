#!/usr/bin/env python

import json
import os

from flask import Flask
from flask import jsonify
from flask import request

# Flask app should start in global layout
app = Flask(__name__)

base_response = {
    'speech': "sample response",

    'source': 'Manual'}


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print('Request from Dialogflow:')
    print(json.dumps(req, indent=4))
    req_body = request.get_json()
    print(req_body)
    response = base_response.copy()
    return jsonify(response)


if __name__ == '__main__':
    # bind to port if defined, otherwise default to 5000
    port = int(os.getenv('PORT', 5000))
    print('Starting Rudy on port %d' % port)
    app.run(debug=False, port=port, host='0.0.0.0')
