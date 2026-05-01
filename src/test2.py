from database import get_DB
from fix_user import register_user_safe, login
from add_account import new_account

def test_register():
    name = input("Имя: ")
    email = input("Email: ")
    password = input("Пароль: ")
    #register_user_safe(name, email, password)
    register_success = register_user_safe(name, email, password)
    login(name, password)
    login_success, user_id = login(name, password)
    new_account(register_success, user_id)
    print(user_id, login_success)

def login_test():
    login(name, password)
    login_success, user_id = login(name, password)

test_register()