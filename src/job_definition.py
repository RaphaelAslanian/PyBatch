import json


class JobDefinition:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

