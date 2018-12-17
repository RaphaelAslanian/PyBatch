import json
from enum import Enum
from queue import Queue

from json_configuration import CONFIG_CREATE_JOB_QUEUE
from schema_constructor import SchemaConstructor


class JobQueue(Queue, SchemaConstructor):

    def __init__(self, **kwargs):
        Queue.__init__(self)
        SchemaConstructor.__init__(self, schema=CONFIG_CREATE_JOB_QUEUE)
        for key, val in kwargs.items():
            setattr(self, key, val)
