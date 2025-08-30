from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional


class BudgetBase(BaseModel):
    amount: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, description="Budget amount (positive)")
    period: str = Field(..., min_length=1, max_length=20, description="Budget period (e.g., monthly, weekly, daily)")
    start_date: datetime = Field(..., description="Start date of the budget period")
    end_date: datetime = Field(..., description="End date of the budget period")
    

class BudgetCreate(BudgetBase):
    category_id: Optional[UUID] = None
    user_id: UUID
    pass

class BudgetUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2)
    period: Optional[str] = Field(None, min_length=1, max_length=20)
    category_id: Optional[UUID] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class BudgetResponse(BudgetBase):
    id: UUID
    category_id: Optional[UUID]
    user_id: UUID
    created_at: datetime