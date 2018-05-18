#!/usr/bin/env python

import os
import json

from flask import Flask
from flask import request
from flask import make_response

# flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)
	r = make_response(req)
	return r


if __name__ == '__main__':
    # bind to PORT if defined, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    print('Starting Rudy on port %d' % port)
    app.run(host='0,0,0,0', port=port)
