import json


class JobDefinition:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def __repr__(self):
        return json.dumps(self.__dict__)
