from enum import Enum
from threading import Thread
import docker


class Job(Thread):

    class STATE(Enum):
        CREATED = 0,
        RUNNING = 1,
        SUCCEEDED = 2,
        FAILED = 3

    def __init__(self, *args, **kwargs):
        Thread.__init__(self)
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.state = self.STATE.CREATED
        self.container = None

    def run(self):
        self.state = self.STATE.RUNNING
        docker_client = docker.from_env()
        self.container = docker_client.containers.run(self.jobDefinitionData.containerProperties["image"])
        self.state = self.STATE.SUCCEEDED

    def __repr__(self):
        state = {
            self.STATE.CREATED: "CREATED",
            self.STATE.RUNNING: "RUNNING",
            self.STATE.SUCCEEDED: "SUCCEEDED",
            self.STATE.FAILED: "FAILED",
        }
        return f"My state is {state[self.state]}"
