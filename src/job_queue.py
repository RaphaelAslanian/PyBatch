import json
from enum import Enum
from queue import PriorityQueue


class JobQueue(PriorityQueue):

    def __init__(self, jobQueueName, priority, **kwargs):
        PriorityQueue.__init__(self)
        self.jobQueueName = jobQueueName
        self.priority = priority


