from pydantic import BaseModel

class ModelResponse(BaseModel):
    id: str
    created: int
    object: str
    owned_by: str