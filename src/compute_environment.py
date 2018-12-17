import queue
from threading import Thread, Event
from time import sleep

from json_configuration import CONFIG_CREATE_COMPUTE_ENVIRONMENT
from schema_constructor import SchemaConstructor


class ComputeEnvironment(Thread, SchemaConstructor):

    def __init__(self, **kwargs):
        Thread.__init__(self)
        SchemaConstructor.__init__(CONFIG_CREATE_COMPUTE_ENVIRONMENT)
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.queues = []
        self._need_stop = Event()

    def run(self):
        while not self._need_stop.is_set():
            for q in self.queues:
                if self.state == self.State.ENABLED:
                    try:
                        job = q.get_nowait()
                        job.start()
                        break
                    except queue.Empty:
                        continue
            sleep(1)

    def add_queue(self, queue):
        # TODO: possibility to insert here instead of appending
        self.queues.append(queue)

    def remove_queue(self, queue):
        self.queues.remove(queue)

    def __repr__(self):
        return self.computeEnvironmentName

