from pathlib import Path
from functools import lru_cache
from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    host: str = '0.0.0.0'
    port: int = 8000

    models_file: Path = BASE_DIR / 'data/models.json'
    workflows_file: Path = BASE_DIR / 'data/workflows.json'

    comfyui_url: AnyUrl = 'http://localhost:8188'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()