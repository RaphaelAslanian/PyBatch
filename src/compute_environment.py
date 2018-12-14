import json


class ComputeEnvironment:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.state = "ENABLED"

    def __repr__(self):
        return json.dumps(self.__dict__)

    def update(self):
        pass


class ComputeEnvironmentIterable:

    def __init__(self):
        self.ces = []

    def __iter__(self):
        return self.ces

    def __getitem__(self):
        return 3

    def update(self):
        pass
