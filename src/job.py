import datetime
import hashlib
import logging
import threading
from threading import Thread
import docker

from json_configuration import CONFIG_SUBMIT_JOB
from schema_constructor import SchemaConstructor


class Job(Thread):
    """
    Represents one job executed by AWS Batch. It uses a jobDefinitionData
    """

    STATE_SUBMITTED = "SUBMITTED"
    STATE_PENDING = "PENDING"
    STATE_CREATED = "CREATED"
    STATE_RUNNING = "RUNNING"
    STATE_SUCCEEDED = "SUCCEEDED"
    STATE_FAILED = "FAILED"
    STATE_STARTING = "STARTING"
    STATE_RUNNABLE = "RUNNABLE"

    DEFAULT_VALUES = {}

    def __init__(self, **kwargs):
        Thread.__init__(self)
        SchemaConstructor.__init__(
            self,
            schema=CONFIG_SUBMIT_JOB,
            defined_values=kwargs,
            default_values=self.DEFAULT_VALUES
        )
        self.__created_at = datetime.datetime.now()
        self.__started_at = None
        self.__stopped_at = None
        self.__container = None
        self.__jobId = hashlib.md5(f"{self.jobName}{self.__created_at}".encode()).hexdigest()
        self.__logger = logging.getLogger(f"{self.jobName} {self.getName()} {self.__jobId}")
        self.change_state(self.STATE_SUBMITTED)

    def run(self):
        docker_client = docker.from_env()
        self.__started_at = datetime.datetime.now()
        self.change_state(self.STATE_STARTING)
        self.__container = docker_client.containers.run(
            command=self.containerOverrides["command"] if self.containerOverrides
            else self.jobDefinitionData.containerProperties["command"],
            image=self.containerOverrides["command"] if self.containerOverrides
            else self.jobDefinitionData.containerProperties["image"],
            environment=self.containerOverrides["environment"] if self.containerOverrides
            else self.jobDefinitionData.containerProperties["environment"],
            user=self.jobDefinitionData.containerProperties["user"] or None,
            privileged=self.jobDefinitionData.containerProperties["privileged"] or None,
            volumes=self.jobDefinitionData.containerProperties["volumes"] or None,
            read_only=self.jobDefinitionData.containerProperties["readonlyRootFilesystem"] or None,
            mem_limit=self.jobDefinitionData.containerProperties["memory"],
            detach=True
        )
        self.change_state(self.STATE_RUNNING)
        result = self.__container.wait()
        self.change_state(self.STATE_SUCCEEDED if result["StatusCode"] == 0 else self.STATE_FAILED)
        self.__stopped_at = datetime.datetime.now()
        with open(f"logs/{self.__created_at.strftime('%Y-%m-%d_%H:%M:%S')}__{self.jobName}", "wb") as log_file:
            log_file.write(self.__container.logs())
        self.__container.remove()

    def stop(self):
        if self.__container:
            self.__container.stop()
            self.state = self.STATE_FAILED

    def cancel(self):
        if self.state in (self.STATE_SUBMITTED, self.STATE_PENDING, self.STATE_RUNNABLE):
            pass

    def terminate(self):
        if self.state in (self.STATE_RUNNING, self.STATE_STARTING):
            self.stop()
        else:
            self.cancel()

    def __lt__(self, other):
        return self.priority < other.prioriy

    def describe(self, everything=False):
        # ToDo: jobId value to edit
        return {
            "jobId": self.__jobId,
            "jobName": self.jobName
        }

    def summary(self):
        return {
            "createdAt": self.__created_at.timestamp(),
            "jobId": self.__jobId,
            "jobName": self.jobName,
            "status": self.state
        }

    def change_state(self, new_state: str):
        self.state = new_state
        self.__logger.info(f"New Job state: {self.state}")

