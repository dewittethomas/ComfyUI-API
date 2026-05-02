import httpx
from typing import Any

class ComfyClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')

    async def queue_prompt(self, prompt: dict) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f'{self.base_url}/prompt',
                json=prompt
            )
            response.raise_for_status()

            data = response.json()
            return data['prompt_id']

    async def get_history(self, prompt_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f'{self.base_url}/history/{prompt_id}'
            )
            response.raise_for_status()

            return response.json()

    async def get_queue(self) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.base_url}/queue')
            response.raise_for_status()

            return response.json()