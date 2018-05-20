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
    key = authenticate()
    print(key)
    cred = credentials.Certificate(key)
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://rudy-b5e54.firebaseio.com'})

    req = request.get_json(silent=True, force=True)
    print('Request from client:')
    print(json.dumps(req, indent=4))

    print(db.reference('degrees').child('Bachelor of Applied Science').get())


# return make_response(req)


def authenticate():
    key = {
        "type": "service_account",
        "project_id": "rudy-b5e54",
        "private_key_id": "6122bb03ca6f7ae3bc96e5451df252beeaf72b57",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCZMvJ2zbCSYx66\n2/4m7DdKOQ0PRKvG8+0yg6676RiGYRrnFGK7Zjs9rejmbQw4UT2EyWPl7/MGvEkp\nhUeJFAuIkcM6OjyLY29DfQ1IRIqyhPz88X9t+TEQskWkl9QK5sn/qMk4My/xCQjH\n1yK2Jpcb1Flhwc0bDm1vDikfBk8OUjVohbBrPx7uulnwamRnSkc7aFlkdwsJwDET\nklPVLHZpT3YPazem3/vx97zQDnqCK79rzGHx7yrr3JoM838IiTZhuLm4NuZiAc9w\nHj/Y6p5MtbYyJIOe5gARMtl0Iyzmn2uqfk/SYo+MVEQEgmuCJSe5RQeJppSKotZk\nExRFezr3AgMBAAECggEANv2jLAL8WSeMPc2+5nDPDez5o5vmPyWK5KGBBMGQhJfx\npLXcFOGG7UZyPdgx1TtQJkx19/EQHsBSUL2fJnTUCQMtfUavOeeI5kRKksDLunXj\nK9ZyA+M5egFL31+ChSE/q+4FwI8bK92u0bEHLDQg9KPeK6l5urcMkBsYpqLImN5a\nMad9zxmQ+NzeTUd0g63knzqcfzBsz0+m38eAC4azyoS3/mbLePjw37R49h7YdpGr\nA0zpCh8FWXpZlI1vcpBvzOjjlhxuPp6eHtHLAR+9Va9+iQZBH/1KOsTNwl8NsAyw\nxKouO7kl9CgqZpFv+G1rLoHYr2j9WhF9n30TpwK5FQKBgQDOky+lcg23nqEvqwgW\nuEu18dujHiOWXW3YbbTIyUj1466BftLMh6oxYvcekLdkNSiTJzvhV2Ll//MoywCm\n6H74k2da1VlS0Ao6KluAWOxfmg/IUMo+9+mTQjgxFg/N/wYWLcgh56ki6Dh9BAko\n8Z1n049AOKec1laBLziODMnt6wKBgQC92nWqyhnvZuM0Hi2Fb/tLS/Dzm/9eUuWi\nxI9qcV/B/4rvVwv6iVXBD+6Kd8caVWl+GlTJomCHO5AAGXBuXEC8Yn6G1F7C70of\nXSA77yiIq8ArXs+ot7JaO1mRLk9aaMBHM0dUBa+58gTSEQsvd7hLUl/rucYl/cx6\n+qMAXPWIJQKBgQDNNCzqfqfdtXiM76szVpPvA3iZSwEzB1Bs5F3n7vvJNwlMnf0t\nK78HHDY7aKqkoqHRu/Gh4bremyijZzUYmHA44cST2MfImdzu9tC6aJs2RMZUyNx/\nPKoMnIVRTYcZrLIRKh1agNPlVyV2GqI2x/0C/Iea1iy6gbigz5WwlkepTQKBgQCD\nvqNEvzY8ISOtOPvRyyGQ4MP16NzO8auUxd3XuZD/qHsbF0aitsahUJLx16h8p6Sq\n806/FUTy0uxchUq16qKpl5fBrIGNuEuxdAg4Tv/Lx5N1BTgJFmBXqTPAQWijjmlP\nf1ASCFgnKsEZnOYsLGHhMuqJQ8My/en1tROD3v4rWQKBgQCZF/ABKC9KAUZbhT1U\nZaopE9RzkuwYPPAubGKSGtZSOa5EcUeWiQcffib21mMwS4BPsD2cP/hbWl5ymP+4\nocMxSd12b100j3OiLqHc33ccer0xYk7q4/bRYZITi/0dE5TsZdScWJv5blH3SyLP\nkXNgH77r6XPzNwsgCg1mn3YTkg==\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-82pjt@rudy-b5e54.iam.gserviceaccount.com",
        "client_id": "104996643543832294229",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-82pjt%40rudy-b5e54.iam.gserviceaccount.com"}

    return key


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
