from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.src.db import get_db
from . import models, schemas

router = APIRouter(tags=['Category'], prefix='/category')

@router.get("/list")
async def get_category_list(db: Session = Depends(get_db)):
    categories = db.query(models.CategoryModel).all()
    return {"categories": categories}

@router.post("/add")
async def add_new_category(category_data: schemas.CreateCategory, db: Session = Depends(get_db)):
    # Check if category with the same name already exists
    existing_category = db.query(models.CategoryModel).filter(models.CategoryModel.name == category_data.name).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This Category already registered"
        )
    
    # Create new category
    category_obj = models.CategoryModel(**category_data.model_dump())
    db.add(category_obj)
    db.commit()
    db.refresh(category_obj)

    return {"message": "Category is added successfully", "category": category_obj}