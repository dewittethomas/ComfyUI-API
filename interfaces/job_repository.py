from abc import ABC, abstractmethod
from typing import List, Optional

from models.job import Job

class JobRepository(ABC):
    
    @abstractmethod
    def save(self, job: Job) -> None:
        pass

    @abstractmethod
    def get(self, job_id: str) -> Job | None:
        pass

    @abstractmethod
    def list(self) -> List[Job]:
        pass

    @abstractmethod
    def update(self, job: Job) -> None:
        pass

    @abstractmethod
    def delete(self, job_id: str) -> None:
        pass

    @abstractmethod
    def find_by_prompt_id(self, prompt_id: str) -> Optional[Job]:
        pass