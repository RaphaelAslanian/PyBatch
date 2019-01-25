from asyncio import QueueFull

from stoppable_thread import StoppableThread
from threading import Thread


class Scheduler(Thread, StoppableThread):

    def __init__(self, queues, compute_environments):
        Thread.__init__(self)
        StoppableThread.__init__(self, setted=False)
        self.__queues = queues
        self.__compute_environments = compute_environments

    def run(self):
        while not self.stop_event.wait(timeout=0.1):
            for q in self.__queues.values():
                if not q.empty():
                    for ce_name in q.get_ordered_compute_environments():
                        try:
                            ce = self.__compute_environments[ce_name]
                            if ce.has_capacity() and ce.is_enabled():
                                ce.add_job(q.get())
                        except QueueFull:  # priority queue is full, should not happen
                            continue
                        except KeyError:  # compute env does not exist, should not happen
                            continue
