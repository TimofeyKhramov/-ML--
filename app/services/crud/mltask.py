from src.mltask import MLTaskType
from sqlmodel import Session
from typing import List, Optional, Union
from src.transaction import AddTransaction, DebitTransaction
from src.mltask import MLTaskType, MLTaskHistory
from sqlmodel import Session, select
from services.crud import user as UserService

def create_mltask(mltask: MLTaskType, session: Session):
    """
    Create new user.
    
    Args:
        user: User to create
        session: Database session
    
    Returns:
        User: Created user with ID
    """
    try:
        session.add(mltask)
        session.commit()
        session.refresh(mltask)
        return mltask
    except Exception as e:
        session.rollback()
        raise

def get_all_mltasks(session: Session) -> List[MLTaskType]:
    """
    Retrieve all users with their events.
    
    Args:
        session: Database session
    
    Returns:
        List[User]: List of all users
    """
    try:
        statement = select(MLTaskType)
        mltasks = session.exec(statement).all()
        return mltasks
    except Exception as e:
        raise

def get_mltask_by_id(mltask_id: int, session: Session):
    try:
        statement = select(MLTaskType).where(MLTaskType.id == mltask_id)
        mltask = session.exec(statement).first()
        return mltask
    except Exception as e:
        raise



def ml_prediction(user_id,  session: Session):
   
    user = UserService.get_user_by_id(user_id, session)
    if not user:
        raise ValueError(f"Пользователь с ID = {user_id} не найден")
    
    history = MLTaskHistory(
            user_id=user_id,
        )
    session.add(history)
        
    session.commit()
    return history

