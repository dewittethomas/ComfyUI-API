import uuid

class ComfySession:
    def __init__(self):
        self.client_id = str(uuid.uuid4())