#!/usr/bin/env python

import os
import json

from flask import Flask
from flask import request

# flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print('Request from Dialogflow:')
    print(json.dumps(req, indent=4))
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    res = request.getresponse()


if __name__ == '__main__':
    # bind to port if defined, otherwise default to 5000
    port = int(os.getenv('PORT', 5000))
    print('Starting Rudy on port %d' % port)
    app.run(debug=False, port=port, host='0.0.0.0')
