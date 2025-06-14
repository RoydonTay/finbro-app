from typing import Any, Optional
from pydantic import BaseModel

class ClassifyRequest(BaseModel):
    text: str


class ClassifyResponse(BaseModel):
    label: str
    scroe: float
