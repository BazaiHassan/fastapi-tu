from core.src.db import Base
from sqlalchemy import Column, String, Boolean, DateTime, Numeric, Date
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Authentication fields
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(100), nullable=True)
    
    # Personal information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=True)
    
    # Preferences and settings
    default_currency = Column(String(3), default="USD")
    monthly_budget = Column(Numeric(10, 2), nullable=True)
    language = Column(String(10), default="en")
    timezone = Column(String(50), default="UTC")
    
    # Status and timestamps
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    expenses = relationship("ExpenseModel", back_populates="user", cascade="all, delete-orphan")
    categories = relationship("CategoryModel", back_populates="user", cascade="all, delete-orphan")
    budgets = relationship("BudgetModel", back_populates="user", cascade="all, delete-orphan")
    
    # Optional: Profile fields
    profile_picture = Column(String(500), nullable=True)
    date_of_birth = Column(String, nullable=True)
    country = Column(String(100), nullable=True)
    