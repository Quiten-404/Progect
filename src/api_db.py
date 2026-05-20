from fastapi import FastAPI, HTTPException, status,  Depends
from src.database import execute_query, execute_insert, execute_update
from src.schemas import (
    UserResponse, UserUpdate, 
    UserRegister, UserLogin, Token,
    AccountResponse, AccountCreate, AccountUpdate,
    TransactionResponse, TransactionCreate, TransactionUpdate,
    CategoryResponse, CategoryCreate, CategoryUpdate
    
)
from src.auth import (
    get_password_hash, verify_password, validate_password_strength,
    create_access_token, get_current_user
)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "FastAPI работает!"}

@app.get("/health")
async def health_check():
    return {"message": "Здоров!"}



"""Роуты для аккаунта"""
@app.get("/accounts/{user_id}", response_model=list[AccountResponse])
async def get_account(user_id: int):
    query = "SELECT * FROM Account WHERE user_id = ?"
    result = execute_query(query, (user_id,))
    if not result or len(result) == 0:
        raise HTTPException(status_code=404, detail="Account not found")
    return result

@app.post("/accounts", response_model=AccountResponse, status_code=201)
async def post_account(account: AccountCreate):
    user = execute_query("SELECT id FROM Users WHERE id = ?", (account.user_id,))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    check_acc = execute_query("SELECT id FROM Account WHERE name = ? AND user_id = ?",(account.name, account.user_id))
    if check_acc:
        raise HTTPException(status_code=404, detail="Account is busy")
    sql = "INSERT INTO Account (user_id, name, spend_method, balance)VALUES (?, ?, ?, ?)"
    new_id = execute_insert(sql, (account.user_id, account.name, account.spend_method, account.balance))
    new_account = execute_query(
        "SELECT id, user_id, name, spend_method, balance FROM Account WHERE id = ?",(new_id,))
    return new_account[0]

