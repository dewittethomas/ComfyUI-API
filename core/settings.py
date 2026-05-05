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

    comfyui_host: str = 'localhost'
    comfyui_port: int = 8188

    @property
    def comfyui_url(self) -> AnyUrl:
        return AnyUrl(f"http://{self.comfyui_host}:{self.comfyui_port}")
    
    @property
    def comfyui_ws_url(self) -> AnyUrl:
        return AnyUrl(f"ws://{self.comfyui_host}:{self.comfyui_port}/ws")

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()