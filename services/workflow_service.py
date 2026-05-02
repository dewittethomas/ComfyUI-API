from repositories.workflow_repository import WorkflowRepository
from models.workflow import Workflow

class WorkflowService:
    def __init__(self, repository: WorkflowRepository):
        self.repo = repository

    def list_workflows(self) -> list:
        return self.repo.list()

    def get_workflow(self, workflow_id: str) -> Workflow | None:
        return self.repo.get(workflow_id)

    def get_workflows_by_model(self, model_id: str) -> list:
        return self.repo.get_by_model(model_id)

    def load_workflow_file(self, workflow_id: str) -> dict | None:
        return self.repo.load_workflow_file(workflow_id)

    def get_prompt_options(self, workflow_id: str) -> dict:
        workflow = self.get_workflow(workflow_id)
        nodes = self.load_workflow_file(workflow_id)

        if workflow is None or nodes is None:
            return {}

        result = {"settings": {}, "inputs": {}, "outputs": {}}

        for node in nodes.values():
            class_type = node.get("class_type")
            inputs = node.get("inputs", {})
            self._extract_node(class_type, inputs, workflow, result)

        return result

    def _extract_node(self, class_type: str, inputs: dict, workflow: Workflow, result: dict):
        self._extract_settings(class_type, inputs, workflow, result["settings"])
        self._extract_inputs(class_type, inputs, workflow, result["inputs"])
        self._extract_outputs(class_type, inputs, workflow, result["outputs"])

    def _extract_settings(self, class_type: str, inputs: dict, workflow: Workflow, result: dict):
        for key, node_config in workflow.settings_nodes.model_dump().items():
            if not node_config:
                continue

            if class_type == node_config["class_type"]:
                result[key] = inputs.get(node_config["key"])

    def _extract_inputs(self, class_type: str, inputs: dict, workflow: Workflow, result: dict):
        for key, node_config in workflow.input_nodes.model_dump().items():
            if node_config and class_type == node_config["class_type"]:
                result[key] = inputs.get(node_config["key"])

    def _extract_outputs(self, class_type: str, inputs: dict, workflow: Workflow, result: dict):
        for key, node_class in workflow.output_nodes.model_dump().items():
            if node_class and class_type == node_class:
                result[key] = inputs