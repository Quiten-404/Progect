from database import get_DB
from fix_user import register_user_safe, login
from add_account import new_account
from categories import check_categories
from add_account import add_2_account
from transaction import add_transaction

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

def categories_test():
    login_success, user_id = login(name, password)
    check_categories(login_success, user_id)
    
def account_test():
    login_success, user_id = login(name, password)
    add_2_account(login_success, user_id)

def add_transaction_test():
    login_success, user_id = login(name, password)
    add_transaction(user_id)
password = "FFF181fff"
name = "Alex"
#categories_test()
add_transaction_test()