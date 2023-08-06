from typing import Callable

class MarshalJob(object):
    def __init__(self, name: str, execute: Callable[[dict], None]):
        self.name = name
        self.execute = execute
