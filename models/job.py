from pydantic import BaseModel
from typing import Optional, List
import time

from models.prompt import PromptRequest
from models.execution import Execution

class Job(BaseModel):
    id: str
    workflow_id: str

    request: PromptRequest  

    status: str = "queued"

    executions: List[Execution] = []

    created: int = int(time.time())