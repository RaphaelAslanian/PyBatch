from typing import List

from job import Job
from stoppable_thread import StoppableThread
from threading import Thread


class Scheduler(Thread, StoppableThread):

    def __init__(self, queues, compute_environments, jobs):
        Thread.__init__(self)
        StoppableThread.__init__(self, setted=False)
        self.__queues = queues
        self.__compute_environments = compute_environments
        self.__jobs = jobs
        self.__pending_jobs = {}

    def run(self):
        while not self.stop_event.wait(timeout=0.1):
            for queue_name, queue in self.__queues.items():
                # Case there is a pending job for that queue
                for pending_job in self.__pending_jobs.get(queue_name, []):
                    pending_job_dependencies = self.__find_dependencies(pending_job)
                    # Case dependency has failed
                    if self.__dependency_failed(pending_job_dependencies):
                        pending_job.change_state(Job.STATE_FAILED)
                        self.__pending_jobs[queue_name].remove(pending_job)
                    # Case dependencies have succeeded
                    elif self.__dependencies_succeeded(pending_job_dependencies):
                        for ce_name in queue.get_ordered_compute_environments():
                            ce = self.__compute_environments[ce_name]
                            if ce.has_capacity() and ce.is_enabled():
                                ce.add_job(pending_job)
                                self.__pending_jobs[queue_name].remove(pending_job)
                    if not self.__pending_jobs[queue_name]:
                        self.__pending_jobs.pop(queue_name)
                if not queue.empty():
                    for ce_name in queue.get_ordered_compute_environments():
                        ce = self.__compute_environments[ce_name]
                        if ce.has_capacity() and ce.is_enabled():
                            job = queue.get()
                            if self.__find_dependencies(job):
                                self.__pending_jobs.setdefault(queue_name, []).append(job)
                            else:
                                ce.add_job(job)

    def __find_dependencies(self, job: Job) -> List[Job]:
        """
        Checks whether or not a job

        :param job:
        :return:
        """
        dependencies_jobids = [dependency["jobId"] for dependency in job.dependsOn]
        dependencies_jobs = [j for j in self.__jobs.values() if j.jobId in dependencies_jobids]
        return dependencies_jobs

    def __dependency_failed(self, dependencies: List[Job]) -> Job:
        """

        :param dependencies:
        :return:
        """
        return next((d for d in dependencies if d.state == Job.STATE_FAILED), default=None)

    def __dependencies_succeeded(self, dependencies: List[Job]) -> bool:
        """

        :param dependencies:
        :return:
        """
        return all([j.state == Job.STATE_SUCCEEDED for j in dependencies])
