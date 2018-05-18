#!/usr/bin/env python

import os
import json

from flask import Flask, jsonify, request

# Flask app should start in global layout
app = Flask(__name__)

base_response = {
    'fulfillmentText': "sample response",
}


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print('Request from Dialogflow:')
    print(json.dumps(req, indent=4))
    response = base_response.copy()
    print(response)
    processRequest(req)
    return jsonify(response)


def processRequest(req):
    if req.body.queryResult.action('getPaperRequisites'):
        print('WOW')
        getPaperRequisites(req)


def getPaperRequisites(req):
    result = req.get.queryResult()
    parameters = result.parameters()
    paper = parameters['papers']
    requisites = parameters['requisites']
    print(paper)
    print(requisites)


if __name__ == '__main__':
    # bind to port if defined, otherwise default to 5000
    port = int(os.getenv('PORT', 5000))
    print('Starting Rudy on port %d' % port)
    app.run(debug=False, port=port, host='0.0.0.0')
