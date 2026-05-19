from fastapi import FastAPI, HTTPException
from src.schemas import UserResponse, AccountResponse, AccountCreate
from src.database import execute_query, execute_insert

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

"""Роуты для аккаунта"""
@app.get("/accounts/{user_id}", response_model=list[AccountResponse])
async def get_account(user_id: int):
    query = "SELECT * FROM Account WHERE user_id = ?"
    result = execute_query(query, (user_id,))
    if not result or len(result) == 0:
        raise HTTPException(status_code=404, detail="Account not found")
    return result

@app.post("/accounts", response_model=AccountResponse, status_code=201)
async def get_account(account: AccountCreate):
    user = execute_query("SELECT id FROM Users WHERE id = ?", (account.user_id,))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    check_acc = execute_query("SELECT id FROM Account WHERE name = ?", (account.name,))
    if check_acc:
        raise HTTPException(status_code=404, detail="Account is busy")
    sql = "INSERT INTO Account (user_id, name, spend_method, balance)VALUES (?, ?, ?, ?)"
    new_id = execute_insert(sql, (account.user_id, account.name, account.spend_method, account.balance))
    new_account = execute_query(
        "SELECT id, user_id, name, spend_method, balance FROM Account WHERE id = ?",(new_id,))
    return new_account[0]
    


"""Роуты для пользователя"""
@app.get("/user/{user_id}",  response_model=UserResponse)
async def get_user(user_id: int):
    sql = "SELECT * FROM Users WHERE id = ?"
    result = execute_query(sql, (user_id,))
    if not result or len(result) == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return result[0]

"""Роуты для транзакций"""
@app.get("/Transaction/{user_id}")
async def get_transactions(user_id: int):
    sql = "SELECT * FROM 'Transaction' WHERE user_id = ?"
    result = execute_query(sql, (user_id,))
    if not result or len(result) == 0:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return result

"""Роуты для категорий"""
@app.get("/categories/{user_id}")
async def get_categories(user_id: int):
    sql = "SELECT * FROM categories WHERE user_id = ?"
    result = execute_query(sql, (user_id,))
    if not result or len(result) == 0:
        raise HTTPException(status_code=404, detail="Categories not found")
    return result