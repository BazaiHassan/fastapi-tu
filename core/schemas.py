# schemas.py
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Optional

# Schemas
class ExpenseBaseSchema(BaseModel):
    description: str = Field(..., min_length=2)
    amount: int = Field(..., gt=0)

class ExpenseCreateSchema(ExpenseBaseSchema):
    pass

class ExpenseUpdateSchema(BaseModel):
    description: Optional[str] = Field(None, min_length=2)
    amount: Optional[int] = Field(None, gt=0)

class ExpenseSchema(ExpenseBaseSchema):
    id: UUID = Field(default_factory=uuid4)