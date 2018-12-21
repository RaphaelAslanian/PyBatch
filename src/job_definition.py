import json

from json_configuration import CONFIG_REGISTER_JOB_DEFINITION
from schema_constructor import SchemaConstructor


class JobDefinition(SchemaConstructor):

    def __init__(self, **kwargs):
        SchemaConstructor.__init__(self, schema=CONFIG_REGISTER_JOB_DEFINITION)
        for key, val in kwargs.items():
            setattr(self, key, val)

