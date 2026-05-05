from pydantic import BaseModel
from typing import Optional
from models.execution_status import ExecutionStatus

class Execution(BaseModel):
    prompt_id: str

    status: ExecutionStatus = ExecutionStatus.execution_start
    current_node: Optional[str] = None

    result: Optional[dict] = None
    error: Optional[str] = None