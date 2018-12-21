import queue
from asyncio import QueueFull
from collections import deque
from threading import Thread

from json_configuration import CONFIG_CREATE_COMPUTE_ENVIRONMENT
from schema_constructor import SchemaConstructor
from stoppable_thread import StoppableThread


class ComputeEnvironment(Thread, StoppableThread, SchemaConstructor):

    STATE_ENABLED = "ENABLED"
    STATE_DISABLED = "DISABLED"

    def __init__(self, **kwargs):
        Thread.__init__(self)
        StoppableThread.__init__(self, setted=False)
        SchemaConstructor.__init__(self, CONFIG_CREATE_COMPUTE_ENVIRONMENT)
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.state = self.STATE_ENABLED
        self.__associated_queue = queue.PriorityQueue(maxsize=4)  # Compute maxsize as parameter of CE power
        self.__jobs_current = []
        self.__jobs_done = deque()  # Add Max Len for limiting logs

    def run(self):
        while not self.stop_event.wait(timeout=1):
            if self.state == self.STATE_ENABLED:
                # Handle current jobs
                for idx, job in enumerate(self.__jobs_current):
                    if job.state in (job.STATE_SUCCEEDED, job.STATE_FAILED):
                        self.__jobs_done.append(self.__jobs_current.pop(idx))
                        break
                # Take new jobs
                try:
                    job = self.__associated_queue.get_nowait()
                    self.__jobs_current.append(job)
                    job.start()
                    break
                except queue.Empty:
                    continue

    def is_enabled(self):
        return self.state == self.STATE_ENABLED

    def has_capacity(self):
        return not self.__associated_queue.full()

    def add_job(self, job):
        self.__associated_queue.put_nowait(job)

