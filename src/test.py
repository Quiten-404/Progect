# quick_test.py
from database import get_DB
from zxcvbn import zxcvbn
import hashlib


def get_password_hash(password):
    """Хеширование пароля"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_password_strength(password, user_inputs=None):
    """Проверяет пароль через zxcvbn"""
    if user_inputs is None:
        user_inputs = []
    result = zxcvbn(password, user_inputs=user_inputs)
    return result['score'], result['feedback']

def register_user_safe(name, email, password):
    """Регистрация с проверкой сложности и хешированием"""
    # 1. Проверяем сложность пароля
    score, feedback = validate_password_strength(password, [name, email])
    if score < 3:
        print(f"❌ Пароль слишком простой! Оценка: {score}/4")
        print(f"Совет: {feedback['suggestions']}")
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
            print(f"✅ Пользователь {name} зарегистрирован!")
            return True
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                print("❌ Пользователь с таким email уже существует!")
            else:
                print(f"❌ Ошибка: {e}")
            return None

def login(name, password):
    """Авторизация пользователя"""
    password_hash = get_password_hash(password)
    with get_DB() as conn:
        cur = conn.cursor()
        cur.execute("SELECT name, email, password_hash FROM users WHERE name = ? AND password_hash = ?", 
                   (name, password_hash))
        user = cur.fetchone()
        
        if user:
            print(f"✅ Добро пожаловать, {user[0]}!")
            return True
        else:
            print("❌ Неверное имя пользователя или пароль")
            return False

# ============ ТЕСТЫ ============

def test_registration():
    """Тест регистрации нового пользователя"""
    print("\n=== ТЕСТ 1: Регистрация нового пользователя ===")
    test_name = "testuser"
    test_email = "test@example.com"
    test_password = "StrongP@ssw0rd123!"
    
    result = register_user_safe(test_name, test_email, test_password)
    print(f"Результат регистрации: {result}")

def test_weak_password():
    """Тест на слабый пароль"""
    print("\n=== ТЕСТ 2: Проверка слабого пароля ===")
    weak_password = "123456"
    score, feedback = validate_password_strength(weak_password)
    print(f"Пароль '{weak_password}' - оценка: {score}/4")
    print(f"Совет: {feedback['suggestions']}")

def test_strong_password():
    """Тест на сильный пароль"""
    print("\n=== ТЕСТ 3: Проверка сильного пароля ===")
    strong_password = "MySecureP@ssw0rd2024!"
    score, feedback = validate_password_strength(strong_password)
    print(f"Пароль '{strong_password}' - оценка: {score}/4")

def test_duplicate_registration():
    """Тест попытки повторной регистрации"""
    print("\n=== ТЕСТ 4: Повторная регистрация ===")
    test_name = "duplicateuser"
    test_email = "duplicate@example.com"
    test_password = "AnotherP@ss123!"
    
    # Первая регистрация
    register_user_safe(test_name, test_email, test_password)
    
    # Вторая регистрация с тем же email
    register_user_safe(test_name + "2", test_email, "DifferentP@ss456!")

def test_login():
    """Тест авторизации"""
    print("\n=== ТЕСТ 5: Авторизация пользователя ===")
    
    # Сначала регистрируем пользователя
    test_name = "logintest"
    test_email = "login@test.com"
    test_password = "LoginP@ss123!"
    
    register_user_safe(test_name, test_email, test_password)
    
    # Тест успешного входа
    print("\nПопытка входа с правильными данными:")
    login(test_name, test_password)
    
    # Тест с неправильным паролем
    print("\nПопытка входа с неправильным паролем:")
    login(test_name, "wrongpassword")

def test_hash_consistency():
    """Тест консистентности хеширования"""
    print("\n=== ТЕСТ 6: Проверка хеширования паролей ===")
    password = "test123"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    hash3 = get_password_hash(password + "different")
    
    print(f"Хеш пароля '{password}': {hash1}")
    print(f"Хеш повторный: {hash2}")
    print(f"Хеш другого пароля: {hash3}")
    print(f"Хеши совпадают для одинаковых паролей: {hash1 == hash2}")
    print(f"Хеши разные для разных паролей: {hash1 != hash3}")

# ============ ЗАПУСК ТЕСТОВ ============

if __name__ == "__main__":
    print("🚀 ЗАПУСК МИНИМАЛЬНЫХ ТЕСТОВ")
    print("=" * 50)
    
    # Запускаем все тесты
    test_hash_consistency()
    test_weak_password()
    test_strong_password()
    test_registration()
    test_duplicate_registration()
    test_login()
    
    print("\n" + "=" * 50)
    print("✅ Тесты завершены!")