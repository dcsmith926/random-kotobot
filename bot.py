"""
The stuff that the bot actually does
"""

import argparse

from jmdict import JMDict
from twitter import get_api
from header import generate_header, HEADER_PATH

class TwitterBot(object):

    def __init__(self, api):
        self.api = api 

    def get_num_tweets(self):
        user = self.api.me()
        return user.statuses_count

    def tweet_random_word(self):
        jmd = JMDict()
        entry = jmd.random_entry()
        return self.api.update_status(entry.get_definition())

    def update_header_image(self):
        generate_header()
        return self.api.update_profile_banner(HEADER_PATH)

def main():

    parser = argparse.ArgumentParser(description='A cool twitter bot :)')
    parser.add_argument('--update-header', action='store_true')
    args = parser.parse_args()

    bot = TwitterBot(get_api())

    if args.update_header:
        bot.update_header_image()
    else:
        bot.tweet_random_word()

if __name__ == '__main__':
    main()