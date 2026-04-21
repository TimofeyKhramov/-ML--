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

def ml_prediction(user_id, ml_task_type, input_data,  session: Session):
    if not MLTaskType.is_valid(session, ml_task_type):
        raise ValueError
        
    user = UserService.get_user_by_id(user_id, session)
    if not user:
        raise ValueError(f"Пользователь с ID = {user_id} не найден")
    
    prediction_result = '123'

    history = MLTaskHistory(
            user_id=user_id,
             ml_task_type=ml_task_type,
            input_data=input_data,

            prediction_result=prediction_result,
        )
    session.add(history)
        
    session.commit()
    return prediction_result

