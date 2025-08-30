from fastapi import APIRouter

router = APIRouter(tags=['Category'], prefix='/category')

@router.get("/list")
async def get_category_list():
    pass