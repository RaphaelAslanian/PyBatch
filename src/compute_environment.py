import queue
from threading import Thread, Event
from time import sleep


class ComputeEnvironment(Thread):

    class State:
        ENABLED = "ENABLED",
        DISABLED = "DISABLED"

    def __init__(self, **kwargs):
        Thread.__init__(self)
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.state = self.State.ENABLED
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
        self.queues.append(queue)

    def remove_queue(self, queue):
        self.queues.remove(queue)

    def __repr__(self):
        return self.computeEnvironmentName

