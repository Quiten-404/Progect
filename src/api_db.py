from fastapi import FastAPI
from src.schemas import AccountResponse
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

@app.get("/account/{id}")
async def get_account(id: int):
    query = "SELECT * FROM Account WHERE user_id = ?"
    result = execute_query(query, (id,))
    return result

    