@app.put("/accounts/{account_id}", response_model=AccountResponse)
async def update_account(account_id: int, account: AccountUpdate):
    existing = execute_query("SELECT id, user_id, name, spend_method, balance FROM Account WHERE id = ?", (account_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Account not exist")
    updates = []
    params = []

    if account.name is not None:
        updates.append("name = ?")
        params.append(account.name)
    
    if account.spend_method is not None:
        updates.append("spend_method = ?")
        params.append(account.spend_method)
    
    if account.balance is not None:
        updates.append("balance = ?")
        params.append(account.balance)
    
    if not updates:
        return existing[0]

    params.append(account_id)
    sql = f"UPDATE Account SET {', '.join(updates)} WHERE id = ?"
    execute_update(sql, params)
    updated = execute_query("SELECT id, user_id, name, spend_method, balance FROM Account WHERE id = ?",(account_id,))
    return updated[0]

@app.delete("/accounts/{account_id}", status_code=204)
async def delete_account(account_id: int):
    existing = execute_query("SELECT id FROM Account WHERE id = ?", (account_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Account not found")
    execute_update("DELETE FROM Account WHERE id = ?", (account_id,))
    return None


"""Роуты для пользователя"""
@app.get("/users", response_model=list[UserResponse])
async def get_all_users():
    sql = "SELECT id, name, email, currency, created_at FROM Users"
    result = execute_query(sql)
    if not result:
        raise HTTPException(status_code=404, detail="No users found")
    return result


@app.get("/user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    sql = "SELECT id, name, email, currency, created_at FROM Users WHERE id = ?"
    result = execute_query(sql, (user_id,))
    if not result or len(result) == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return result[0]


@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate):
    existing = execute_query("SELECT id FROM Users WHERE id = ?", (user_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    updates = []
    params = []
    if user.name is not None:
        updates.append("name = ?")
        params.append(user.name)
    
    if user.email is not None:
        email_exists = execute_query(
            "SELECT id FROM Users WHERE email = ? AND id != ?",
            (user.email, user_id)
        )
        if email_exists:
            raise HTTPException(status_code=409, detail="Email already in use")
        updates.append("email = ?")
        params.append(user.email)
    
    if user.password_hash is not None:
        updates.append("password_hash = ?")
        params.append(user.password_hash)
    
    if user.currency is not None:
        updates.append("currency = ?")
        params.append(user.currency)
    
    if not updates:
        result = execute_query("SELECT id, name, email, currency, created_at FROM Users WHERE id = ?",(user_id,))
        return result[0]
    params.append(user_id)
    sql = f"UPDATE Users SET {', '.join(updates)} WHERE id = ?"
    execute_update(sql, params)
    updated = execute_query(
        "SELECT id, name, email, currency, created_at FROM Users WHERE id = ?",
        (user_id,)
    )
    return updated[0]


@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int):
    existing = execute_query("SELECT id FROM Users WHERE id = ?", (user_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    execute_update("DELETE FROM Users WHERE id = ?", (user_id,))
    
    return None


@app.get("/users/{user_id}/summary")
async def get_user_summary(user_id: int):
    user = execute_query("SELECT id, name FROM Users WHERE id = ?", (user_id,))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    accounts = execute_query("SELECT id, name, spend_method, balance FROM Account WHERE user_id = ?",(user_id,))
    #статистика по транзакциям
    stats = execute_query("""
        SELECT 
            COUNT(*) as total_transactions,
            SUM(CASE WHEN c.type = 'expense' THEN t.amount ELSE 0 END) as total_expenses,
            SUM(CASE WHEN c.type = 'income' THEN t.amount ELSE 0 END) as total_income
        FROM "Transaction" t
        JOIN Categories c ON t.category_id = c.id
        WHERE t.user_id = ?
    """, (user_id,))
    
    total_balance = execute_query("SELECT SUM(balance) as total FROM Account WHERE user_id = ?",(user_id,))

    return {
        "user": user[0],
        "accounts": accounts,
        "total_balance": total_balance[0]['total'] or 0,
        "statistics": stats[0] if stats else {"total_transactions": 0, "total_expenses": 0, "total_income": 0}
    }

"""Роуты для транзакций"""
@app.get("/transactions/{user_id}", response_model=list[TransactionResponse])
async def get_transactions(user_id: int):
    sql = "SELECT * FROM 'Transaction' WHERE user_id = ?"
    result = execute_query(sql, (user_id,))
    if not result or len(result) == 0:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return result

@app.get("/transaction/{transaction_id}", response_model=TransactionResponse)
async def get_transaction_by_id(transaction_id: int):
    result = execute_query('SELECT id, user_id, account_id, category_id, amount, description, transaction_date FROM "Transaction" WHERE id = ?',(transaction_id,))
    if not result:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return result[0]


@app.post("/transactions", response_model=TransactionResponse, status_code=201)
async def create_transaction(transaction: TransactionCreate):
    user = execute_query("SELECT id FROM Users WHERE id = ?", (transaction.user_id,))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    account = execute_query("SELECT id, balance FROM Account WHERE id = ? AND user_id = ?",(transaction.account_id, transaction.user_id))
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    category = execute_query("SELECT id FROM Categories WHERE id = ? AND user_id = ?",(transaction.category_id, transaction.user_id))
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    cat_type = execute_query("SELECT type FROM Categories WHERE id = ?",(transaction.category_id,))
    current_balance = account[0]['balance']
    if cat_type and cat_type[0]['type'] == 'expense' and transaction.amount > current_balance:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    sql = 'INSERT INTO "Transaction" (user_id, account_id, category_id, amount, description)VALUES (?, ?, ?, ?, ?)'
    new_id = execute_insert(sql, (
        transaction.user_id,
        transaction.account_id,
        transaction.category_id,
        transaction.amount,
        transaction.description or ""))
    if cat_type and cat_type[0]['type'] == 'expense':
        execute_update("UPDATE Account SET balance = balance - ? WHERE id = ?",(transaction.amount, transaction.account_id))
    else:
        execute_update("UPDATE Account SET balance = balance + ? WHERE id = ?",(transaction.amount, transaction.account_id))
    new_transaction = execute_query('SELECT id, user_id, account_id, category_id, amount, description, transaction_date FROM "Transaction" WHERE id = ?',(new_id,))
    return new_transaction[0]


@app.put("/transactions/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(transaction_id: int, transaction: TransactionUpdate):
    existing = execute_query('SELECT id, amount, account_id FROM "Transaction" WHERE id = ?',(transaction_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Transaction not found")
    existing_transaction = existing[0]
    updates = []
    params = []
    if transaction.amount is not None:
        old_amount = existing_transaction['amount']
        new_amount = transaction.amount
        diff = new_amount - old_amount
        execute_update("UPDATE Account SET balance = balance - ? WHERE id = ?",(diff, existing_transaction['account_id']))
        updates.append("amount = ?")
        params.append(transaction.amount)
    
    if transaction.description is not None:
        updates.append("description = ?")
        params.append(transaction.description)
    
    if transaction.category_id is not None:
        updates.append("category_id = ?")
        params.append(transaction.category_id)
    
    if not updates:
        result = execute_query('SELECT id, user_id, account_id, category_id, amount, description, transaction_date FROM "Transaction" WHERE id = ?',(transaction_id,))
        return result[0]
    params.append(transaction_id)
    sql = f'UPDATE "Transaction" SET {", ".join(updates)} WHERE id = ?'
    execute_update(sql, params)
    updated = execute_query('SELECT id, user_id, account_id, category_id, amount, description, transaction_date FROM "Transaction" WHERE id = ?',(transaction_id,))
    return updated[0]


@app.delete("/transactions/{transaction_id}", status_code=204)
async def delete_transaction(transaction_id: int):
    existing = execute_query('SELECT id, amount, account_id FROM "Transaction" WHERE id = ?',(transaction_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Transaction not found")
    transaction_data = existing[0]
    execute_update("UPDATE Account SET balance = balance + ? WHERE id = ?",
        (transaction_data['amount'], transaction_data['account_id']))
    execute_update('DELETE FROM "Transaction" WHERE id = ?', (transaction_id,))
    
    return None

"""Роуты для категорий"""
@app.get("/categories/{user_id}", response_model=list[CategoryResponse])
async def get_categories(user_id: int):
    sql = "SELECT * FROM Categories WHERE user_id = ?"
    result = execute_query(sql, (user_id,))
    if not result or len(result) == 0:
        raise HTTPException(status_code=404, detail="Categories not found")
    return result

@app.get("/category/{category_id}", response_model=CategoryResponse)
async def get_category_by_id(category_id: int):
    result = execute_query("SELECT id, user_id, name FROM Categories WHERE id = ?",(category_id,))
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")
    return result[0]


@app.post("/categories", response_model=CategoryResponse, status_code=201)
async def create_category(category: CategoryCreate):
    user = execute_query("SELECT id FROM Users WHERE id = ?", (category.user_id,))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    existing = execute_query("SELECT id FROM Categories WHERE user_id = ? AND name = ?",(category.user_id, category.name))
    if existing:
        raise HTTPException(status_code=409, detail="Category already exists")
    sql = "INSERT INTO Categories (user_id, name) VALUES (?, ?)"
    new_id = execute_insert(sql, (category.user_id, category.name))
    new_category = execute_query("SELECT id, user_id, name FROM Categories WHERE id = ?",(new_id,))
    return new_category[0]


@app.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, category: CategoryUpdate):
    existing = execute_query("SELECT id, user_id, name FROM Categories WHERE id = ?",(category_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Category not found")
    if category.name is None:
        return existing[0]
    execute_update("UPDATE Categories SET name = ? WHERE id = ?",(category.name, category_id))
    updated = execute_query("SELECT id, user_id, name FROM Categories WHERE id = ?",(category_id,))
    return updated[0]


@app.delete("/categories/{category_id}", status_code=204)
async def delete_category(category_id: int):
    existing = execute_query("SELECT id FROM Categories WHERE id = ?", (category_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Category not found")
    execute_update("DELETE FROM Categories WHERE id = ?", (category_id,))
    
    return None



# ========== РЕГИСТРАЦИЯ И АВТОРИЗАЦИЯ ==========
@app.post("/register", response_model=UserResponse, status_code=201)
async def register(user: UserRegister):
    existing_email = execute_query("SELECT id FROM Users WHERE email = ?", (user.email,))
    if existing_email:
        raise HTTPException(status_code=409, detail="Email already exists")
    existing_name = execute_query("SELECT id FROM Users WHERE name = ?", (user.name,))
    if existing_name:
        raise HTTPException(status_code=409, detail="Username already exists")
    score, feedback = validate_password_strength(user.password, [user.name, user.email])
    if score < 3:
        suggestions = feedback.get('suggestions', ['Используйте более сложный пароль'])
        raise HTTPException(
            status_code=400,
            detail=f"Weak password: {', '.join(suggestions)}"
        )
    password_hash = get_password_hash(user.password)
    sql = "INSERT INTO Users (name, email, password_hash, currency) VALUES (?, ?, ?, ?)"
    new_id = execute_insert(sql, (user.name, user.email, password_hash, user.currency))
    new_user = execute_query(
        "SELECT id, name, email, currency, created_at FROM Users WHERE id = ?",
        (new_id,))
    return new_user[0]


@app.post("/login", response_model=Token)
async def login(user: UserLogin):
    db_user = execute_query("SELECT id, name, email, password_hash, currency FROM Users WHERE email = ? OR name = ?",(user.login, user.login))
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    if not verify_password(user.password, db_user[0]['password_hash']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    access_token = create_access_token(data={"sub": str(db_user[0]['id'])})
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/login/name", response_model=Token)
async def login_by_name(name: str, password: str):
    return await login(UserLogin(login=name, password=password))


@app.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user


@app.get("/check-name/{name}")
async def check_name(name: str):
    user = execute_query("SELECT id FROM Users WHERE name = ?", (name,))
    return {"exists": bool(user), "available": not bool(user)}

@app.get("/check-email/{email}")
async def check_email(email: str):
    user = execute_query("SELECT id FROM Users WHERE email = ?", (email,))
    return {"exists": bool(user), "available": not bool(user)}