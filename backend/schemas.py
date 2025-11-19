from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TodoCreate(BaseModel):
    name: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class TodoUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_completed: Optional[bool] = None


class TodoResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    creation_date: datetime
    due_date: Optional[datetime]
    created_by: int
    is_completed: bool
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


class TodoListResponse(BaseModel):
    todos: List[TodoResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

