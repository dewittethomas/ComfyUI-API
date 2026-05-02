from typing import List, Optional
import uuid
import copy

from models.job import Job
from models.prompt import PromptRequest

from interfaces.job_repository import JobRepository

from services.workflow_service import WorkflowService
from services.prompt_builder import PromptBuilder

from clients.comfy_client import ComfyClient
from clients.comfy_session import ComfySession

class JobService:
    def __init__(
        self,
        job_repository: JobRepository,
        workflow_service: WorkflowService,
        comfy_client: ComfyClient,
        comfy_session: ComfySession,
        prompt_builder: PromptBuilder
    ):
        self.job_repository = job_repository
        self.workflow_service = workflow_service
        self.comfy_client = comfy_client
        self.comfy_session = comfy_session
        self.prompt_builder = prompt_builder

    async def create(self, request: PromptRequest) -> Job:
        workflow = self.workflow_service.get_workflow(request.workflow_id)
        nodes = self.workflow_service.load_workflow_file(request.workflow_id)

        if not workflow or not nodes:
            raise ValueError('Invalid workflow')

        nodes = copy.deepcopy(nodes)

        prompt = self.prompt_builder.build(workflow, request, nodes)

        response = await self.comfy_client.queue_prompt(
            prompt,
            self.comfy_session.client_id
        )

        prompt_id = response.get('prompt_id')
        if not prompt_id:
            raise ValueError('ComfyUI did not return prompt_id')

        job = Job(
            id=str(uuid.uuid4()),
            workflow_id=request.workflow_id,
            request=request,
            status='queued'
        )

        self.job_repository.save(job)

        return job

    def get_all(self) -> List[Job]:
        return self.job_repository.list()

    def get_by_id(self, job_id: str) -> Optional[Job]:
        return self.job_repository.get(job_id)

    def update(self, job: Job) -> None:
        existing = self.job_repository.get(job.id)
        if not existing:
            raise ValueError(f"Job {job.id} not found")

        self.job_repository.update(job)

    def delete(self, job_id: str) -> None:
        self.job_repository.delete(job_id)