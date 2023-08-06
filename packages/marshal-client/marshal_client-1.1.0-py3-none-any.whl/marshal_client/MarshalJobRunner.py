import sys
import signal
from time import sleep
from typing import List as ListType

from .MarshalClient import MarshalClient
from .models import Job, JobStatus

SLEEP_TIMEOUT = 0.1

class MarshalJobRunner(object):
    def __init__(self, marshal_client: MarshalClient, worker_name: str, jobs: ListType[Job]):
        self._client = marshal_client
        self._worker_name = worker_name
        self._jobs = jobs
        self._is_running = False
    
    def start(self):
        self._is_running = True

        def stop_running(signal_number, stack):
            print("Stopping MarshalJobRunner...")
            self._is_running = False
        original_sigint_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, stop_running)

        job_names = [job.name for job in self._jobs]
        job_map = {job.name:job.execute for job in self._jobs}
        while self._is_running:
            job = self._client.fetch_pending_job(self._worker_name, job_names)
            if job is None:
                sleep(SLEEP_TIMEOUT)
                continue
            try:
                job_map[job.name](job.arguments)
                self._client.set_dispatchment_status(job.id, JobStatus.FINISHED.value)
            except Exception as e:
                print(e, file=sys.stderr)
                print('Job failed:\n{}'.format(job), file=sys.stderr)
                self._client.set_dispatchment_status(job.id, JobStatus.FAILED.value)
        self._is_running = False
        signal.signal(signal.SIGINT, original_sigint_handler)
 