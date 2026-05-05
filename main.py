import logging
from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI
from routers import models, workflows, jobs

app = FastAPI()

app.include_router(models.router)
app.include_router(workflows.router)
app.include_router(jobs.router)

app = VersionedFastAPI(
    app,
    version_format='{major}',
    prefix_format='/v{major}'
)