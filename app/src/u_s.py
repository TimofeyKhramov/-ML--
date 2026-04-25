from pydantic import BaseModel, Field
class UserCreate(BaseModel):
    login: str = Field(..., min_length=5, max_length=50)
    password: str = Field(..., min_length=5, max_length=128)