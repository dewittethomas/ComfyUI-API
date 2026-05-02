from pydantic import BaseModel
from typing import Optional

class Execution(BaseModel):
    prompt_id: str

    status: str = "queued"
    progress: float = 0.0
    current_node: Optional[str] = None

    result: Optional[dict] = None
    error: Optional[str] = None