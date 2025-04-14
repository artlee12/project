from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OperationBase(BaseModel):
    operation_type: str
    input_text: str
    output_text: str

class OperationCreate(OperationBase):
    pass

class Operation(OperationBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True 