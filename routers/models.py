from fastapi import APIRouter, HTTPException, Depends
from fastapi_versioning import version
from typing import Annotated

from services.model_service import ModelService
from services.dependencies import get_model_service

router = APIRouter()

ModelServiceDep = Annotated[ModelService, Depends(get_model_service)]

@router.get("/models", responses={
    200: {"description": "List of available models"}
})
@router.get("/models")
@version(1)
async def list_models_route(service: ModelServiceDep):
    models = service.list_models()

    return {
        "object": "list",
        "data": [m.model_dump() for m in models]
    }

@router.get("/models/{model_id}", responses={
    200: {"description": "Model found"},
    404: {"description": "Model not found"}
})
@router.get("/models/{model_id}")
@version(1)
async def get_model_by_id_route(
    model_id: str,
    service: ModelServiceDep
):
    model = service.get_model(model_id)

    if model is None:
        raise HTTPException(status_code=404, detail=f"Model '{model_id}' not found")

    return model.model_dump()