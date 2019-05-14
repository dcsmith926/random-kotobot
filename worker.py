"""
The worker is what actually executes the bot functions, at certain intervals
I'm just crudely sleeping for 6 hours after every tweet, because scheduling
using a clock process is too complicated for this simple use case
(and requires a 3rd Heroku process, which requires non-Free tier dynos)
"""

from datetime import datetime, timedelta
from time import sleep

from bot import tweet_random_word, update_header

def main():

    last_header_update = datetime.now() 

    # okay it'll go out of sync eventually but whatever
    # we'll still be tweeting 4 times a day on average
    while True:

        # tweet our word
        tweet_random_word()

        # update the header image if it's been a week since the last update
        if (datetime.now() - last_header_update).days >= 7:
            update_header()
            last_header_update = datetime.now()

        # sleep for 6 hours
        sleep(6 * 60 * 60)

if __name__ == '__main__':
    main()