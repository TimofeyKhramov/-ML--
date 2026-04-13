from src.user import User
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from typing import List, Optional, Union
from src.transaction import AddTransaction, DebitTransaction
from src.mltask import MLTaskType

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
        statement = select(User).options(
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


def get_user_balance(user_id: int, session: Session) -> int:
   
    user = get_user_by_id(user_id, session)
    if not user:
        raise ValueError(f"Пользователь с id {user_id} не найден")
    return user.balance

def add_balance(user_id: int, amount: int, session: Session) -> User:

    try:
        # Валидация суммы
        if amount <= 0:
            raise ValueError(f"Сумма должна быть больше 0, получено: {amount}")
        
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
        session.refresh(user)
        return user
        
    except Exception as e:
        session.rollback()
        raise

def debit_balance(
    user_id: int, 
    session: Session, 
    ml_task_type: str,  
    description: str = None
) -> None:
    try:
        
        if not MLTaskType.is_valid(session, ml_task_type):
            raise ValueError(f"В настоящий момент ML-задача {ml_task_type} не поддерживается")
        
        user = get_user_by_id(user_id, session)
        if not user:
            raise ValueError(f"Пользователь с id {user_id} не найден")
        
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
        session.refresh(user)
        return user
        
    except Exception as e:
        session.rollback()
        raise

def get_all_add_transactions(session: Session) -> List[AddTransaction]:
    """Получить все транзакции пополнения"""
    statement = select(AddTransaction).order_by(AddTransaction.created_at.desc())
    return session.exec(statement).all()

def get_all_debit_transactions(session: Session) -> List[DebitTransaction]:
    """Получить все транзакции списания"""
    statement = select(DebitTransaction).order_by(DebitTransaction.created_at.desc())
    return session.exec(statement).all()

def get_user_add_transactions(user_id: int, session: Session) -> List[AddTransaction]:
    """Получить все пополнения пользователя"""
    statement = select(AddTransaction).where(
        AddTransaction.creator_id == user_id
    ).order_by(AddTransaction.created_at.desc())
    return session.exec(statement).all()

def get_user_debit_transactions(user_id: int, session: Session) -> List[DebitTransaction]:
    """Получить все списания пользователя"""
    statement = select(DebitTransaction).where(
        DebitTransaction.creator_id == user_id
    ).order_by(DebitTransaction.created_at.desc())
    return session.exec(statement).all()

def get_user_all_transactions(user_id: int, session: Session) -> List[Union[AddTransaction, DebitTransaction]]:
    """
    Получить все транзакции пользователя (пополнения + списания).
    
    Args:
        user_id: ID пользователя
        session: Сессия БД
    
    Returns:
        List[Union[AddTransaction, DebitTransaction]]: Объединённый список транзакций,
        отсортированный по дате создания (сначала новые)
    """
    # Получаем пополнения
    add_statement = select(AddTransaction).where(
        AddTransaction.creator_id == user_id
    )
    add_transactions = session.exec(add_statement).all()
    
    # Получаем списания
    debit_statement = select(DebitTransaction).where(
        DebitTransaction.creator_id == user_id
    )
    debit_transactions = session.exec(debit_statement).all()
    
    # Объединяем и сортируем
    all_transactions = add_transactions + debit_transactions
    all_transactions.sort(key=lambda x: x.created_at, reverse=True)
    
    return all_transactions

