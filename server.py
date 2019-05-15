"""
A simple web server to execute the bot functions
"""

import os
from flask import Flask, jsonify
from flask_httpauth import HTTPTokenAuth
from hashlib import blake2b 

from bot import TwitterBot 

bot = TwitterBot()

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Token')

@auth.verify_token
def verify_token(token):
    token_hash = blake2b(bytes(token, encoding='utf8')).hexdigest()
    return token_hash == os.environ['TOKEN_HASH']

@app.route('/')
def index():
    """
    Return total number of tweets bot has tweeted so far
    """
    return jsonify({
        'num_tweets': bot.get_num_tweets(),
    })

@app.route('/tweet')
@auth.login_required
def tweet():
    """
    Tweet a random word and return the tweet's ID
    """
    tweet = bot.tweet_random_word()
    return jsonify({
        'tweet_id': tweet.id_str,
    })

@app.route('/update-header')
@auth.login_required
def update_header():
    """
    Update the Twitter header (API method returns the User object,
    so we'll just return the user's ID
    """
    user = bot.update_header_image()
    return jsonify({
        'user_id': user.id_str,
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 8080))