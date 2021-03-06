import logging
import queue
from threading import Thread
from typing import Dict

from job import Job
from json_configuration import CONFIG_CREATE_COMPUTE_ENVIRONMENT
from schema_constructor import SchemaConstructor
from stoppable_thread import StoppableThread
from arn_object import ARNObject


class ComputeEnvironment(Thread, StoppableThread, SchemaConstructor, ARNObject):

    STATE_ENABLED = "ENABLED"
    STATE_DISABLED = "DISABLED"

    DEFAULT_VALUES = {
        "state": STATE_ENABLED
    }

    MAX_PARALLEL_JOBS = 4

    def __init__(self, **kwargs):
        Thread.__init__(self)
        StoppableThread.__init__(self, setted=False)
        SchemaConstructor.__init__(
            self,
            schema=CONFIG_CREATE_COMPUTE_ENVIRONMENT,
            default_values=self.DEFAULT_VALUES,
            defined_values=kwargs
        )
        ARNObject.__init__(
            self,
            name=self.computeEnvironmentName,
            resource="compute-environment/" + self.computeEnvironmentName
        )
        self.__associated_queue = queue.PriorityQueue(maxsize=4)  # Compute maxsize as parameter of CE power
        self.__jobs_current = []
        self.__logger = logging.getLogger(f"[CE] {self.computeEnvironmentName} {self.getName()}")
        self.__logger.info("Compute environment created")

    def run(self):
        while not self.stop_event.wait(timeout=1):
            if self.state == self.STATE_ENABLED:
                # Handle current jobs
                for idx, job in enumerate(self.__jobs_current):
                    if job.state in (job.STATE_SUCCEEDED, job.STATE_FAILED):
                        self.__logger.info(f"Detected job '{job.jobName}' finished")
                        self.__jobs_current.pop(idx)
                        break
                # Take new jobs
                try:
                    if len(self.__jobs_current) <= self.MAX_PARALLEL_JOBS:  # Parameterized max size here
                        job = self.__associated_queue.get_nowait()
                        self.__jobs_current.append(job)
                        job.start()
                except queue.Empty:
                    continue
        for job in self.__jobs_current:
            job.stop()

    def is_enabled(self) -> bool:
        """ Returns True if the compute environment's state is 'ENABLED' ; False otherwise """
        return self.state == self.STATE_ENABLED

    def has_capacity(self) -> bool:
        """
        Returns True if the compute environment's own internal queue is full, depicting the fact
        that the compute environment is working at maximum capacity. False otherwise.
        """

        return not self.__associated_queue.full()

    def add_job(self, job: Job):
        """
        Add a job to the compute environment's own internal queue.
        :param job: job to be processed by the compute environment.
        """
        job.change_state(Job.STATE_RUNNABLE)
        self.__associated_queue.put_nowait(job)

    def describe(self, everything=False) -> Dict[str, str]:
        # Todo: some values need to be checked with API reference.
        if not everything:
            return {
                "computeEnvironmentArn": self.arn,
                "computeEnvironmentName": self.computeEnvironmentName
            }
        else:
            return {
                "computeEnvironmentArn": self.arn,
                "computeEnvironmentName": self.computeEnvironmentName,
                "computeResources": self.computeResources,
                "ecsClusterArn": "PyBatch",
                "serviceRole": self.serviceRole,
                "state": self.state,
                "status": "",
                "statusReason": "",
                "type": self.type
            }

    def __del__(self):
        self.__logger.info("Compute environment deleted")
