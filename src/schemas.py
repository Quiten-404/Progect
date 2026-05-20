from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AccountCreate(BaseModel):
    user_id: int
    name: str
    spend_method: str
    balance: float

class AccountResponse(BaseModel):
    """Модель для ответа API"""
    id: int
    user_id: int
    name: str
    spend_method: str
    balance: float

class AccountUpdate(BaseModel):
    """Модель для обновления счёта (все поля опциональны)"""
    name: Optional[str] = None
    spend_method: Optional[str] = None
    balance: Optional[float] = None

class UserResponse(BaseModel):
    """Модель для ответа API (GET запросы)"""
    id: int
    name: str
    email: str
    currency: str
    created_at: Optional[datetime] = None

class TransactionResponse(BaseModel):
    """Модель для ответа API"""
    id: int
    user_id: int
    account_id: int
    category_id: int
    amount: float
    description: Optional[str] = None
    transaction_date: datetime