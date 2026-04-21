from src.user import User
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from typing import List, Optional, Union
from src.transaction import AddTransaction, DebitTransaction
from src.mltask import MLTaskType, MLTaskHistory

def get_all_users(session: Session) -> List[User]:
    """
    Retrieve all users with their events.
    
    Args:
        session: Database session
    
    Returns:
        List[User]: List of all users
    """
    try:
        statement = select(User).options(
            selectinload(User.add_transactions).selectinload(AddTransaction.creator),
            selectinload(User.debit_transactions).selectinload(DebitTransaction.creator)).order_by(User.created_at.desc())
        users = session.exec(statement).all()
        return users
    except Exception as e:
        raise

def get_user_by_id(user_id: int, session: Session) -> Optional[User]:
    """
    Get user by ID.
    
    Args:
        user_id: User ID to find
        session: Database session
    
    Returns:
        Optional[User]: Found user or None
    """
    try:
        statement = select(User).where(User.id == user_id).options(
            selectinload(User.add_transactions).selectinload(AddTransaction.creator),
            selectinload(User.debit_transactions).selectinload(DebitTransaction.creator))
        user = session.exec(statement).first()
        return user
    except Exception as e:
        raise

def get_user_by_login(login: str, session: Session) -> Optional[User]:
    """
    Get user by email.
    
    Args:
        email: Email to search for
        session: Database session
    
    Returns:
        Optional[User]: Found user or None
    """
    try:
        statement = select(User).where(User.login == login).options(
            selectinload(User.add_transactions).selectinload(AddTransaction.creator),
            selectinload(User.debit_transactions).selectinload(DebitTransaction.creator))
        user = session.exec(statement).first()
        return user
    except Exception as e:
        raise

def create_user(user: User, session: Session) -> User:
    """
    Create new user.
    
    Args:
        user: User to create
        session: Database session
    
    Returns:
        User: Created user with ID
    """
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except Exception as e:
        session.rollback()
        raise

def delete_user(user_id: int, session: Session) -> bool:
    """
    Delete user by ID.
    
    Args:
        user_id: User ID to delete
        session: Database session
    
    Returns:
        bool: True if deleted, False if not found
    """
    try:
        user = get_user_by_id(user_id, session)
        if user:
            session.delete(user)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        raise

def delete_number_of_users(user_id: List[int], session: Session) -> bool:
    """
    Delete user by ID.
    
    Args:
        user_id: User ID to delete
        session: Database session
    
    Returns:
        bool: True if deleted, False if not found
    """
    try:
        for i in range(len(user_id)):
            user = get_user_by_id(user_id[i], session)
            if user:
                session.delete(user)
        session.commit()        
        return True
    except Exception as e:
        session.rollback()
        raise


def get_user_balance(user_id: int, session: Session) -> int:
   
    user = get_user_by_id(user_id, session)
    return user.balance

def add_balance(user_id: int, amount: int, session: Session) -> User:

    try:
        # Валидация суммы
        if amount <= 0:
            raise ValueError(f"Сумма пополнения должна быть больше 0, получено: {amount}")
        
        # Получаем пользователя
        user = get_user_by_id(user_id, session)
        if not user:
            raise ValueError(f"Пользователь с id {user_id} не найден")
        
        # Создаём транзакцию
        transaction = AddTransaction(
            amount=amount,
            creator_id=user_id
        )
        
        # Обновляем баланс пользователя
        user.balance += amount
        
        # Сохраняем всё в БД
        session.add(transaction)
        session.commit()
        # session.refresh(user)
        return get_user_by_id(user_id, session)
        
    except Exception as e:
        session.rollback()
        raise

def debit_balance(
    user_id: int, 
    session: Session, 
    ml_task_type: str,  
    description: str = None,
) -> User:
    try:
        
        user = get_user_by_id(user_id, session)
        if not user:
            raise ValueError(f"Пользователь с ID = {user_id} не найден")
        
        total_cost = MLTaskType.get_cost(session, ml_task_type)
        
        if user.balance < total_cost:
            raise ValueError(
                f"Не хватает средств. Текущий баланс: {user.balance}, "
                f"Сумма, необходимая для выполнения операции: {total_cost} "
            )
        
        
        
        transaction = DebitTransaction(
            ml_task_type=ml_task_type, 
            creator_id=user_id,
            amount = total_cost
        )
        
        user.balance -= total_cost
        session.add(transaction)
        session.commit()
        # session.refresh(user)
        return get_user_by_id(user_id, session)
        
    except Exception as e:
        session.rollback()
        raise

def get_user_add_transactions(user_id: int, session: Session):
    user = get_user_by_id(user_id, session)
    return user.add_transactions

def get_user_debit_transactions(user_id: int, session: Session):
    user = get_user_by_id(user_id, session)
    return user.debit_transactions

def get_user_all_transactions(user_id: int, session: Session):
    user = get_user_by_id(user_id, session)
    return sorted(user.debit_transactions+user.add_transactions, key=lambda x: x.created_at, reverse=True)

def get_user_ml_predictions(user_id: int, session: Session):
    user = get_user_by_id(user_id, session)
    return user.mlhistory


