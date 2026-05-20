import sqlite3
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path(__file__).parent.parent / "database" / "finance.db"


@contextmanager
def get_DB():
    conn = sqlite3.connect(DB_PATH) #Открывает соединение с БД
    
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
    
    with get_DB() as conn:
        conn.executescript(finance_sql)
        
    
    print("✅ База данных инициализирована")

def execute_query(query: str, params =()):    
    with get_DB() as conn:
        if params:
            cur = conn.execute(query, params)
        else:
            cur = conn.execute(query)
        return [dict(row) for row in cur.fetchall()]
    
def execute_insert(sql: str, params = ()):
    with get_DB() as conn:
        if params:
            cur = conn.execute(sql, params)
        else:
            cur = conn.execute(sql)
        return cur.lastrowid

def execute_update(sql: str, params = ()):
     with get_DB() as conn:
        if param:
            cur = conn.execute(sql, params)
        else:
            cur = conn.execute(sql)
        return cur.rowcount