from pydantic import BaseModel
from typing import Optional
import time

from models.prompt import PromptRequest

class Job(BaseModel):
    id: str
    workflow_id: str

    request: PromptRequest  

    status: str = 'queued'
    progress: float = 0.0
    current_node: Optional[str] = None

    result: Optional[dict] = None
    error: Optional[str] = None

    created: int = int(time.time())