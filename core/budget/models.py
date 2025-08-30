from core.src.db import Base
from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class BudgetModel(Base):
    __tablename__ = "budgets"
    
    id = Column(String, primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    period = Column(String(20), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'), nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    user_id = Column(String, ForeignKey('users.id'), nullable=False, index=True)
    
    user = relationship("UserModel", back_populates="budgets")
    category = relationship("CategoryModel")