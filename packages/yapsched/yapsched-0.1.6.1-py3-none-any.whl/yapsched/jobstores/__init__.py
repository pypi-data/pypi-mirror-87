# Copyright 2020 Software Factory Labs, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List
from ..util import get_class_logger
from ..job import Job


class JobStore(ABC):
    def __init__(self):
        self._logger = get_class_logger(self)
        self._scheduler = None

    def setup(self):
        pass

    def teardown(self):
        pass

    def get_due_jobs(self, latest: datetime) -> List[Job]:
        jobs = self.get_jobs()
        pending = list(filter(lambda job: job.next_run_time <= latest, jobs))
        return pending

    def get_next_run_time(self) -> Optional[datetime]:
        jobs = self.get_jobs()
        return jobs[0].next_run_time if jobs else None

    @abstractmethod
    def add_job(self, job: Job, replace_existing: bool):
        pass

    @abstractmethod
    def update_job(self, job: Job):
        pass

    @abstractmethod
    def remove_job(self, job_id: str):
        pass

    @abstractmethod
    def remove_all_jobs(self):
        pass

    @abstractmethod
    def get_job(self, job_id: str):
        pass

    @abstractmethod
    def get_jobs(self, pattern: str = None) -> List[Job]:
        pass

    @abstractmethod
    def contains_job(self, job_id: str) -> bool:
        pass


class JobAlreadyExistsException(Exception):
    pass


class JobDoesNotExistException(Exception):
    pass
