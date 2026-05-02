from pydantic import BaseModel, Field
import time

class Model(BaseModel):
    id: str
    created: int = Field(default_factory=lambda: int(time.time()))
    object: str = "model"
    owned_by: str = "comfyui"

    model_config = {"extra": "ignore"} 