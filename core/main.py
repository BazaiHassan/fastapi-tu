from fastapi import FastAPI, status, Body, Path, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Expense Tracker API",
    description="A simple API to track expenses",
    version="1.0.0"
)

# Database
db = []

# Routes for expenses
@app.get("/expenses", status_code=status.HTTP_200_OK)
def get_all_expenses():
    return JSONResponse(
        content={"data": db},
        status_code=status.HTTP_200_OK
    )

@app.post("/expenses", status_code=status.HTTP_201_CREATED)
def add_expense(description: str = Body(min_length=2), amount: int = Body()):
    new_id = len(db) + 1
    new_expense = {
        "id": new_id,
        "description": description,
        "amount": amount
    }
    db.append(new_expense)
    
    return JSONResponse(
        content={"data": new_expense},
        status_code=status.HTTP_201_CREATED
    )

@app.get("/expenses/{id}", status_code=status.HTTP_200_OK)
def get_expense_by_id(id: int = Path(..., gt=0)):
    for expense in db:
        if expense["id"] == id:
            return JSONResponse(
                content={"data": expense},
                status_code=status.HTTP_200_OK
            )
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Expense not found"
    )

@app.put("/expenses/{id}", status_code=status.HTTP_200_OK)
def update_expense(
    id: int = Path(..., gt=0),
    description: str = Body(min_length=2),
    amount: int = Body()
):
    for expense in db:
        if expense["id"] == id:
            expense["description"] = description
            expense["amount"] = amount
            
            return JSONResponse(
                content={"data": expense},
                status_code=status.HTTP_200_OK
            )
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Expense not found"
    )

@app.delete("/expenses/{id}", status_code=status.HTTP_200_OK)
def delete_expense(id: int = Path(..., gt=0)):
    for index, expense in enumerate(db):
        if expense["id"] == id:
            deleted_expense = db.pop(index)
            return JSONResponse(
                content={"data": deleted_expense},
                status_code=status.HTTP_200_OK
            )
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Expense not found"
    )