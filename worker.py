import os
import redis
from rq import Worker, Queue, Connection

conn = redis.from_url(os.environ['REDISTOGO_URL'])

if __name__ == '__main__':
    worker = Worker([Queue(connection=conn)])
    worker.work()