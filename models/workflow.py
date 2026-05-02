from pydantic import BaseModel
from typing import Optional

class WorkflowAccepts(BaseModel):
    image: bool = False
    audio: bool = False
    prompt: bool = False

class WorkflowSettingsNode(BaseModel):
    class_type: str
    key: str

class WorkflowSettingsNodes(BaseModel):
    fps: Optional[WorkflowSettingsNode] = None
    width: Optional[WorkflowSettingsNode] = None
    height: Optional[WorkflowSettingsNode] = None
    duration: Optional[WorkflowSettingsNode] = None

class WorkflowInputNode(BaseModel):
    class_type: str
    key: str

class WorkflowInputNodes(BaseModel):
    image: Optional[WorkflowInputNode] = None
    audio: Optional[WorkflowInputNode] = None
    positive_prompt: Optional[WorkflowInputNode] = None
    negative_prompt: Optional[WorkflowInputNode] = None

class WorkflowOutputNodes(BaseModel):
    video: Optional[str] = None
    last_frame: Optional[str] = None

class Workflow(BaseModel):
    id: str
    model_id: str
    workflow_file: str
    accepts: WorkflowAccepts
    settings_nodes: WorkflowSettingsNodes
    input_nodes: WorkflowInputNodes
    output_nodes: WorkflowOutputNodes