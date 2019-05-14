"""
A simple web server
"""

from flask import Flask
from json import JSONEncoder
import os
from twitter import get_api

app = Flask(__name__)

@app.route('/')
def index():
    """
    Return total number of tweets bot has tweeted so far
    """
    api = get_api()
    user = api.me()
    return JSONEncoder().encode({
        'num_tweets': user.statuses_count,
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 8080))