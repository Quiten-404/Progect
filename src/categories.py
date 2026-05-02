from database import get_DB

def check_categories(login_success, user_id):
     with get_DB() as conn:
        categories = conn.execute("SELECT * FROM categories WHERE user_id = ?", ("user_id",)).fetchone()
        if categories:
            print(f"✅ Категории уже существуют ({len(categories)} шт.):")
        else:
            print("📂 Добавляем категории...")

            categories_data=[
                (user_id, "Продукты"),
                (user_id, "Транспорт"),
                (user_id, "Кафе и рестораны"),
                (user_id, "Развлечения"),
                (user_id, "Зачисления"),
                ]
            conn.executemany("""INSERT INTO Categories (user_id, name) VALUES (?, ?)""", categories_data)
            conn.commit()
            print(f"   ✅ Добавлено {len(categories_data)} категорий")

