from core.settings import get_settings
from core.json_loader import load_json_file
from models.model import Model

class ModelRepository:
    def __init__(self):
        settings = get_settings()

        raw_models = load_json_file(settings.models_file)
        self._models = [Model(**m) for m in raw_models]

    def list(self) -> list[Model]:
        return self._models

    def get(self, model_id: str) -> Model | None:
        return next((m for m in self._models if m.id == model_id), None)