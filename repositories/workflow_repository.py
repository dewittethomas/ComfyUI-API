from core.settings import get_settings
from core.json_loader import load_json_file
from models.workflow import Workflow
from typing import List

class WorkflowRepository:
    def __init__(self):
        settings = get_settings()

        raw_workflows = load_json_file(settings.workflows_file)
        self._workflows = [Workflow(**w) for w in raw_workflows]

    def list(self) -> list[Workflow]:
        return self._workflows

    def get(self, workflow_id: str) -> Workflow | None:
        return next((w for w in self._workflows if w.id == workflow_id), None)

    def get_by_model(self, model_id: str) -> List[Workflow]:
        return [w for w in self._workflows if w.model_id == model_id]

    def load_workflow_file(self, workflow_id: str) -> dict | None:
        workflow = self.get(workflow_id)
        if workflow is None:
            return None
        data = load_json_file(workflow.workflow_file)
        if isinstance(data, list):
            return data[0]
        return data