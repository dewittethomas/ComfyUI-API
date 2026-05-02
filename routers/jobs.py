from typing import Annotated

from fastapi import APIRouter, Depends, status

from models.prompt import PromptRequest

from services.job_service import JobService
from services.dependencies import get_job_service

router = APIRouter()

JobServiceDep = Annotated[JobService, Depends(get_job_service)]


@router.post(
    "/jobs",
    status_code=status.HTTP_202_ACCEPTED,
    responses={202: {"description": "Job created successfully"}}
)
async def create_job(
    request: PromptRequest,
    service: JobServiceDep
):
    job = await service.create(request)

    return {
        "object": "job",
        "data": job.model_dump()
    }


@router.get("/jobs")
def list_jobs(service: JobServiceDep):
    jobs = service.get_all()

    return {
        "object": "list",
        "data": [j.model_dump() for j in jobs]
    }