"""
The stuff that the bot actually does
"""

import argparse
from jmdict import JMDict
from twitter import get_api
from header import generate_header, HEADER_PATH

def tweet_random_word():
    jmd = JMDict()
    entry = jmd.random_entry()
    api = get_api()
    api.update_status(entry.get_definition())

def update_header():
    generate_header()
    api = get_api()
    api.update_profile_banner(HEADER_PATH)

def main():

    parser = argparse.ArgumentParser(description='A cool twitter bot :)')
    parser.add_argument('--update-header', action='store_true')
    args = parser.parse_args()

    if args.update_header:
        update_header()
    else:
        tweet_random_word()

if __name__ == '__main__':
    main()