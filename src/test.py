from  database import init_database, get_BD
init_database()
def test_1():
    with get_BD() as conn:
        cur = conn.cursor()

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

        
       #conn.commit()
        cur.execute("select name FROM Account")
        results = cur.fetchall()
        for row in results:
  
            # ✅ Правильно - печатает значения
            print(row['name'])        # Основной счет
        
        
           
        
        

test_1()