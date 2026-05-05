import asyncio
import json
import websockets
from typing import Optional

from models.execution_status import ExecutionStatus
from models.job import Job
from models.job_status import JobStatus

class ComfyWebSocketClient:
    def __init__(self, base_url: str, session, job_service):
        self.base_url = base_url
        self.session = session
        self.job_service = job_service
        self._ws: Optional[websockets.WebSocketClientProtocol] = None
        self._listen_task: Optional[asyncio.Task] = None
        self._ws_connected = False

    async def connect(self):
        if self._ws_connected:
            return
        try:
            url = f"{self.base_url}?clientId={self.session.client_id}"
            self._ws = await websockets.connect(url)
            self._ws_connected = True
            self._listen_task = asyncio.create_task(self._listen())
        except Exception:
            self._ws_connected = False
            raise

    async def disconnect(self):
        if self._listen_task:
            self._listen_task.cancel()
            try:
                await self._listen_task
            except asyncio.CancelledError:
                pass
        if self._ws and self._ws_connected:
            await self._ws.close()
            self._ws_connected = False

    async def _listen(self):
        while self._ws_connected:
            try:
                msg = await self._ws.recv()
            except websockets.exceptions.ConnectionClosed:
                self._ws_connected = False
                break
            except Exception:
                self._ws_connected = False
                break

            try:
                data = json.loads(msg)
            except Exception:
                continue

            await self._handle_message(data)

    async def _handle_message(self, data): # noqa: S7503
        event_type = data.get("type")
        payload = data.get("data", {})

        if event_type == "execution_start":
            _ = asyncio.create_task(self._handle_execution_start(payload))
        elif event_type == "execution_success":
            _ = asyncio.create_task(self._handle_execution_success(payload))
        elif event_type == "execution_cached":
            _ = asyncio.create_task(self._handle_cached(payload))
        elif event_type == "executing":
            if payload.get("node") is not None:
                _ = asyncio.create_task(self._handle_executing(payload))
        elif event_type == "executed":
            _ = asyncio.create_task(self._handle_executed(payload))

    async def _handle_execution_start(self, payload: dict): # noqa: S7503
        prompt_id = payload.get("prompt_id")
        if not prompt_id or not self.job_service:
            return
        job = self.job_service.find_by_prompt_id(prompt_id)
        if not job:
            return
        for execution in job.executions:
            if execution.prompt_id == prompt_id:
                execution.status = ExecutionStatus.execution_start
                break
        try:
            self.job_service.update(job)
        except Exception:
            pass

    async def _handle_execution_success(self, payload: dict): # noqa: S7503
        prompt_id = payload.get("prompt_id")
        if not prompt_id or not self.job_service:
            return
        job = self.job_service.find_by_prompt_id(prompt_id)
        if not job:
            return
        for execution in job.executions:
            if execution.prompt_id == prompt_id:
                execution.status = ExecutionStatus.executed
                break
        job.status = JobStatus.completed
        try:
            self.job_service.update(job)
        except Exception:
            pass
        try:
            self.job_service.delete(job.id)
        except Exception:
            pass

    async def _handle_executing(self, payload: dict): # noqa: S7503
        prompt_id = payload.get("prompt_id")
        node = payload.get("node")
        if not prompt_id or not self.job_service:
            return
        job = self.job_service.find_by_prompt_id(prompt_id)
        if not job:
            return
        for execution in job.executions:
            if execution.prompt_id == prompt_id:
                execution.current_node = node
                execution.status = ExecutionStatus.executing
                break
        try:
            self.job_service.update(job)
        except Exception:
            pass
        
    async def _handle_executed(self, payload: dict):  # noqa: S7503
        prompt_id = payload.get("prompt_id")
        output = payload.get("output")

        if not prompt_id or not self.job_service:
            return
        
        job = self.job_service.find_by_prompt_id(prompt_id)
        if not job:
            return
        
        for execution in job.executions:
            if execution.prompt_id == prompt_id:
                execution.current_node = payload.get("node")
                execution.result = output
                execution.status = ExecutionStatus.executing
                break

        job.status = JobStatus.in_progress
        
        try:
            self.job_service.update(job)
        except Exception:
            pass

    async def _handle_cached(self, payload: dict):  # noqa: S7503
        prompt_id = payload.get("prompt_id")

        if not prompt_id or not self.job_service:
            return
        
        job = self.job_service.find_by_prompt_id(prompt_id)
        if not job:
            return
        
        for execution in job.executions:
            if execution.prompt_id == prompt_id:
                execution.status = ExecutionStatus.execution_cached
                break

        job.status = JobStatus.in_progress

        try:
            self.job_service.update(job)
        except Exception:
            pass

    def _cleanup_completed_job(self, job: Job):
        try:
            all_completed = all(
                e.status in [ExecutionStatus.executed, ExecutionStatus.execution_cached]
                for e in job.executions
            )
            if all_completed:
                self.job_service.delete(job.id)
        except Exception:
            pass

    def is_connected(self):
        return self._ws_connected

    async def reconnect(self):
        await self.disconnect()
        await self.connect()