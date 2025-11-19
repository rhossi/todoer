from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship
from datetime import datetime
from typing import Optional
from pathlib import Path

# Resolve database path relative to project root (same level as backend/)
project_root = Path(__file__).parent.parent
db_path = project_root / "todos.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    todos: Mapped[list["Todo"]] = relationship("Todo", back_populates="owner")


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[Optional[str]] = mapped_column(default=None)
    creation_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    due_date: Mapped[Optional[datetime]] = mapped_column(default=None)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_completed: Mapped[bool] = mapped_column(default=False, index=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    
    owner: Mapped["User"] = relationship("User", back_populates="todos")


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

