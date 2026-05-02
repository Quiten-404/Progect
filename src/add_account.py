from database import get_DB

def new_account(register_success, user_id):

    if register_success == True:
        with get_DB() as conn:
            account = conn.execute("SELECT * FROM account WHERE user_id = ?",("user_id",)).fetchone()

            if account:
                print(f"✅ Счета уже существуют ({len(accounts)} шт.):")
            else:
                print("💳 Добавляем счета...")

                accounts_data = [
                (user_id, 'Основной счет', 'CARD', 0),
                (user_id, 'Наличные', 'CASH', 0),
                (user_id, 'Сберегательный', 'CARD', 0),
                (user_id, 'Инвестиционный', 'CARD', 0)
                ]
        
                # Массовая вставка
                conn.executemany("""INSERT INTO Account (user_id, name, spend_method, balance)VALUES (?, ?, ?, ?)""", accounts_data)
                print(f"   ✅ Добавлено {len(accounts_data)} счетов")
                conn.commit()
        
                # Показываем результат
                print("\n📋 Текущие счета:")
                acc = conn.execute("SELECT id, name, balance FROM Account WHERE user_id = ?", (user_id,)).fetchone()
                print(acc)
    else:
        print("Ошибка: регистрация не выполнена")
def add_2_account(login_success, user_id):
    if login_success == True:
        with get_DB() as conn:
            account = conn.execute("SELECT id, name, spend_method, balance FROM account WHERE user_id = ?",(user_id,)).fetchall()

            if account:
                print(f"\n💳 Найдено {len(account)} аккаунтов для user_id {user_id}:")
                print("═" * 50)

                for account in account:
                    acc_id, name, spend_method, balance = account
                    print("\n💳 Информация об аккаунте:")
                    print(f"  ID аккаунта: {acc_id}")
                    print(f"  Владелец (user_id): {user_id}")
                    print(f"  Баланс {name}: {balance} {spend_method}")
                
            else:
                print("❌ Аккаунт не найден для user_id:", user_id)


