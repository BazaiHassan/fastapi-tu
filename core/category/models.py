from core.src.db import Base
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime


class CategoryModel(Base):
    __tablename__ = "categories"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    color = Column(String(7), default="#000000")
    icon = Column(String(50), nullable=True)
    is_default = Column(Boolean, default=False)
    
    user_id = Column(String, ForeignKey('users.id'), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    user = relationship("UserModel", back_populates="categories")
    expenses = relationship("ExpenseModel", back_populates="category")