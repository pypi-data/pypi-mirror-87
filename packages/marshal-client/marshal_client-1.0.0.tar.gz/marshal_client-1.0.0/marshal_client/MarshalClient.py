import json
from datetime import datetime
from urllib.parse import urljoin
from typing import Optional, List as ListType

import requests
from websocket import create_connection as Websocket

from .models import Job, JobStatus

class MarshalClient(object):
    def __init__(self, api_key: str, base_url: str):
        self._api_key = api_key
        self._base_url = base_url
        self._requests_session = requests.Session()
        self._requests_session.headers.update({'Authorization': 'Bearer {}'.format(self._api_key)})

    def __url(self, path: str) -> str:
        return urljoin(self._base_url, path)
    
    def __response_to_job(self, data):
        # Dates are from javascript, and are therefore in millliseconds
        submit_time = datetime.fromtimestamp(data['submitTime'] / 1000)
        scheduled_time = datetime.fromtimestamp(data['scheduledTime'] / 1000) if data['scheduledTime'] is not None else None
        return Job(data['id'], data['tenantId'], data['name'], data['arguments'], data['status'], submit_time, scheduled_time)
    
    def submit_job(self, name: str, arguments: dict, scheduled_time: Optional[datetime] = None) -> str:
        request_data = {
            'name': name,
            'arguments': arguments
        }
        if scheduled_time is not None:
            request_data['scheduled_time'] = scheduled_time
        url = self.__url('/v1/jobs')
        response = self._requests_session.post(url, json=request_data)
        response.raise_for_status()
        response_data = response.json()
        return response_data['id']
    
    def wait_for_job_completion(self, job_id: str) -> None:
        url = self.__url('/v1/jobs/{}/status'.format(job_id)).replace('http', 'ws', 1)
        websocket = Websocket(url, header=['Authorization: Bearer {}'.format(self._api_key)])
        while True:
            message = websocket.recv()
            try:
                data = json.loads(message)
            except json.decoder.JSONDecodeError as e:
                raise Exception('Invalid response from server, likely due to an abrupt disconnection')
            status = data['status']
            if not status:
                raise Exception('Invalid status returned from server')
            if status == JobStatus.FINISHED.value:
                return
            if status == JobStatus.FAILED.value:
                raise Exception('Job failed')


    def get_job(self, job_id: str) -> Job:
        url = self.__url('/v1/jobs/{}'.format(job_id))
        response = self._requests_session.get(url)
        response.raise_for_status()
        data = response.json()
        return self.__response_to_job(data)
    
    def submit_job_and_wait_for_completion(self, name: str, arguments: dict):
        job_id = self.submit_job(name, arguments)
        return self.wait_for_job_completion(job_id)
    
    def fetch_pending_job(self, worker_name: str, job_names: ListType[str]) -> Optional[Job]:
        url = self.__url('/v1/dispatchments')
        response = self._requests_session.post(url, params={'workerName': worker_name, 'jobNames': job_names})
        response.raise_for_status()
        data = response.json()
        return self.__response_to_job(data[0]) if len(data) > 0 else None

    def set_dispatchment_status(self, job_id: str, status: JobStatus) -> None:
        url = self.__url('/v1/dispatchments')
        response = self._requests_session.patch(url, params={'jobId': job_id}, json={'status': status})
        response.raise_for_status()
