from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from pydantic import field_validator
import re


if TYPE_CHECKING:
    from src.transaction import AddTransaction
    from src.transaction import DebitTransaction

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    login: str = Field(
        ...,  # Required field
        unique=True,
        index=True,
        min_length=5,
        max_length=50
    )
    
    password: str = Field(..., min_length=6, max_length=128)
    balance: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    add_transactions: List["AddTransaction"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "lazy": "selectin"
        })
    
    debit_transactions: List["DebitTransaction"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "lazy": "selectin"
        }
        )
   
    def __str__(self) -> str:
        return f"Id: {self.id}. Login: {self.login}. Balance: {self.balance} {self.password}"
    
    

