

from sqlmodel import Session 
from src.user import User
from src.transaction import AddTransaction
import pytest



def test_create_user(session: Session):
    """
    Тест создания пользователя с валидными данными.
    
    Аргументы:
        session (Session): Сессия базы данных
    """
    user = User(id=1, login="test1@mail.ru", password="123456")
    session.add(user)
    session.commit()

# def test_delete_user(session: Session):
#     """
#     Тест удаления пользователя.
    
#     Аргументы:
#         session (Session): Сессия базы данных
#     """
#     test_create_user(session)
#     user = session.get(User, 1)
#     assert user is not None, "Пользователь с id=1 не найден"  # Fixed incorrect ID in error message

#     session.delete(user)
#     session.commit()

#     deleted_user = session.get(User, 1)
#     assert deleted_user is None, "Пользователь не был удален"


