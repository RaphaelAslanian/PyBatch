from queue import Queue
from typing import List

from json_configuration import CONFIG_CREATE_JOB_QUEUE
from schema_constructor import SchemaConstructor
from arn_dict import ARNObject


class JobQueue(Queue, SchemaConstructor, ARNObject):

    STATE_ENABLED = "ENABLED"
    STATE_DISABLED = "DISABLED"

    DEFAULT_VALUES = {
        "state": STATE_ENABLED,
    }

    def __init__(self, **kwargs):
        Queue.__init__(self)
        SchemaConstructor.__init__(self, schema=CONFIG_CREATE_JOB_QUEUE, default_values=self.DEFAULT_VALUES, defined_values=kwargs)
        ARNObject.__init__(self, name=self.jobQueueName, resource="job-queue/" + self.jobQueueName)

    def get_ordered_compute_environments(self) -> List[str]:
        """ Retrieve list of ordered compute environments to try in scheduler """
        sorted_compute_envs = sorted(self.computeEnvironmentOrder, key=lambda x: x["order"])
        return [ce["computeEnvironment"] for ce in sorted_compute_envs]

    def describe(self, everything: bool = False):
        # ToDo: status and statusReason are not mandatory, check parameters in api reference
        if not everything:
            return {
                "jobQueueArn": self.arn,
                "jobQueueName": self.jobQueueName,
            }
        else:
            return {
                "computeEnvironmentOrder": self.computeEnvironmentOrder,
                "jobQueueArn": self.arn,
                "jobQueueName": self.jobQueueName,
                "priority": self.priority,
                "state": self.state,
                "status": "",
                "statusReason": "",
            }
