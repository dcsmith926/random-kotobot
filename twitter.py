"""
One place where we instantiate our tweepy API instance
"""

import os
import tweepy

def get_api():

    auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
    auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])

    api = tweepy.API(auth)
    
    return api