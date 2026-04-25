import sqlite3
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path(__file__).parent.parent / "database" / "finance.db"
#DB_PATH ="D:\Progect\database\finance"

@contextmanager
def get_BD():
    conn = sqlite3.connect(DB_PATH) #Открывает соединение с БД
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row #Результаты запросов возвращается как словари
    try:
        yield conn
        conn.commit() #Сохраняет все изменения
    except Exception:
        conn.rollback() #Отменяет изменения при ошибке
        raise
    finally:
        conn.close() #Закрывает соединение



def init_database():
    """Инициализация БД из finance.sql"""
    finance_path = Path(__file__).parent.parent / "database" / "finance.sql" 
    
    with open(finance_path, "r", encoding="utf-8") as f:
        finance_sql = f.read()
    
    with get_BD() as conn:
        conn.executescript(finance_sql)
        
    
    print("✅ База данных инициализирована")