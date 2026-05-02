from typing import List, Optional
import uuid

from models.job import Job
from models.prompt import PromptRequest

from interfaces.job_repository import JobRepository

class JobService:
    def __init__(self, job_repository: JobRepository):
        self.job_repository = job_repository

    # -------------------------
    # CREATE (QUEUE ONLY)
    # -------------------------

    def create(self, request: PromptRequest) -> Job:
        job = Job(
            id=str(uuid.uuid4()),
            workflow_id=request.workflow_id,
            request=request,
            status="queued"
        )

        self.job_repository.save(job)
        return job

    # -------------------------
    # READ
    # -------------------------

    def get_all(self) -> List[Job]:
        return self.job_repository.list()

    def get_by_id(self, job_id: str) -> Optional[Job]:
        return self.job_repository.get(job_id)

    # -------------------------
    # UPDATE
    # -------------------------

    def update(self, job: Job) -> None:
        existing = self.job_repository.get(job.id)
        if not existing:
            raise ValueError(f"Job {job.id} not found")

        self.job_repository.update(job)

    # -------------------------
    # DELETE
    # -------------------------

    def delete(self, job_id: str) -> None:
        self.job_repository.delete(job_id)