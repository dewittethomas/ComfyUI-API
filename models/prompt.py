from pydantic import BaseModel
from typing import Optional

class PromptRequest(BaseModel):
    model_id: str
    workflow_id: str

    positive_prompt: Optional[str] = None
    negative_prompt: Optional[str] = None
    image: Optional[str] = None
    audio: Optional[str] = None

    custom_image: bool = False
    custom_audio: bool = False

    fps: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None