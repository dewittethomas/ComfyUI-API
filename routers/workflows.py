from fastapi import APIRouter, HTTPException, Depends
from fastapi_versioning import version
from typing import Annotated

from services.workflow_service import WorkflowService
from services.dependencies import get_workflow_service

router = APIRouter()

WorkflowServiceDep = Annotated[WorkflowService, Depends(get_workflow_service)]

@router.get("/workflows", responses={
    200: {"description": "List of available workflows"}
})
@version(1)
async def list_workflows_route(service: WorkflowServiceDep):
    return {
        "object": "list",
        "data": [w.model_dump() for w in service.list_workflows()]
    }

@router.get("/workflows/{workflow_id}", responses={
    200: {"description": "Workflow found"},
    404: {"description": "Workflow not found"}
})
@version(1)
async def get_workflow_by_id_route(workflow_id: str, service: WorkflowServiceDep):
    workflow = service.get_workflow(workflow_id)
    if workflow is None:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")
    return workflow.model_dump()

@router.get("/models/{model_id}/workflows", responses={
    200: {"description": "List of workflows for model"},
    404: {"description": "Model not found"}
})
@version(1)
async def list_model_workflows_route(model_id: str, service: WorkflowServiceDep):
    workflows = service.get_workflows_by_model(model_id)
    if not workflows:
        raise HTTPException(status_code=404, detail=f"No workflows found for model '{model_id}'")
    return {
        "object": "list",
        "data": [w.model_dump() for w in workflows]
    }

@router.get("/workflows/{workflow_id}/options", responses={
    200: {"description": "Workflow options found"},
    404: {"description": "Workflow not found"}
})
@version(1)
async def get_workflow_options_route(workflow_id: str, service: WorkflowServiceDep):
    workflow = service.get_workflow(workflow_id)
    if workflow is None:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")
    return {
        "object": "options",
        "data": service.get_prompt_options(workflow_id)
    }