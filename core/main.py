from fastapi import FastAPI, status, HTTPException
from schemas import ExpenseSchema, ExpenseUpdateSchema, ExpenseCreateSchema
from typing import List
from uuid import UUID, uuid4


app = FastAPI(
    title="Expense Tracker API",
    description="A simple API to track expenses",
    version="1.0.1"
)

# Database
db = []


# Routes
@app.get("/expenses", response_model=List[ExpenseSchema], status_code=status.HTTP_200_OK)
def get_all_expenses():
    return db

@app.post("/expenses", response_model=ExpenseSchema, status_code=status.HTTP_201_CREATED)
def add_expense(expense: ExpenseCreateSchema):
    new_expense = ExpenseSchema(id=uuid4(), **expense.model_dump())
    db.append(new_expense)
    return new_expense

@app.get("/expenses/{expense_id}", response_model=ExpenseSchema)
def get_expense_by_id(expense_id: UUID):
    for expense in db:
        if expense.id == expense_id:
            return expense
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Expense not found"
    )

@app.put("/expenses/{expense_id}", response_model=ExpenseSchema)
def update_expense(expense_id: UUID, expense_update: ExpenseUpdateSchema):
    for index, expense in enumerate(db):
        if expense.id == expense_id:
            update_data = expense_update.model_dump(exclude_unset=True)
            updated_expense = expense.copy(update=update_data)
            db[index] = updated_expense
            return updated_expense
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Expense not found"
    )

@app.delete("/expenses/{expense_id}", response_model=ExpenseSchema)
def delete_expense(expense_id: UUID):
    for index, expense in enumerate(db):
        if expense.id == expense_id:
            return db.pop(index)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Expense not found"
    )