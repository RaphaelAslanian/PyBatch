import json
from enum import Enum
from queue import Queue
from typing import List

from json_configuration import CONFIG_CREATE_JOB_QUEUE
from schema_constructor import SchemaConstructor


class JobQueue(Queue, SchemaConstructor):

    def __init__(self, **kwargs):
        Queue.__init__(self)
        SchemaConstructor.__init__(self, schema=CONFIG_CREATE_JOB_QUEUE)
        for key, val in kwargs.items():
            setattr(self, key, val)

    def get_ordered_compute_environments(self) -> List[str]:
        """ Retrieve list of ordered compute environments to try in scheduler """
        sorted_compute_envs = sorted(self.computeEnvironmentOrder, key=lambda x: x["order"])
        return [ce["computeEnvironment"] for ce in sorted_compute_envs]
