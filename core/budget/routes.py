# budget.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.src.db import get_db
from .models import BudgetModel
from .schemas import BudgetCreate, BudgetUpdate, BudgetResponse
from core.auth.jwt_auth import get_current_user_from_cookie

router = APIRouter(tags=['Budget'], prefix='/budget')


@router.get("/list", response_model=list[BudgetResponse])
async def get_budget_list(
    current_user = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    budgets = db.query(BudgetModel).filter(BudgetModel.user_id == str(current_user.id)).all()
    return budgets


@router.post("/add", response_model=BudgetResponse)
async def add_budget(
    request: BudgetCreate,
    current_user = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    budget_obj = BudgetModel(
        **request.model_dump(),
        user_id=str(current_user.id)
    )
    db.add(budget_obj)
    db.commit()
    db.refresh(budget_obj)
    return budget_obj


@router.put("/update/{budget_id}", response_model=BudgetResponse)
async def update_budget(
    budget_id: str,
    request: BudgetUpdate,
    current_user = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    budget = db.query(BudgetModel).filter(BudgetModel.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    if budget.user_id != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    for key, value in request.model_dump(exclude_unset=True).items():
        setattr(budget, key, value)

    db.commit()
    db.refresh(budget)
    return budget


@router.delete("/delete/{budget_id}")
async def delete_budget(
    budget_id: str,
    current_user = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    budget = db.query(BudgetModel).filter(BudgetModel.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    if budget.user_id != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    db.delete(budget)
    db.commit()
    return {"message": "Budget deleted successfully"}