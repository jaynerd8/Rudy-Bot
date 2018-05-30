#!/usr/bin/env python


# ----------------------------------REGION IMPORT---------------------------------- #


# Importing os to access core libraries of Heroku including secured config vars.
import os

# Importing json to manage communication contents in the acceptable json format.
import json

# Importing firebase_admin to authenticate server's Firebase access.
import firebase_admin

# Credentials will be used to confirm identification of the service key provided in
# Heroku's config vars.
# db will be the main database that Rudy will be accessing.
from firebase_admin import credentials, db

# Flask package will manage flow of communications between the server and client.
# 1. jsonify will be used for translating Rudy's response into an acceptable json
# format.
# 2. make_response will pass the text response from Heroku app (Rudy) to client's
# Dialogflow view.
# 3. request components contains json format messages from the client side (input).
from flask import Flask, jsonify, make_response, request

# --------------------------------END_REGION IMPORT-------------------------------- #


# ----------------------------------REGION GLOBAL---------------------------------- #


# Starting the flask application in global layout.
app = Flask(__name__)

# Database url (Firebase).
db_url = {'databaseURL': 'https://rudy-b5e54.firebaseio.com'}

# Secured service account key in json format. Will be referred from Heroku's preset
# config vars.
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
print('Rudy: Connecting to Firebase.')
cred = credentials.Certificate(key)
firebase = firebase_admin.initialize_app(cred, db_url)
print('Rudy: Firebase access granted.')

# Instantiating database references.
db_requisites = db.reference('requisites')
db_majors = db.reference('majors')
db_jobs = db.reference('jobs')
db_major_list = db.reference('major-list')


# --------------------------------END_REGION GLOBAL-------------------------------- #


# ---------------------------------REGION WEBHOOK---------------------------------- #


# The fulfillment webhook settings in Dialogflow should have a url that ends with
# '/webhook'. For example, if an Heroku app has a url of rudybot.app, the finalized
# Dialogflow's webhook integration address should be 'rudybot.app/webhook'. Upon
# generating a successful server-client connection, the client request will be rout
# -ed to the webhook function below.
@app.route('/webhook', methods=['POST'])
def webhook():
    # Getting the request from client then print.
    req = request.get_json(silent=True, force=True)
    print('Rudy: Request received ->')
    print(json.dumps(req, indent=4))

    # Process the request to generate a response.
    res = process_request(req)

    # Returning generated response in json format to the client's Dialogflow view.s
    return make_response(res)


# Sorting out client's request then forward to a matching function based on the
# action parameter of the request's intent.
def process_request(req):
    print('Rudy: Request processing started.')

    # Starting request sorting process.
    result: str
    if req['queryResult'].get('action') == 'getPaperRequisites':
        result = get_paper_requisites(req)
    elif req['queryResult'].get('action') == 'getFailureDetails':
        result = get_failure_details(req)
    elif req['queryResult'].get('action') == 'getMajorDetails':
        result = get_major_details(req)
    elif req['queryResult'].get('action') == 'getMajorList':
        result = get_major_list()

    # Showing the generated response.
    print('Rudy: Generated response ->')
    print(result)

    # Returning the result in the acceptable json format.
    return jsonify({'fulfillmentText': result})


# -------------------------------END_REGION WEBHOOK-------------------------------- #


# --------------------------------REGION REQUISITES-------------------------------- #


# Get required parameters (papers & requirements) from the request for a database
# query.
def get_paper_requisites(req):
    print('Rudy: Extracting paper & requisite parameters.')

    # Getting paper and requisite parameters.
    speech = ''
    paper = req['queryResult']['parameters'].get('paper')
    requisites = [req['queryResult']['parameters'].get('requisite'),
                  req['queryResult']['parameters'].get('requisite1')]

    # Creating query.
    print('Rudy: Requisites query created.')
    requisites_query = make_requisites_query(paper, requisites)

    # Parsing query results into a speech format.
    counter = 0
    for result in requisites_query:
        if result is None:
            print('Rudy: Requisites query is empty.')
            speech += 'There are no ' + requisites[counter] + ' for paper ' \
                      + paper + '. '
        else:
            print('Rudy: Parsing query results.')
            speech += 'Here is the list of ' + requisites[counter] + '. ' \
                      + str(result).strip('[]') + '. '
        counter += 1

    # Returning the speech context.
    return speech


# Get requisite data source from Firebase based on the requested parameters.
def make_requisites_query(paper, requisites):
    print('Rudy: Accessing to the database.')

    # Making a list of query results for multiple requisite parameters.
    query_result = [db_requisites.child(paper).child(requisites[0]).get()]

    # If client asks about two different types of requisite parameters.
    if requisites[1] is not '' and requisites[0] is not requisites[1]:
        query_result.append(db_requisites.child(paper).child(requisites[1]).get())

    # Returning collected query results.
    return query_result


# ------------------------------END_REGION REQUISITES------------------------------ #


# ------------------------------REGION MAJOR_DETAILS------------------------------- #


# Get required parameters (majors) from the request for a database query.
def get_major_details(req):
    print('Rudy : Extracting major parameters. (majors)')

    # Getting parameters.
    speech = ''
    major = req['queryResult']['parameters'].get('major')
    year = req['queryResult']['parameters'].get('year')

    # Query creation.
    print('Rudy: Major details query created.')
    major_details_query = make_major_details_query(major, year)

    # Parsing query results into a speech format.
    if major_details_query is None:
        print('Rudy: Major details query is empty.')
        speech += 'There are no ' + year + ' courses for ' + major + ' major. '
    else:
        print('Rudy: Parsing query results.')
        speech += 'The list of suggested courses for ' + year \
                  + ' are ' + str(major_details_query).strip('{}') + '. '

    # Returning the speech contexts.
    return speech


# Get major details data source from Firebase based on the request parameters.
def make_major_details_query(major, year):
    print('Rudy: Accessing to the database.')

    # Making a list of query results for the specific year's major details.
    query_result = str(db_majors.child(major).child(year).get()).strip('[]')

    # Returning collected query results.
    return query_result


# ----------------------------END_REGION MAJOR_DETAILS----------------------------- #


# -------------------------------REGION MAJOR_LIST--------------------------------- #


# Get list of majors in BCIS, so the client can choose one of the options.
def get_major_list():
    print('Rudy: Processing major list query request')

    # Query creation.
    speech = ''
    print('Rudy: Major list query created.')
    major_list_query = make_major_list_query()

    # Parsing query results into a speech format.
    if major_list_query is None:
        print('Rudy: Major list query is empty.')
        speech += 'There are no majors you can choose for now.'
    else:
        print('Rudy: Parsing query results.')
        speech += 'The majors offered in the BCIS department are: ' \
                  + str(major_list_query).strip('[]') + '.'

    # Returning speech context.
    return speech


# Get major list information from Firebase.
def make_major_list_query():
    print('Rudy: Accessing to the database.')

    # Making a query result for the major list.
    query_result = [db_major_list.get()]

    # Returning collected query results.
    return query_result


# -----------------------------END_REGION MAJOR_LIST------------------------------- #


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


def make_failure_details_query(paper):
    print('Rudy: Accessing to the database.')

    query_result = [db_requisites.child(paper).child('next').get()]

    return query_result


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print('Rudy: Starting Rudy on port %d' % port)
    app.run(debug=True, port=port, host='0.0.0.0')
