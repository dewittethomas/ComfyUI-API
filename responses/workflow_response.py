from pydantic import BaseModel

class WorkflowAcceptsResponse(BaseModel):
    image: bool = False
    audio: bool = False
    prompt: bool = False

class WorkflowSettingsNodeResponse(BaseModel):
    class_type: str
    key: str

class WorkflowInputNodeResponse(BaseModel):
    class_type: str
    key: str

class WorkflowResponse(BaseModel):
    id: str
    model_id: str
    workflow_file: str

    accepts: WorkflowAcceptsResponse

    settings_nodes: dict[str, WorkflowSettingsNodeResponse]
    input_nodes: dict[str, WorkflowInputNodeResponse]
    output_nodes: dict[str, str]

    custom_image: bool = False
    custom_audio: bool = False