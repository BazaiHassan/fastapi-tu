from fastapi import FastAPI, status, HTTPException, Depends
from schemas import ExpenseSchema, ExpenseUpdateSchema, ExpenseCreateSchema
from typing import List
from uuid import UUID
from db import Expense, get_db
from sqlalchemy.orm import Session


app = FastAPI(
    title="Expense Tracker API",
    description="A simple API to track expenses",
    version="1.0.1"
)


# Routes
@app.get("/expenses", response_model=List[ExpenseSchema], status_code=status.HTTP_200_OK)
def get_all_expenses(db: Session = Depends(get_db)):
    expenses = db.query(Expense).all()
    return expenses

@app.post("/expenses", response_model=ExpenseSchema, status_code=status.HTTP_201_CREATED)
def add_expense(expense: ExpenseCreateSchema, db: Session = Depends(get_db)):
    new_expense = Expense(**expense.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@app.get("/expenses/{expense_id}", response_model=ExpenseSchema)
def get_expense_by_id(expense_id: UUID, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    return expense

@app.put("/expenses/{expense_id}", response_model=ExpenseSchema)
def update_expense(expense_id: UUID, expense_update: ExpenseUpdateSchema, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    update_data = expense_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense, field, value)
    
    db.commit()
    db.refresh(expense)
    return expense

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: UUID, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    db.delete(expense)
    db.commit()
    return {
        "status_code":status.HTTP_200_OK,
        "detail":f"Expense with ID:{expense_id} is now deleted"
    }