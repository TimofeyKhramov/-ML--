from sqlmodel import SQLModel, Field, Relationship, Session, select
from pydantic import field_validator
from typing import Optional, List, TYPE_CHECKING

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
            raise ValueError(f"ML task type '{ml_task_type}' not found in database")
        
        return result.cost
    
    @classmethod
    def is_valid(cls, session: Session, ml_task_type: str) -> bool:
        """Проверить, существует ли тип задачи в БД"""
        statement = select(cls).where(cls.name == ml_task_type)
        return session.exec(statement).first() is not None
    
    @classmethod
    def get_all_types(cls, session: Session) -> List[str]:
        """Получить все типы задач из БД"""
        statement = select(cls.name)
        return session.exec(statement).all()
    
    def __str__(self) -> str:
        return f"Id: {self.id}. Name: {self.name}. Price: {self.cost}"