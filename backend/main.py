from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc
from typing import Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from .database import get_db, init_db, Todo, User
from .auth import (
    get_current_user,
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_user_by_username,
    get_user_by_email,
    oauth2_scheme,
)
from .schemas import (
    UserCreate,
    UserResponse,
    Token,
    TodoCreate,
    TodoUpdate,
    TodoResponse,
    TodoListResponse,
)
from .config import settings

app = FastAPI(title="Todo API", version="1.0.0")


class ChatMessage(BaseModel):
    message: str
    conversation_history: list[dict] = []


class ChatResponse(BaseModel):
    response: str


def get_todo_by_id_and_user(todo_id: int, user_id: int, db: Session) -> Optional[Todo]:
    """Helper function to get a todo by ID and user, or None if not found"""
    return db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.created_by == user_id
    ).first()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    init_db()


@app.post("/api/auth/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username exists
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    # Check if email exists
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/api/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/api/todos", response_model=TodoListResponse)
async def list_todos(
    search: Optional[str] = Query(None, description="Search in name and description"),
    sort_by: Optional[str] = Query("creation_date", description="Sort by: name, creation_date, due_date"),
    sort_order: Optional[str] = Query("desc", description="Sort order: asc or desc"),
    completed: Optional[str] = Query("", description="Filter by completion: all, true, false (empty string = all)"),
    page: Optional[int] = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: Optional[int] = Query(10, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Todo).filter(Todo.created_by == current_user.id)
    
    # Completion filter - empty string or "all" shows all todos
    if completed == "true":
        query = query.filter(Todo.is_completed == True)
    elif completed == "false":
        query = query.filter(Todo.is_completed == False)
    # If empty string, "all", or None, don't filter by completion (show all)
    
    # Search filter
    if search:
        query = query.filter(
            or_(
                Todo.name.contains(search),
                Todo.description.contains(search)
            )
        )
    
    # Get total count before pagination
    total = query.count()
    
    # Sorting
    sort_column = {
        "name": Todo.name,
        "creation_date": Todo.creation_date,
        "due_date": Todo.due_date
    }.get(sort_by, Todo.creation_date)
    
    if sort_order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))
    
    # Pagination
    offset = (page - 1) * page_size
    todos = query.offset(offset).limit(page_size).all()
    
    # Calculate total pages
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    
    return {
        "todos": todos,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


@app.post("/api/todos", response_model=TodoResponse)
async def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_todo = Todo(
        name=todo.name,
        description=todo.description,
        due_date=todo.due_date,
        created_by=current_user.id
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.get("/api/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    todo = get_todo_by_id_and_user(todo_id, current_user.id, db)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return todo


@app.put("/api/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    todo = get_todo_by_id_and_user(todo_id, current_user.id, db)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    # Update fields if provided
    update_data = todo_update.model_dump(exclude_unset=True)
    
    # Handle is_completed change - set completed_at accordingly
    if "is_completed" in update_data:
        if update_data["is_completed"]:
            todo.completed_at = datetime.utcnow()
        else:
            todo.completed_at = None
    
    for field, value in update_data.items():
        if field != "is_completed":  # Already handled above
            setattr(todo, field, value)
    
    db.commit()
    db.refresh(todo)
    return todo


@app.patch("/api/todos/{todo_id}/toggle-complete", response_model=TodoResponse)
async def toggle_todo_complete(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Toggle the completion status of a todo"""
    todo = get_todo_by_id_and_user(todo_id, current_user.id, db)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    todo.is_completed = not todo.is_completed
    # Set completed_at when marking as completed, clear when uncompleting
    if todo.is_completed:
        todo.completed_at = datetime.utcnow()
    else:
        todo.completed_at = None
    
    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/api/todos/{todo_id}")
async def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    todo = get_todo_by_id_and_user(todo_id, current_user.id, db)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_agent(
    chat_message: ChatMessage,
    token: str = Depends(oauth2_scheme),
    current_user: User = Depends(get_current_user)
):
    """Chat endpoint that uses the ReAct agent with MCP tools"""
    try:
        from agent.agent import create_react_agent, chat_with_agent
        
        # Create or get cached agent for this user
        # Note: We need to recreate agents when tokens expire, so caching might not be ideal
        # For now, create a new agent each time (can be optimized later)
        agent = await create_react_agent(
            auth_token=token,
            api_base_url=settings.API_BASE_URL
        )
        
        # Convert conversation history format
        from langchain_core.messages import HumanMessage, AIMessage
        history = []
        for msg in chat_message.conversation_history:
            if msg.get("role") == "user":
                history.append(HumanMessage(content=msg.get("content", "")))
            elif msg.get("role") == "assistant":
                history.append(AIMessage(content=msg.get("content", "")))
        
        response = await chat_with_agent(agent, chat_message.message, history)
        return ChatResponse(response=response)
    except Exception as e:
        import traceback
        import sys
        error_detail = str(e)
        error_traceback = traceback.format_exc()
        # Log to stderr so it shows in terminal
        print(f"Chat error: {error_detail}", file=sys.stderr)
        print(f"Traceback: {error_traceback}", file=sys.stderr)
        sys.stderr.flush()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in chat: {error_detail}"
        )


@app.get("/")
async def root():
    return {"message": "Todo API is running"}

