from fastapi import APIRouter, HTTPException, status, Depends
from  database.database import get_session
from src.user import User
from services.crud import user as UserService
from typing import List, Dict
from src.mltask import MLTaskType
from services.crud import mltask as MLtaskService
import logging

# Configure logging
logger = logging.getLogger(__name__)

mltask_route = APIRouter()

@mltask_route.get(
    "/get_all_mltasks",
    response_model=List[MLTaskType],
    summary="Get all ML tasks",
    response_description="List of all ML tasks"
)
async def get_all_mltasks(
    session = Depends(get_session)
) -> List[MLTaskType]:
    """
    Get list of all ML tasks.
    """
    try:
        mltasks = MLtaskService.get_all_mltasks(session)
        logger.info(f"Retrieved {len(mltasks)} ML tasks")
        return mltasks
    except Exception as e:
        logger.error(f"Error retrieving ML tasks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving ML tasks"
        )
    
@mltask_route.post(
    "/predict",
    response_model=Dict[str, object],
    summary="Get all mltasks",
    response_description="List of all mltasks")
async def predict(
    user_id: int, 
    mltasktype: str, 
    input_data = '123',
    session = Depends(get_session)
):
 
    try:
        prediction_result = MLtaskService.ml_prediction(user_id, mltasktype, input_data, session)
        user = UserService.debit_balance(user_id, session, mltasktype)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
       
        
        
        logger.info(f"ML task '{mltasktype}' completed for user {user_id}")
      
        return {
            "status": "success",
            "user_id": user_id,
            "task_type": mltasktype,
            "new_balance": user.balance,
            "result": prediction_result
        }
        
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing ML task for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    

@mltask_route.get(
    "/history",
    summary="Get user prediction history ",
    response_description="User predictions"
)
async def get_user_ml_predictions(user_id: int, session=Depends(get_session)):
    try:
        user = UserService.get_user_by_id(user_id, session)
        if not user:
            logger.warning(f"User {user_id} not found"),
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Пользователь с ID {user_id} не найден"
            )
        predictions = user.ml_history
        logger.info(f"User with ID = {user_id} add transactions retrieved successfully")
        return predictions
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting add transactions for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )