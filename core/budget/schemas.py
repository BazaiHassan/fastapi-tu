from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional


class BudgetBase(BaseModel):
    amount: float = Field(..., ge=0, le=9999999999.99, multiple_of=0.01)
    period: str = Field(..., min_length=1, max_length=20, description="Budget period (e.g., monthly, weekly, daily)")
    start_date: datetime = Field(..., description="Start date of the budget period")
    end_date: datetime = Field(..., description="End date of the budget period")
    

class BudgetCreate(BudgetBase):
    category_id: Optional[UUID] = None
    user_id: UUID
    pass

class BudgetUpdate(BaseModel):
    amount: float = Field(..., ge=0, le=9999999999.99, multiple_of=0.01)
    period: Optional[str] = Field(None, min_length=1, max_length=20)
    category_id: Optional[UUID] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class BudgetResponse(BudgetBase):
    id: UUID
    category_id: Optional[UUID]
    user_id: UUID
    created_at: datetime