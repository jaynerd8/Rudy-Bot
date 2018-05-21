#!/usr/bin/env python

# Importing os to access core libraries of Heroku including secured
# config vars.
import os

# Importing json to manage communication contents in the acceptable
# json format.
import json

# Importing firebase_admin to authenticate server's Firebase database
# access.
import firebase_admin

# credentials will be used to confirm identification of the service
# key provided in Heroku's config vars.
from firebase_admin import credentials

# db will be the main database that Rudy will be accessing.
from firebase_admin import db

# Flask package will manage flow of communications between the server
# and client.
# 1. jsonify will be used for translating Rudy's response into
# an acceptable json format.
# 2. make_response will pass the text response
# from Heroku app (Rudy) to client's Dialogflow view.
# 3. request components contains json format messages from the client
# side (input).
from flask import Flask, jsonify, make_response, request

# Starting flask app in global layout.
app = Flask(__name__)

# Database url (Firebase).
db_url = {'databaseURL': 'https://rudy-b5e54.firebaseio.com'}

# Secured service account key json from Heroku's config vars.
key = {"type": os.environ['type'],
       "project_id": os.environ['project_id'],
       "private_key_id": os.environ['private_key_id'],
       "private_key": os.environ['private_key'].replace('\\n', '\n'),
       "client_email": os.environ['client_email'],
       "client_id": os.environ['client_id'],
       "auth_uri": os.environ['auth_uri'],
       "token_uri": os.environ['token_uri'],
       "auth_provider_x509_cert_url": os.environ['auth_provider_x509_cert_url'],
       "client_x509_cert_url": os.environ['client_x509_cert_url']}

# Authentication process into Firebase.
print('Rudy (Firebase): Connecting to Firebase.')
cred = credentials.Certificate(key)
firebase = firebase_admin.initialize_app(cred, db_url)
print(firebase)
print('Rudy (Firebase): Firebase access granted.')

# Generating database references.
db_requisites = db.reference('requisites')


# The fulfillment webhook settings in Dialogflow should have a url
# that ends with '/webhook'. For example, if an Heroku app has a url of
# rudybot.app, the finalized Dialogflow's fulfillment webhook integration
# address should be 'rudybot.app/webhook'. Upon generating a successful
# server-client connection, the client request will be routed to the
# webhook function below.
@app.route('/webhook', methods=['POST'])
def webhook():
    # Get a request from client then print.
    req = request.get_json(silent=True, force=True)
    print('Rudy (Flask): Request received ->')
    print(json.dumps(req, indent=4))

    # Process the request to get a response.
    res = process_request(req)
    print('Rudy (Heroku): Generated response ->')
    print(res)

    # Returning acquired response in json format to the client's
    # Dialogflow view.
    return make_response(res)


# Sorting out client's request then forward to a matching function based
# on the action parameter of the request's intent.
def process_request(req):
    print('Rudy (Heroku): Request processing started.')

    # Request sorting process.
    result: str
    if req['queryResult'].get('action') == 'getPaperRequisites':
        result = get_paper_requisites(req)
    return jsonify({'fulfillmentText': result})


# Get required parameters from the request for a database query.
def get_paper_requisites(req):
    # Getting parameters.
    speech = ''
    paper = req['queryResult']['parameters'].get('paper')
    requisite = req['queryResult']['parameters'].get('requisite')

    # Query creation.
    print('Rudy (Heroku): Requisites query created.')
    requisites_query = make_requisites_query(paper, requisite)

    # Parsing query results into a speech format.
    if requisites_query is None:
        print('Rudy (Firebase): Requisites query is empty.')
        speech += 'There are no ' + requisite + ' for paper: ' + paper
    else:
        print('Rudy (Firebase): Parsing query results.')
        speech += 'The list of ' + requisite + ' are: ' + str(requisites_query).strip('[]')

    # Returning the speech contexts.
    return speech


# Get requisite data source from Firebase based on the request parameters.
def make_requisites_query(paper, requisite):
    print('Rudy (Firebase): Accessing to the database.')
    query_result = db_requisites.child(paper).child(requisite).get()
    return query_result


# Initializing app to server connection (hosting).
if __name__ == '__main__':
    # Setting the default port to 5000. Other defined values can be
    # used as an alternative.
    port = int(os.getenv('PORT', 5000))
    print('Rudy (Heroku): Starting Rudy on port %d' % port)
    app.run(debug=True, port=port, host='0.0.0.0')
