import asyncio
import json
import websockets

from services.job_service import JobService

class ComfyWebSocketClient:
    def __init__(self, base_url: str, session, job_service: JobService):
        self.base_url = base_url
        self.session = session
        self.job_service = job_service
        self._ws = None
        self._listen_task = None

    async def connect(self):
        url = f"{self.base_ws_url}/ws?clientId={self.session.client_id}"
        self._ws = await websockets.connect(url)
        self._listen_task = asyncio.create_task(self._listen())

    async def disconnect(self):
        if self._listen_task:
            self._listen_task.cancel()

        if self._ws:
            await self._ws.close()

    async def _listen(self):
        while True:
            msg = await self._ws.recv()

            try:
                data = json.loads(msg)
            except Exception:
                continue

            event_type = data.get("type")
            payload = data.get("data", {})

            if event_type == "status":
                await self._handle_status(payload)

            elif event_type == "executing":
                await self._handle_executing(payload)

    def _handle_status(self, payload: dict):
        exec_info = payload.get("status", {}).get("exec_info", {})
        queue = exec_info.get("queue_remaining")

        if queue is None:
            return

        print("queue:", queue)

    def _handle_executing(self, payload: dict):
        node = payload.get("node")
        prompt_id = payload.get("prompt_id")
        progress = payload.get("progress", 0)

        if not prompt_id:
            return

        job = self.job_service.find_by_prompt_id(prompt_id)
        if not job:
            return

        job.progress = progress or 0.0
        job.current_node = node

        if node is None:
            job.status = "completed"
            job.progress = 1.0

        self.job_service.update(job)