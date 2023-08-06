import json
from typing import Optional
from datetime import datetime

from .JobStatus import JobStatus

class Job(object):
    def __init__(self, id: str, tenant_id: int, name: str, arguments: dict, status: JobStatus, submit_time: datetime, scheduled_time: Optional[datetime] = None):
        self.id = id
        self.tenant_id = tenant_id
        self.name = name
        self.arguments = arguments
        self.status = status
        self.submit_time = submit_time
        self.scheduled_time = scheduled_time

    def __str__(self):
        return json.dumps(self.__dict__, indent=2, sort_keys=True)
