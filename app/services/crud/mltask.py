from src.mltask import MLTaskType
from sqlmodel import Session

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