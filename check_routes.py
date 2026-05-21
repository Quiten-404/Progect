from src.api_db import app

print("Зарегистрированные маршруты:")
for route in app.routes:
    print(f"{route.methods} {route.path}")