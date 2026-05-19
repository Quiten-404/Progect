from fastapi import FastAPI, HTTPException
from src.schemas import UserResponse
from src.database import execute_query

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "FastAPI работает!"}

@app.get("/health")
async def health_check():
    return {"message": "Здоров!"}

@app.get("/login")
async def login():
    return {"message": "FastAPI работает!"}

@app.get("/account/{user_id}", response_model=AccountResponse)
async def get_account(user_id: int):
    query = "SELECT * FROM Account WHERE user_id = ?"
    result = execute_query(query, (user_id,))
    if not result or len(result) == 0:
        raise HTTPException(status_code=404, detail="Account not found")
    return result

@app.get("/user/{user_id}",  response_model=UserResponse)
async def get_user(user_id: int):
    sql = "SELECT * FROM Users WHERE id = ?"
    result = execute_query(sql, (user_id,))
    if not result or len(result) == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return result[0]
    
@app.get("/Transaction/{user_id}")
async def get_transactions(user_id: int):
    sql = "SELECT * FROM 'Transaction' WHERE user_id = ?"
    result = execute_query(sql, (user_id,))
    if not result or len(result) == 0:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return result