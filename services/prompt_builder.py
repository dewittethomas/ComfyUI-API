from models import Workflow, PromptRequest

class PromptBuilder:
    def build(self, workflow: Workflow, request: PromptRequest, nodes: dict) -> dict:
        clip_roles = self._detect_clip_roles(nodes)

        for node_id, node in nodes.items():
            class_type = node.get("class_type")
            inputs = node.get("inputs", {})

            self._apply_settings(workflow, request, class_type, inputs)
            self._apply_generic_inputs(workflow, request, class_type, inputs)
            self._apply_prompt_inputs(workflow, request, node_id, inputs, clip_roles)

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

    def _apply_generic_inputs(self, workflow, request, class_type, inputs):
        for key, config in workflow.input_nodes.model_dump().items():
            if not config:
                continue

            if key in ("positive_prompt", "negative_prompt"):
                continue

            if class_type != config["class_type"]:
                continue

            value = getattr(request, key, None)
            if value is None:
                continue

            inputs[config["key"]] = value
    
    def _apply_prompt_inputs(self, workflow, request, node_id, inputs, clip_roles):
        mapping = {
            "positive_prompt": "positive",
            "negative_prompt": "negative"
        }

        role = clip_roles.get(node_id)
        if not role:
            return

        for key, expected_role in mapping.items():
            if role != expected_role:
                continue

            config = workflow.input_nodes.model_dump().get(key)
            if not config:
                continue

            if config["class_type"] != "CLIPTextEncode":
                continue

            value = getattr(request, key, None)
            if value is None:
                continue

            inputs[config["key"]] = value

    def _detect_clip_roles(self, nodes: dict):
        roles = {}

        for node_id, node in nodes.items():
            if node.get("class_type") != "KSampler":
                continue

            positive = node["inputs"].get("positive")
            negative = node["inputs"].get("negative")

            if isinstance(positive, list):
                roles[positive[0]] = "positive"

            if isinstance(negative, list):
                roles[negative[0]] = "negative"

        return roles