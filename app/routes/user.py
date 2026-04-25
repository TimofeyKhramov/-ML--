from fastapi import APIRouter, HTTPException, status, Depends
from  database.database import get_session
from src.user import User
from src.u_s import UserCreate
from services.crud import user as UserService
from typing import List, Dict
from src.mltask import MLTaskType
from services.crud import mltask as MLTaskService
import logging

# Configure logging
logger = logging.getLogger(__name__)

user_route = APIRouter()


# GET-ЗАПРОСЫ
@user_route.get('/profile/{user_id}', response_model=User)
async def get_profile(
    user_id: int,
    session = Depends(get_session)
) -> User:
    """
    Get user profile by ID.
    """
    try:
        user = UserService.get_user_by_id(user_id, session)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return User(
            id=user.id,
            login=user.login,
            balance=user.balance,
            created_at=user.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting profile"
        )
    
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
    response_model=Dict[str, int],
    summary="Get user balance",
    response_description="User balance"
)
async def get_user_balance(user_id: int, session=Depends(get_session)):
    try:
        user = UserService.get_user_by_id(user_id, session)
       
        if not user:
            logger.warning(f"User {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь с ID {user_id} не найден"
            )
        
        balance = user.balance
        logger.info(f"Balance for user {user_id}: {balance}")
        return {f"Баланс пользователя с ID={user_id}": balance}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting balance for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


    
@user_route.get(
    "/get_user_by_id",
    summary="Get user by ID",
    response_description="User info"
)
async def get_user_by_id(user_id: int, session=Depends(get_session)):
 
    try:
        user = UserService.get_user_by_id(user_id, session)
        if not user:
            logger.warning(f"User {user_id} not found"),
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь с ID {user_id} не найден"
            )
        logger.info(f"User {user_id} retrieved successfully")  # 
        return user
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error retrieving user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
@user_route.get(
    "/get_user_add_transactions",
    summary="Get user add transactions",
    response_description="User add transactions"
)
async def get_user_add_transactions(user_id: int, session=Depends(get_session)):
    try:
        user = UserService.get_user_by_id(user_id, session)
        if not user:
            logger.warning(f"User {user_id} not found"),
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь с ID {user_id} не найден"
            )
        transactions = user.add_transactions
        logger.info(f"User with ID = {user_id} add transactions retrieved successfully")
        return transactions
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting add transactions for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@user_route.get(
    "/get_user_debit_transactions",
    summary="Get user debit transactions",
    response_description="User debit transactions"
)
async def get_user_debit_transactions(user_id: int, session=Depends(get_session)):
    try:

        user = UserService.get_user_by_id(user_id, session)
        if not user:
            logger.warning(f"User {user_id} not found"),
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь с ID {user_id} не найден"
            )
        transactions = user.debit_transactions
        logger.info(f"User with ID = {user_id} debit transactions retrieved successfully")
        return transactions
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting debit transactions for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@user_route.get(
    "/get_user_all_transactions",
    summary="Get user all transactions",
    response_description="User all transactions"
)
async def get_user_all_transactions(user_id: int, session=Depends(get_session)):
    try:

        user = UserService.get_user_by_id(user_id, session)
        if not user:
            logger.warning(f"User {user_id} not found"),
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь с ID {user_id} не найден"
            )
        transactions = user.add_transactions+user.debit_transactions
        logger.info(f"User with ID = {user_id} all transactions retrieved successfully")
        return sorted(transactions, key=lambda x: x.created_at, reverse=True)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting all transactions for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

    
#POST-ЗАПРОСЫ
@user_route.post(
    '/signup',
    response_model=Dict[str, str],
    status_code=status.HTTP_201_CREATED,
    summary="User Registration",
    description="Register a new user with login and password")
async def signup(data: User, session=Depends(get_session)) -> Dict[str, str]:
 
    try:
        if UserService.get_user_by_login(data.login, session):
            logger.warning(f"Signup attempt with existing login: {data.login}")
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

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error during signup: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )

@user_route.post('/signin')
async def signin(data: User, session=Depends(get_session)) -> Dict[str, object]:

    user = UserService.get_user_by_login(data.login, session)
    if user is None:
        logger.warning(f"Login attempt with non-existent login: {data.login}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with login {data.login} does not exist")
    
    if user.password != data.password:
        logger.warning(f"Failed login attempt for user: {data.login}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong password")
    
    return {"message": "User signed in successfully", "user_id": user.id}

@user_route.post(
    "/add_balance",
    response_model=Dict[str, int],
    summary="Add user balance",
    response_description="User balance"
)
async def add_balance(user_id: int, amount: int,  session=Depends(get_session)):
  
    try:
        user = UserService.add_balance(user_id, amount, session)
        if not user:
            logger.warning(f"User {user_id} not found"),
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь с ID {user_id} не найден"
            )
        new_balance = user.balance
        
        logger.info(f"Added {amount} to user {user_id}, new balance: {new_balance}")
        
        return {
            "user_id": user_id,
            "added_amount": amount,
            "new_balance": new_balance
        }
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error adding balance to user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


#DELETE-ЗАПРОСЫ
@user_route.delete(
    "/delete_user",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user by ID",
    response_description="User deleted successfully"
)
async def delete_user(
    user_id: int,
    session = Depends(get_session)
):
    """
    Delete a user by their ID.
    
    Args:
        user_id: User ID to delete
        session: Database session
    
    Returns:
        None (204 No Content)
    
    Raises:
        HTTPException: If user not found
    """
    try:
        success = UserService.delete_user(user_id, session)
        if not success:
            logger.warning(f"User with id {user_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        logger.info(f"User with id {user_id} deleted successfully")
        return None  # 204 No Content
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting user"
        )
        
