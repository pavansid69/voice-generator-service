# src/models/request_models.py
from typing import List
from pydantic import BaseModel

class ScriptRequest(BaseModel):
    text: str
    voice_id: str | None = None

class DialogueRequest(BaseModel):
    inputs: List[ScriptRequest]