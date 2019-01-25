import datetime
from threading import Thread
import docker

from json_configuration import CONFIG_SUBMIT_JOB
from schema_constructor import SchemaConstructor


class Job(Thread):
    """
    Represents one job executed by AWS Batch. It uses a jobDefinitionData
    """

    STATE_SUBMITTED = "SUBMITTED"
    STATE_CREATED = "CREATED"
    STATE_RUNNING = "RUNNING"
    STATE_SUCCEEDED = "SUCCEEDED"
    STATE_FAILED = "FAILED"

    DEFAULT_VALUES = {
        "state": STATE_SUBMITTED
    }

    def __init__(self, **kwargs):
        Thread.__init__(self)
        SchemaConstructor.__init__(
            self,
            schema=CONFIG_SUBMIT_JOB,
            default_values=self.DEFAULT_VALUES,
            defined_values=kwargs
        )
        self.__created_at = datetime.datetime.now()
        self.__started_at = None
        self.__stopped_at = None
        self.__container = None

    def run(self):
        self.state = self.STATE_RUNNING
        self.__started_at = datetime.datetime.now()
        docker_client = docker.from_env()
        command = self.containerOverrides["command"] if self.containerOverrides \
            else self.jobDefinitionData.containerProperties["command"]
        image = self.containerOverrides["command"] if self.containerOverrides \
            else self.jobDefinitionData.containerProperties["image"]
        environment = self.containerOverrides["environment"] if self.containerOverrides \
            else self.jobDefinitionData.containerProperties["environment"]
        self.__container = docker_client.containers.run(
            command=command,
            image=image,
            environment=environment,
            user=self.jobDefinitionData.containerProperties["user"],
            privileged=self.jobDefinitionData.containerProperties["privileged"],
            volumes=self.jobDefinitionData.containerProperties["volumes"],
            read_only=self.jobDefinitionData.containerProperties["readonlyRootFilesystem"],
            mem_limit=self.jobDefinitionData.containerProperties["memory"],
            remove=True,
            detach=True
        )
        result = self.__container.wait()
        self.__stopped_at = datetime.datetime.now()
        self.state = self.STATE_SUCCEEDED if result["StatusCode"] == 0 else self.STATE_FAILED

    def stop(self):
        if self.__container:
            self.__container.kill()

    def __lt__(self, other):
        return self.priority < other.prioriy

    def describe(self, everything=False):
        # ToDo: jobId value to edit
        return {
            "jobId": "GreatId",
            "jobName": self.jobName
        }

    def summary(self):
        return {
            "createdAt": self.__created_at.timestamp(),
            "jobId": "GreatId",
            "jobName": self.jobName,
            "status": self.state
        }
