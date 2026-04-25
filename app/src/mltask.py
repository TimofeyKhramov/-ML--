from sqlmodel import SQLModel, Field, Relationship, Session, select
from enum import Enum
from pydantic import field_validator, BaseModel
from typing import Optional, List, TYPE_CHECKING
from src.user import User
from datetime import datetime

if TYPE_CHECKING:
    from src.user import User

class MLTaskType(SQLModel, table=True):
    """Таблица типов ML задач в БД"""
    __tablename__ = "ml_task_types"
    
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(unique=True)  # "classification", "cheque" и т.д.
    cost: int = Field()  # Стоимость за операцию
    description: Optional[str] = Field()  # Описание задачи

    @classmethod
    def get_cost(cls, session: Session, ml_task_type: str) -> int:
        """
        Получить стоимость ML задачи из БД.
        
        Args:
            session: Сессия БД
            task_type: Название типа задачи (например, "classification")
            
        Returns:
            int: Стоимость задачи
            
        Raises:
            ValueError: Если тип задачи не найден в БД
        """
        statement = select(cls).where(cls.name == ml_task_type)
        result = session.exec(statement).first()
        
        if not result:
            raise ValueError(f"ML-задача {ml_task_type} не найдена")
        
        return result.cost
    
    @classmethod
    def is_valid(cls, session: Session, ml_task_type: str) -> bool:
        """Проверить, существует ли тип задачи в БД"""
        statement = select(cls).where(cls.name == ml_task_type)
        result =  session.exec(statement).first() 

        if result is None:
            raise ValueError(f"ML-задача {ml_task_type} не найдена")
    
        return True
    
    @classmethod
    def get_all_types(cls, session: Session) -> List[str]:
        """Получить все типы задач из БД"""
        statement = select(cls.name)
        return session.exec(statement).all()
    
    
    
    def __str__(self) -> str:
        return f"Id: {self.id}. Name: {self.name}. Price: {self.cost}"
    
    class Config:
        """Model configuration"""
        validate_assignment = True
        arbitrary_types_allowed = True

    


class MLTaskHistory(SQLModel, table=True):
    __tablename__ = "ml_tasks_history"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    result: Optional[str] = Field(default=None)      # Результат предсказания                          # Стоимость операции
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Связь с пользователем
    user: Optional[User] = Relationship(back_populates="ml_history")

class MLTaskCreate(BaseModel):
    id: int  
    name: str
    cost: int
    description: Optional[str] = None
    question: Optional[str] = None
    user_id: int
    features: Optional[dict] = None

    
    def to_queue_message(self, history_id: int) -> dict:
        return {
            "task_id": history_id,  
            "features": self.features,
            "model": self.name,
            "question": self.question,
        }


