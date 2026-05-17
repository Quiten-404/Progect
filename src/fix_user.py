from database import get_DB
from zxcvbn import zxcvbn
import hashlib


def unique_name(name): #Проверка имени на уникальность
    #name = input("Введите имя: ")
    with get_DB() as conn:
        user = conn.execute("SELECT * FROM Users WHERE name = ?", (name,)).fetchone()
    
    if user:
        print(f"Найден: {user['name']} - {user['email']}")

    else:
        print("Пользователь не найден")


def unique_email(email): #Проверка почты на уникальность
    #email = input("Введите email: ")
    with get_DB() as conn:
        user = conn.execute("SELECT * FROM Users WHERE email = ?", (email,)).fetchone()
    
    if user:
        print(f"Почта уже существует: {user['email']}")


    else:
        print("Создаём пользователя...")

def get_password_hash(password):
    """Хеширование пароля"""
    return hashlib.sha256(password.encode()).hexdigest()


def validate_password_strength(password, user_inputs=None):
    """    Проверяет пароль через zxcvbn.  user_inputs - список с именем, фамилией, email пользователя для проверки.    """
    if user_inputs is None:
        user_inputs = []
    
    # Анализируем пароль
    result = zxcvbn(password, user_inputs=user_inputs)
    
    # score - от 0 (очень плохой) до 4 (отличный)
    # Рекомендуют требовать score >= 3
    return result['score'], result['feedback']

def register_user_safe(name, email, password):
    """Регистрация с проверкой сложности и хешированием."""
    
    # 1. Проверяем сложность пароля
    score, feedback = validate_password_strength(password, [name, email])
    if score < 3: # Требуем оценку не ниже "хорошо"
        print(f"Пароль слишком простой! Совет: {feedback['suggestions']}")
        return None

    # 2. Хешируем пароль
    password_hash = get_password_hash(password)
    
    # 3. Сохраняем в БД
    with get_DB() as conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO Users (name, email, password_hash, currency) 
                VALUES (?, ?, ?, 'RUB')
                """, (name, email, password_hash))
            conn.commit()
            print(f"Пользователь {name} зарегистрирован!")
            return True
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                print("❌ Пользователь с таким email уже существует!")
            else:
                print(f"❌ Ошибка: {e}")
            return None
        
def login(name, password):
    user_id = None
    password_hash = get_password_hash(password)
    with get_DB() as conn:
        cur = conn.cursor()
        
        cur.execute("SELECT name, id, email, password_hash FROM users WHERE name = ? AND password_hash = ?",(name,password_hash))
        user = cur.fetchone()

        if user:
            user_id = user[1]
            print(f"✅ Добро пожаловать, {user[0]}, {user_id}!")
            
            return True, user_id 
        else:
            print("❌ Неверное имя пользователя или пароль")
            return False



       






