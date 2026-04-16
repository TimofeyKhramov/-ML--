from fastapi import APIRouter, HTTPException, status, Depends
from  database.database import get_session
from src.user import User
from services.crud import user as UserService
from typing import List, Dict
from src.mltask import MLTaskType
from services.crud.mltask import create_mltask
import logging

# Configure logging
logger = logging.getLogger(__name__)

user_route = APIRouter()

@user_route.post(
    '/signup',
    response_model=Dict[str, str],
    status_code=status.HTTP_201_CREATED,
    summary="User Registration",
    description="Register a new user with email and password")
async def signup(data: User, session=Depends(get_session)) -> Dict[str, str]:
    """
    Create new user account.

    Args:
        data: User registration data
        session: Database session

    Returns:
        dict: Success message

    Raises:
        HTTPException: If user already exists
    """
    try:
        if UserService.get_user_by_login(data.login, session):
            logger.warning(f"Signup attempt with existing email: {data.login}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )

        user = User(
            login=data.login,
            password=data.password)
        UserService.create_user(user, session)
        logger.info(f"New user registered: {data.login}")
        return {"message": "User successfully registered"}

    except Exception as e:
        logger.error(f"Error during signup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )

# @user_route.post('/signin')
# async def signin(data: User, session=Depends(get_session)) -> Dict[str, str]:
#     """
#     Authenticate existing user.

#     Args:
#         form_data: User credentials
#         session: Database session

#     Returns:
#         dict: Success message

#     Raises:
#         HTTPException: If authentication fails
#     """
#     user = UserService.get_user_by_email(data.email, session)
#     if user is None:
#         logger.warning(f"Login attempt with non-existent email: {data.email}")
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    
#     if user.password != data.password:
#         logger.warning(f"Failed login attempt for user: {data.email}")
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong credentials passed")
    
#     return {"message": "User signed in successfully"}

@user_route.get(
    "/get_all_users",
    response_model=List[User],
    summary="Get all users",
    response_description="List of all users"
)
async def get_all_users(session=Depends(get_session)) -> List[User]:
    """
    Get list of all users.

    Args:
        session: Database session

    Returns:
        List[UserResponse]: List of users
    """
    try:
        users = UserService.get_all_users(session)
        logger.info(f"Retrieved {len(users)} users")
        return users
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving users"
        )
    
@user_route.get(
    "/get_user_balance",
    
    summary="Get user balance",
    response_description="User balance"
)
async def get_user_balance(user_id: int, session=Depends(get_session)):
    """
    Get list of all users.

    Args:
        session: Database session

    Returns:
        List[UserResponse]: List of users
    """
    try:
        balance = UserService.get_user_balance(user_id, session)
        # logger.info(f"Retrieved {len(users)} users")
        return {user_id: str(balance)}
    except Exception as e:
        print(1)
        # logger.error({"d": "9"})
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail="Error retrieving users"
    #     )

@user_route.post(
    "/add_balance",
    response_model=List[User],
    summary="Add user balance",
    response_description="User balance"
)
async def add_balance(user_id: int, amount: int,  session=Depends(get_session)):
    """
    Get list of all users.

    Args:
        session: Database session

    Returns:
        List[UserResponse]: List of users
    """
    try:
        UserService.add_balance(user_id, amount, session)
        # logger.info(f"Retrieved {len(users)} users")
        return {"status": "ok"}
    except Exception as e:
        return {"er": "er"}
        # logger.error({"d": "9"})
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail="Error retrieving users"
    #     )

@user_route.post(
    "/debit_balance",
    
    summary="Debit user balance",
    response_description="User balance"
)
async def debit_balance(user_id: int, ml_task_type: str,  session=Depends(get_session)):
    """
    Get list of all users.

    Args:
        session: Database session

    Returns:
        List[UserResponse]: List of users
    """
    try:
        UserService.debit_balance(user_id, session, ml_task_type)
        # logger.info(f"Retrieved {len(users)} users")
        return {"status": "ok"}
    except Exception as e:
        return {"er": "er"}
    
@user_route.get(
    "/get_user_all_transactions",
    
    summary="Debit user balance",
    response_description="User balance"
)
async def get_user_all_transactions(user_id: int,  session=Depends(get_session)):
    """
    Get list of all users.

    Args:
        session: Database session

    Returns:
        List[UserResponse]: List of users
    """
    try:
        tr = UserService.get_user_all_transactions(user_id, session)
        # logger.info(f"Retrieved {len(users)} users")
        return tr
    except Exception as e:
        return {"er": "er"}