from database import get_DB


def add_transaction(user_id):
    with get_DB() as conn:
        account = conn.execute("SELECT id FROM Account WHERE user_id = ? AND name = ?",(user_id, "Основной счет")).fetchone()
        
        category = conn.execute("SELECT id FROM Categories WHERE user_id = ? AND name = ?", (user_id, "Продукты")).fetchone()
        if not account or not category:
            print("❌ Не найден счёт или категория")
        else:
            print(f"💰 Добавляем транзакцию:")
            print(f"   Счёт: Основной счет (id={account['id']})")
            print(f"   Категория: Продукты (id={category['id']})")
            print(f"   Сумма: 850.50 руб.")
        
            conn.execute("""INSERT INTO "Transaction" (user_id, account_id, category_id, amount, description)VALUES (?, ?, ?, ?, ?)""", 
                         (1, account['id'], category['id'], 850.50, "Покупка продуктов"))
            
            # Обновляем баланс счёта (уменьшаем)
            conn.execute("""UPDATE Account SET balance = balance - ? WHERE id = ?""", (850.50, account['id']))
            
            print("   ✅ Транзакция добавлена, баланс обновлён")
            
            # Показываем новый баланс
            new_balance = conn.execute("SELECT balance FROM Account WHERE id = ?", (account['id'],)).fetchone()
            print(f"\n📊 Новый баланс счёта 'Основной счет': {new_balance['balance']} руб.")
