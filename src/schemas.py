from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


# АККАУНТЫ
class AccountCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1, max_length=64)
    spend_method: str
    balance: float = Field(..., ge=0)
    
    @field_validator('spend_method')
    def validate_spend_method(cls, v):
        if v not in ['CARD', 'CASH']:
            raise ValueError('spend_method must be CARD or CASH')
        return v

class AccountResponse(BaseModel):
    id: int
    user_id: int
    name: str
    spend_method: str
    balance: float

class AccountUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=64)
    spend_method: Optional[str] = None
    balance: Optional[float] = Field(None, ge=0)
    
    @field_validator('spend_method')
    def validate_spend_method(cls, v):
        if v is not None and v not in ['CARD', 'CASH']:
            raise ValueError('spend_method must be CARD or CASH')
        return v


# ПОЛЬЗОВАТЕЛИ
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: str
    password_hash: str
    currency: str = "RUB"
    
    @field_validator('email')
    def validate_email(cls, v):
        if '@' not in v or '.' not in v:
            raise ValueError('invalid email format')
        return v.lower()

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[str] = None
    password_hash: Optional[str] = None
    currency: Optional[str] = None
    
    @field_validator('email')
    def validate_email(cls, v):
        if v is not None and ('@' not in v or '.' not in v):
            raise ValueError('invalid email format')
        return v.lower() if v else v

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    currency: str
    created_at: Optional[datetime] = None


# АВТОРИЗАЦИЯ
class UserLogin(BaseModel):
    login: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: str
    password: str = Field(..., min_length=4)
    currency: str = "RUB"
    
    @field_validator('email')
    def validate_email(cls, v):
        if '@' not in v or '.' not in v:
            raise ValueError('invalid email format')
        return v.lower()

class Token(BaseModel):
    access_token: str
    token_type: str


# КАТЕГОРИИ
class CategoryCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1, max_length=64)

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=64)

class CategoryResponse(BaseModel):
    id: int
    user_id: int
    name: str


# ТРАНЗАКЦИИ

class TransactionCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    account_id: int = Field(..., gt=0)
    category_id: int = Field(..., gt=0)
    amount: float = Field(..., gt=0)
    description: Optional[str] = Field(None, max_length=256)
    
    @field_validator('amount')
    def validate_amount(cls, v):
        return round(v, 2)

class TransactionUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = Field(None, max_length=256)
    category_id: Optional[int] = Field(None, gt=0)
    
    @field_validator('amount')
    def validate_amount(cls, v):
        return round(v, 2) if v is not None else v

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    account_id: int
    category_id: int
    amount: float
    description: Optional[str] = None
    transaction_date: datetime