from pydantic import BaseModel
from typing import Any

# Schema for the success response
class SuccessSchema(BaseModel):
    detail: str
    data: Any
