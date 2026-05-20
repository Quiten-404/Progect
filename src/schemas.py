from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AccountCreate(BaseModel):
    user_id: int
    name: str
    spend_method: str
    balance: float

class AccountResponse(BaseModel):
    id: int
    user_id: int
    name: str
    spend_method: str
    balance: float

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    spend_method: Optional[str] = None
    balance: Optional[float] = None


class UserCreate(BaseModel):
    name: str
    email: str
    password_hash: str
    currency: str = "RUB"

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password_hash: Optional[str] = None
    currency: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    currency: str
    created_at: Optional[datetime] = None
#________________________________________________________
class UserLogin(BaseModel):
    login: str  # может быть email или name
    password: str

class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    currency: str = "RUB"

class Token(BaseModel):
    access_token: str
    token_type: str
#---------------------------------------------------------

class CategoryCreate(BaseModel):
    user_id: int
    name: str

class CategoryUpdate(BaseModel):
    name: Optional[str] = None

class CategoryResponse(BaseModel):
    id: int
    user_id: int
    name: str


class TransactionCreate(BaseModel):
    user_id: int
    account_id: int
    category_id: int
    amount: float
    description: Optional[str] = None

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    category_id: Optional[int] = None

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    account_id: int
    category_id: int
    amount: float
    description: Optional[str] = None
    transaction_date: datetime
