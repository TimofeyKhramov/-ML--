from fastapi import APIRouter, HTTPException, status, Depends
from  database.database import get_session
from src.user import User
from services.crud import user as UserService
from typing import List, Dict
from services.crud import mltask as MLtaskService
import logging
from sqlmodel import Session, update
from src.mltask import MLTaskType, TaskStatus, MLTaskCreate, MLTaskHistory
from services.rm.rm import rabbit_client

# Configure logging
logger = logging.getLogger(__name__)

mltask_route = APIRouter()

def get_mltask_service(session: Session = Depends(get_session)) -> MLtaskService:
    return MLtaskService(session)

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
    

@mltask_route.post(
    "/send_task", 
    response_model=Dict[str, str],
    summary="ML endpoint",
    description="Send ml request"
)
async def send_task(message: str, question: str, mltask_id: int, user_id: int, session=Depends(get_session)) -> str:
    """
    Root endpoint returning welcome message.

    Returns:
        Dict[str, str]: Welcome message
    """
    created_mltask = None
    try:
        print(1)
        mltask = MLtaskService.get_mltask_by_id(mltask_id, session)
        created_mltask = MLTaskCreate(id=mltask.id, name=mltask.name, cost=mltask.cost, description=mltask.description, question=question, user_id=user_id, status=TaskStatus.NEW)
        history = MLtaskService.ml_prediction(user_id, session)
        logger.info(f"Massage has created: {created_mltask}")

        logger.info(f"Sending task to RabbitMQ: {message}")
        rabbit_client.send_task(created_mltask, history_id=history.id)
        return {"message": "Task sent successfully!"}
    except Exception as e:
        logger.error(f"Unexpected error in sending task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    

@mltask_route.post("/send_task_result", response_model=Dict[str, str])
def send_task_result(
    task_id: int,
    result: str,
    session = Depends(get_session)
) -> Dict[str, str]:
    """
    Endpoint for sending ML task using Result.

    Args:
        message (str): The message to be sent.
        user_id (int): ID of the user creating the task.

    Returns:
        Dict[str, str]: Response message with original and processed text.
    """
    try:
        updated = session.exec(
            update(MLTaskHistory)
            .where(MLTaskHistory.id == task_id)
            .values(result=result)
        )
        session.commit()
        
        if updated.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
     
        logger.info(f"!!!!!!!!Task result has been set: {result}")
        return {"message": "Task result sent successfully!"}
    except Exception as e:
        logger.error(f"Unexpected error in sending task result: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
