#!/usr/bin/env python

import os
import json

# flask will be used to interact with Rudy through a predefined webhook
# jsonify for generating Rudy's response in json format
# make_response will pass the text response from Rudy to clients
# request will be client side's request (input) in json format
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)


# the fulfillment webhook in Dialogflow should have an ending like=> /webhook
# For example, if a heroku app has an url of sunnysideup.app, the whole
# webhook url from Dialogflow to heroku should be sunnysideup.app/webhook
# so a request should be routed to this webhook function directly
@app.route('/webhook', methods=['POST'])
def webhook():
    # getting a request from rudy
    req = request.get_json(silent=True, force=True)

    # print in json format
    print('Request from Dialogflow:')
    print(json.dumps(req, indent=4))

    # process a request
    res = process_request(req)

    # paper = req.get['queryResult']['parameters'].get('papers')

    # paper = req.queryResult.parameters['papers']
    return make_response(res)


def process_request(req):
    if req['queryResult'].get('action') == 'getPaperRequisites':
        paper = req['queryResult']['parameters'].get('paper')
        print('WOW')
    res = jsonify({'fulfillmentText': paper})
    return res
    # getPaperRequisites(req)


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
