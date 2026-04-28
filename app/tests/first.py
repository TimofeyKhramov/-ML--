import sys
import os

# Добавляем корневую папку в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session 
from src.user import User
import pytest



def test_create_user(session: Session):
    """
    Тест создания пользователя с валидными данными.
    
    Аргументы:
        session (Session): Сессия базы данных
    """
    user = User(id=1, email="test@mail.ru", password="1234")
    session.add(user)
    session.commit()