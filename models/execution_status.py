from enum import Enum

class ExecutionStatus(str, Enum):
    execution_start = "execution_start" 
    execution_cached = "execution_cached"
    executing = "executing"
    executed = "executed"