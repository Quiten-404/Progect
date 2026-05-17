from pydantic import BaseModel

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