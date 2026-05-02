from models import Workflow, PromptRequest

class PromptBuilder:
    def build(self, workflow: Workflow, request: PromptRequest, nodes: dict) -> dict:
        for node in nodes.values():
            class_type = node.get('class_type')
            inputs = node.get('inputs', {})

            self._apply_settings(workflow, request, class_type, inputs)
            self._apply_inputs(workflow, request, class_type, inputs)

        return nodes

    def _apply_settings(self, workflow: Workflow, request: PromptRequest, class_type: str, inputs: dict):
        for key, config in workflow.settings_nodes.model_dump().items():
            if not config:
                continue

            if class_type != config['class_type']:
                continue

            value = getattr(request, key, None)
            if value is None:
                continue

            inputs[config['key']] = value

    def _apply_inputs(self, workflow: Workflow, request: PromptRequest, class_type: str, inputs: dict):
        for key, config in workflow.input_nodes.model_dump().items():
            if not config:
                continue

            if class_type != config['class_type']:
                continue

            value = getattr(request, key, None)
            if value is None:
                continue

            inputs[config['key']] = value