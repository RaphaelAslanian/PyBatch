from threading import Thread
import docker


class Job(Thread):

    STATE_CREATED = "CREATED"
    STATE_RUNNING = "RUNNING"
    STATE_SUCCEEDED = "SUCCEEDED"
    STATE_FAILED = "FAILED"

    def __init__(self, *args, **kwargs):
        Thread.__init__(self)
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.state = self.STATE_CREATED
        self.container = None

    def run(self):
        self.state = self.STATE_RUNNING
        docker_client = docker.from_env()
        self.container = docker_client.containers.run(
            self.jobDefinitionData.containerProperties["image"],
            remove=True
        )
        self.state = self.STATE_SUCCEEDED

    def __repr__(self):
        return f"My state is {self.state}"
