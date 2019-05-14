import os
from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue

from bot import tweet_random_word, update_header
from worker import conn

q = Queue(connection=conn)
sched = BlockingScheduler()

# run 4 times a day, at every 6th hour
@sched.scheduled_job('cron', hour='0,6,12,18')
def schedule_tweet():
    q.enqueue(tweet_random_word)

# run every Sunday at midnight
@sched.scheduled_job('cron', day_of_week='sun', hour=0)
def schedule_update_header():
    q.enqueue(update_header)

if __name__ == '__main__':
    sched.start()