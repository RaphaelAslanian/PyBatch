import queue
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
        setattr(self, "state", self.STATE_ENABLED)
        self.__associated_queues = []
        self.__jobs_current = []
        self.__jobs_done = deque(maxlen=30)

    def run(self):
        while not self.stop_event.wait(timeout=1):
            if self.state == self.STATE_ENABLED:
                # Handle current jobs
                for idx, job in enumerate(self.__jobs_current):
                    if job.state in (job.STATE_SUCCEEDED, job.STATE_FAILED):
                        self.__jobs_done.append(self.__jobs_current.pop(idx))
                        break
                # Take new jobs
                for q in self.__associated_queues:
                    try:
                        job = q.get_nowait()
                        self.__jobs_current.append(job)
                        job.start()
                        break
                    except queue.Empty:
                        continue

    def add_queue(self, queue):
        # TODO: possibility to insert here instead of appending
        self.__associated_queues.append(queue)

    def remove_queue(self, queue):
        self.__associated_queues.remove(queue)

    def __repr__(self):
        return self.computeEnvironmentName

