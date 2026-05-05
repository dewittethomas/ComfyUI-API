from typing import List, Dict, Optional

from models.job import Job
from interfaces.job_repository import JobRepository

class InMemoryJobRepository(JobRepository):
    def __init__(self):
        self._jobs: Dict[str, Job] = {}

    def save(self, job: Job) -> None:
        self._jobs[job.id] = job

    def get(self, job_id: str) -> Optional[Job]:
        return self._jobs.get(job_id)

    def list(self) -> List[Job]:
        return list(self._jobs.values())

    def update(self, job: Job) -> None:
        self._jobs[job.id] = job

    def delete(self, job_id: str) -> None:
        self._jobs.pop(job_id, None)

    def find_by_prompt_id(self, prompt_id: str) -> Optional[Job]:
        for job in self._jobs.values():
            for execution in job.executions:
                if execution.prompt_id == prompt_id:
                    return job
        return None