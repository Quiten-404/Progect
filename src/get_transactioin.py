#Получение всех транзакций с деталями

from database import get_DB

def get_all_transactions():
    with get_DB() as conn:

        query = """SELECT
t.id,
t.amount,
t.description,
t.transaction_date,
u.name AS user_name,
a.name AS account_name,
a.spend_method,
c.name AS category_name
FROM "Transaction" t
JOIN Users u ON t.user_id = u.id
JOIN Account a ON t.account_id = a.id
JOIN Categories c ON t.category_id = c.id
ORDER BY t.transaction_date DESC
"""

        transactions = conn.execute(query).fetchall()
        return transactions

def show_transactions():
    """Красиво выводит транзакции"""
    
    transactions = get_all_transactions()
    
    if not transactions:
        print("❌ Нет ни одной транзакции")
        return
    
    print("=" * 70)
    print("📋 ВСЕ ТРАНЗАКЦИИ")
    print("=" * 70)
    
    for t in transactions:
        print(f"\n💰 Транзакция #{t['id']}")
        print(f"   Пользователь: {t['user_name']}")
        print(f"   Счёт: {t['account_name']} ({t['spend_method']})")
        print(f"   Категория: {t['category_name']}")
        print(f"   Сумма: {t['amount']} руб.")
        print(f"   Описание: {t['description'] or '—'}")
        print(f"   Дата: {t['transaction_date']}")
        print("-" * 70)

show_transactions()