#!/usr/bin/env python

import os
import json

# Flask will be used to interact with Rudy through a predefined webhook.
# 1. jsonify is for translating Rudy's response into an acceptable json
#    format.
# 2. make_response will pass the text response from Heroku app to Rudy at
#    Dialogflow.
# 3. request contains messages from client side request (input) in json
#    format
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)


# The fulfillment webhook in Dialogflow should have an ending of => /webhook.
# For example, if an heroku app has an url of sunnysideup.app, the whole
# Heroku's webhook url for Dialogflow should be sunnysideup.app/webhook.
# Upon a successful connection, a client request should be directly routed to
# webhook function below.
@app.route('/webhook', methods=['POST'])
def webhook():
    # getting a request from rudy
    req = request.get_json(silent=True, force=True)

    # print request in json format
    print('Request from Dialogflow:')
    print(json.dumps(req, indent=4))

    # process a request
    res = process_request(req)

    # return a text response to Rudy for the client request
    return make_response(res)


# Forward client's request to an appropriate function based on the intent's
# action type.
def process_request(req):
    res: object
    if req['queryResult'].get('action') == 'getPaperRequisites':
        res = get_paper_requisites(req)
    return res


def get_paper_requisites(req):
    # result = req.get.queryResult()
    # parameters = result.parameters()
    # paper = parameters['papers']
    paper = req['queryResult']['parameters'].get('paper')
    requisite = req['queryResult']['parameters'].get('requisite')
    res = jsonify({'fulfillmentText': paper + requisite})
    return res


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.getenv('PORT', 5000))
    print('Starting Rudy on port %d' % port)
    app.run(debug=False, port=port, host='0.0.0.0')
