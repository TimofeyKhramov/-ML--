from database.config import get_settings
from database.database import get_session, init_db, get_database_engine
from services.crud.user import *
from sqlmodel import Session, create_engine, SQLModel
from src.user import User
from src.transaction import AddTransaction
from src.mltask import MLTaskType
from services.crud.mltask import create_mltask

if __name__ == "__main__":
    settings = get_settings()
    print(settings.APP_NAME)
    print(settings.API_VERSION)
    print(f'Debug: {settings.DEBUG}')
    
    print(settings.DB_HOST)
    print(settings.DB_NAME)
    print(settings.DB_USER)
    
    init_db(drop_all=True)
    print('Init db has been success')
    ml_task_cheque = MLTaskType(id=1, name='Cheque_analyzing', cost=25, description='Info from cheque') # создаём ML-задачу
    ml_task_cv = MLTaskType(id=2, name='Computer_vision', cost=15, description='Read images')
    
    test_user = User(login='test1@gmail.com', password='15000000' ) # создаём пользователя
    test_user_2 = User(login='test2@gmail.com', password='6793u')
    test_user_3 = User(login='test3@gmail.com', password='y474686')
    
    engine = get_database_engine()
    
    with Session(engine) as session:
        create_user(test_user, session) # создаём пользователя в БД
        create_mltask(ml_task_cheque, session) # создаём ML-задачу в БД
        create_mltask(ml_task_cv, session)
        create_user(test_user_2, session)
        create_user(test_user_3, session)
        add_balance(user_id=1, amount=50, session=session) # здесь же создаётся AddTransaction для пользователя
        add_balance(user_id=2, amount=60, session=session) 
        add_balance(user_id=3, amount=20, session=session)
        debit_balance(user_id=1, ml_task_type='Cheque_analyzing', session=session) # здесь же создаётся DebitTransaction для пользователя
        debit_balance(user_id=2, ml_task_type='Cheque_analyzing',session=session) 
        debit_balance(user_id=3, ml_task_type='Computer_vision',session=session) 
        balance2 = get_user_balance(user_id=2, session=session) # получаем баланс пользователя
        balance3 = get_user_balance(user_id=3, session=session)
        users = get_all_users(session) # получаем всех пользователей
        all_user_transactions = get_user_all_transactions(user_id=1, session=session) # здесь происходит объединение транзакций пользователя, сортировка по дате создания транзакции


    print('-------')
    print('Пользователи из БД:')        
    for user in users:
        print(user)
    print('-------')
    print('Транзакции пользоватея с ID=1:')     
    for t in all_user_transactions:
        print(t)
    
