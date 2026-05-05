from pydantic import BaseModel, Field
import time

from models.job_status import JobStatus
from models.prompt import PromptRequest
from models.execution import Execution

class Job(BaseModel):
    id: str
    workflow_id: str

    request: PromptRequest

    status: JobStatus = JobStatus.queued

    executions: list[Execution] = Field(default_factory=list)

    created: int = int(time.time())