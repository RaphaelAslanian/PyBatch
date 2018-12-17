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

    def run(self):
        self.state = self.STATE_RUNNING
        docker_client = docker.from_env()
        container = docker_client.containers.run(
            self.jobDefinitionData.containerProperties["image"],
            remove=True,
            detach=True
        ).wait()
        if container["StatusCode"] == 0:
            self.state = self.STATE_SUCCEEDED
        else:
            self.state = self.STATE_FAILED

    def __repr__(self):
        return f"My state is {self.state}"
