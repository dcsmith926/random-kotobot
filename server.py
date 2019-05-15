"""
A simple web server
"""

import os
from flask import Flask, jsonify

from twitter import get_api

app = Flask(__name__)

@app.route('/')
def index():
    """
    Return total number of tweets bot has tweeted so far
    """
    api = get_api()
    user = api.me()
    return jsonify({
        'num_tweets': user.statuses_count,
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 8080))