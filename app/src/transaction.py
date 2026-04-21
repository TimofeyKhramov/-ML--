from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator
from typing import Optional, List, TYPE_CHECKING
from src.mltask import MLTaskType

if TYPE_CHECKING:
    from src.user import User

class Transaction(SQLModel):
    """
    Base Event model with common fields.
    
    Attributes:
        title (str): Event title
        image (str): URL or path to event image
        description (str): Event description
        location (Optional[str]): Event location
        tags (Optional[List[str]]): Event tags
    """
    id: int =  Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
 

class AddTransaction(Transaction, table=True):
    type_of: str = Field(default='Adding')
    amount: int = Field(default=None)
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: int) -> int:
        if v < 1:
            raise ValueError('Amount cannot be less than 1')
        return v
    creator_id: Optional[int] = Field(default=None, foreign_key="user.id")
    creator: Optional["User"] = Relationship(
        back_populates="add_transactions",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    
    
    def __str__(self) -> str:
        result = (f"Id: {self.id}. Type: {self.type_of}. Creator: {self.creator.login}. Amount: {self.amount}. Date: {self.created_at}")
        return result
    
#     @property
#     def short_description(self) -> str:
#         """Returns truncated description for preview"""
#         max_length = 100
#         return (f"{self.description[:max_length]}..."
#                 if len(self.description) > max_length
#                 else self.description)


# class EventCreate(EventBase):
#     """Schema for creating new events"""
#     pass

# class EventUpdate(EventBase):
#     """Schema for updating existing events"""
#     title: Optional[str] = None
#     image: Optional[str] = None
#     description: Optional[str] = None



class DebitTransaction(Transaction, table=True):
    # __tablename__ = "debit_transactions"
    
    type_of: str = Field(default='Debiting')
    ml_task_type: str = Field()  #  Без default, нужно указывать при создании
    description: Optional[str] = Field(default=None, max_length=255)
    amount: int = Field()
    
    creator_id: Optional[int] = Field(default=None, foreign_key="user.id")
    creator: Optional["User"] = Relationship(
        back_populates="debit_transactions",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __str__(self) -> str:
        result = (f"Id: {self.id}. Type: {self.type_of}. Creator: {self.creator.login}. Amount: {self.amount}. Date: {self.created_at}")
        return result
    

class Config:
    """Model configuration"""
    validate_assignment = True
    arbitrary_types_allowed = True