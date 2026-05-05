from enum import Enum

class JobStatus(str, Enum):
    queued = "queued"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"