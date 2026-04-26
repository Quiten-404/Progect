from database import init_database, get_DB
from fix_user import unique_name, unique_email

init_database()
def test_1():
    with get_DB() as conn:
        cur = conn.cursor(id)
        
        accounts = [
            (1, 'Основной счет', 'CARD', 45000.00),
            (1, 'Наличные', 'CASH', 8500.50),
            (1, 'Сберегательный', 'CARD', 150000.00),
            (1, 'Инвестиционный', 'CARD', 50000.00)
        ]
        
        cur.executemany("""
            INSERT INTO Account (user_id, name, spend_method, balance) 
            VALUES (?, ?, ?, ?)
        """, accounts)
        conn.commit()
        
        print(f"✅ Добавлено {len(accounts)} счетов")

        get_name()
  


def get_user_id():
    cur.execute("select user_id FROM Account WHERE id == ?", id)
    results = cur.fetchall()
    for row in results:
        print(row['name'])        # Основной счет
    
           
        
        

test_1()