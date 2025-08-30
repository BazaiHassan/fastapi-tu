from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    default_currency: Optional[str] = "USD"
    language: Optional[str] = "en"
    timezone: Optional[str] = "UTC"
    country: Optional[str] = None
    date_of_birth: Optional[str] = None