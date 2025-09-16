from core.src.db import Base
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
import uuid
# from sqlalchemy.dialects.postgresql import UUID  # You can remove this unused import
from datetime import datetime

class ExpenseModel(Base):
    __tablename__ = "expenses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(String(255), nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_recurring = Column(Boolean, default=False)
    recurrence_frequency = Column(String(50), nullable=True)
    
    # Foreign keys
    user_id = Column(String, ForeignKey('users.id'), nullable=False, index=True)
    # FIX: Change from UUID to String to match categories.id
    category_id = Column(String, ForeignKey('categories.id'), nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("UserModel", back_populates="expenses")
    category = relationship("CategoryModel", back_populates="expenses")
    
    # Optional fields
    currency = Column(String(3), default="USD")
    payment_method = Column(String(50), nullable=True)
    receipt_url = Column(String(500), nullable=True)
    tags = Column(String(255), nullable=True)