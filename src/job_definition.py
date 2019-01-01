import json

from arn_dict import ARNObject
from json_configuration import CONFIG_REGISTER_JOB_DEFINITION
from schema_constructor import SchemaConstructor


class JobDefinition(SchemaConstructor, ARNObject):
    """
    Class representing an AWS Batch Job definition.
    """

    DEFAULT_VALUES = {}

    def __init__(self, revision, **kwargs):
        self.revision = revision
        SchemaConstructor.__init__(self, schema=CONFIG_REGISTER_JOB_DEFINITION, default_values=self.DEFAULT_VALUES, defined_values=kwargs)
        ARNObject.__init__(self, name=self.jobDefinitionName, resource="job-definition/" + self.jobDefinitionName + ":" + str(self.revision))

    def describe(self, everything=False):
        # ToDo: confirm validity of those fields
        if not everything:
            return {
                "jobDefinitionArn": self.arn,
                "jobDefinitionName": self.jobDefinitionName,
                "revision": self.revision
            }
        else:
            return {
                "jobDefinitionArn": self.arn,
                "jobDefinitionName": self.jobDefinitionName,
                "revision": self.revision,
                "containerProperties": self.containerProperties,
                "nodeProperties": self.nodeProperties,
                "parameters": self.parameters,
                "retryStrategy": self.retryStrategy,
                "timeout": self.timeout,
                "status": "",
            }

