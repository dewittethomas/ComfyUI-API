from core.settings import get_settings

from clients.comfy_client import ComfyClient

from clients.comfy_session import ComfySession

from repositories.model_repository import ModelRepository
from .model_service import ModelService

from repositories.workflow_repository import WorkflowRepository
from .workflow_service import WorkflowService

from interfaces.job_repository import JobRepository
from .job_service import JobService
from repositories.in_memory_job_repository import InMemoryJobRepository

from .prompt_builder import PromptBuilder

# Singleton Instances
_comfy_client: ComfyClient | None = None
_comfy_session: ComfySession | None = None
_job_repo: JobRepository | None = None
_job_service: JobService | None = None

# ComfyUI Client
def get_comfy_client() -> ComfyClient:
    global _comfy_client

    if _comfy_client is None:
        settings = get_settings()
        _comfy_client = ComfyClient(settings.comfyui_url)

    return _comfy_client

# ComfyUI Session
def get_comfy_session() -> ComfySession:
    global _comfy_session

    if _comfy_session is None:
        _comfy_session = ComfySession()

    return _comfy_session

# Models
def get_model_repository():
    return ModelRepository()

def get_model_service():
    repo = get_model_repository()
    return ModelService(repo)

# Workflows
def get_workflow_repository():
    return WorkflowRepository()

def get_workflow_service():
    repo = get_workflow_repository()
    return WorkflowService(repo)

# Jobs
def get_job_repository():
    global _job_repo

    if _job_repo is None:
        _job_repo = InMemoryJobRepository() 

    return _job_repo

def get_job_service():
    global _job_service

    if _job_service is None:
        _job_service = JobService(
            get_job_repository(),
            get_workflow_service(),
            get_comfy_client(),
            get_comfy_session(),
            get_prompt_builder()
        )

    return _job_service

# Prompt Builder

def get_prompt_builder():
    return PromptBuilder()

