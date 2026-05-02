from repositories.model_repository import ModelRepository

class ModelService:
    def __init__(self, repository: ModelRepository):
        self.repo = repository

    def list_models(self):
        return self.repo.list()

    def get_model(self, model_id: str):
        model = self.repo.get(model_id)

        if not model:
            return None

        return model