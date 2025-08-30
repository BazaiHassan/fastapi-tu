from fastapi import APIRouter

router = APIRouter(tags=['Expense'], prefix='/expense')

@router.get("/list")
async def get_expense_list():
    pass