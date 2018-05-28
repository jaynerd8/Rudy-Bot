#!/usr/bin/env python
import os
import json
import firebase_admin

from firebase_admin import credentials, db
from flask import Flask, jsonify, make_response, request

# Starting the flask application in global layout.
app = Flask(__name__)
db_url = {'databaseURL': 'https://rudy-b5e54.firebaseio.com'}
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

print('Rudy: Connecting to Firebase.')

cred = credentials.Certificate(key)
firebase = firebase_admin.initialize_app(cred, db_url)

print('Rudy: Firebase access granted.')

db_requisites = db.reference('requisites')


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print('Rudy: Request received ->')
    print(json.dumps(req, indent=4))
    res = process_request(req)
    return make_response(res)


def process_request(req):
    print('Rudy: Request processing started.')
    result: str
    if req['queryResult'].get('action') == 'getPaperRequisites':
        result = get_paper_requisites(req)
    if req['queryResult'].get('action') == 'getFailureDetails':
        result = get_failure_details(req)
    print('Rudy: Generated response ->')
    print(result)

    return jsonify({'fulfillmentText': result})


def get_paper_requisites(req):
    print('Rudy: Extracting required parameters.')

    speech = ''
    paper = req['queryResult']['parameters'].get('paper')
    requisites = [req['queryResult']['parameters'].get('requisite'),
                  req['queryResult']['parameters'].get('requisite1')]

    print('Rudy: Requisites query created.')
    requisites_query = make_requisites_query(paper, requisites)

    counter = 0
    for result in requisites_query:
        if result is None:
            print('Rudy: Requisites query is empty.')
            speech += 'There are no ' + requisites[counter] + ' for paper: ' \
                      + paper + '. '
        else:
            print('Rudy: Parsing query results.')
            speech += 'The list of ' + requisites[counter] + ' are: ' \
                      + str(result).strip('[]') + '. '
        counter += 1

    return speech


def get_failure_details(req):
    print('Rudy: Extracting required parameters.')

    speech = ''
    paper = req['queryResult']['parameters'].get('paper')

    print('Rudy: failure details query created.')
    failure_details_query = make_failure_details_query(paper)

    for result in failure_details_query:
        if result is None:
            print('Rudy: Requisites query is empty.')
            speech += 'There are no restrictions for paper: ' \
                      + paper + '. ' + 'You can still take whatever you want. '
        else:
            print('Rudy: Parsing query results.')
            speech += 'Other than ' + str(result).strip('[]') + ', ' \
                      + 'you can freely choose next courses'

    return speech


def make_requisites_query(paper, requisites):
    print('Rudy: Accessing to the database.')

    query_result = [db_requisites.child(paper).child(requisites[0]).get()]

    if requisites[1] is not '' and requisites[0] is not requisites[1]:
        query_result.append(db_requisites.child(paper).child(requisites[1]).get())

    return query_result


def make_failure_details_query(paper, requisites):
    print('Rudy: Accessing to the database.')

    query_result = [db_requisites.child(paper).child('next').get()]

    return query_result


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print('Rudy: Starting Rudy on port %d' % port)
    app.run(debug=True, port=port, host='0.0.0.0')
