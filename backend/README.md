# Backend - FastAPI Todo API

The backend is a FastAPI-based REST API that provides authentication and todo management functionality.

## Overview

The backend handles:
- User authentication (JWT-based)
- Todo CRUD operations
- Chat endpoint for AI agent integration
- Database management with SQLAlchemy

## Architecture

- **Framework**: FastAPI
- **Database**: SQLite (via SQLAlchemy ORM)
- **Authentication**: JWT tokens with Python-JOSE
- **Password Hashing**: bcrypt via Passlib

## Project Structure

```
backend/
├── __init__.py      # Package initialization
├── main.py          # FastAPI app, routes, and endpoints
├── auth.py          # JWT authentication logic
├── database.py      # SQLAlchemy models and database setup
├── schemas.py       # Pydantic models for request/response validation
└── config.py        # Configuration settings (loads from .env)
```

## Setup

### Prerequisites

- Python 3.12
- uv (Python package manager)

### Installation

1. Install dependencies from the project root:
```bash
cd /path/to/todoer
uv sync
```

2. Create a `.env` file in the project root with the following variables:
```env
SECRET_KEY=your-secret-key-change-in-production
OPENAI_API_KEY=your-openai-api-key
API_BASE_URL=http://localhost:8000
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
```

### Starting the Server

From the project root:

```bash
# Using uv
uv run python run_backend.py

# Or using the shell script
./start_backend.sh
```

The API will be available at `http://localhost:8000`

API documentation (Swagger UI) will be available at `http://localhost:8000/docs`

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
  - Body: `{ "username": "string", "email": "string", "password": "string" }`
  - Returns: User info and JWT token

- `POST /api/auth/login` - Login (OAuth2 form data)
  - Form data: `username`, `password`
  - Returns: JWT access token

- `GET /api/auth/me` - Get current user info (requires auth)
  - Headers: `Authorization: Bearer <token>`
  - Returns: User information

### Todos

All todo endpoints require authentication via JWT token in the `Authorization` header.

- `GET /api/todos` - List todos
  - Query params:
    - `search` (optional): Search query
    - `sort_by` (optional): `name`, `creation_date`, or `due_date`
    - `sort_order` (optional): `asc` or `desc`
    - `completed` (optional): `true`, `false`, or `all`
    - `page` (optional): Page number (default: 1)
    - `page_size` (optional): Items per page (default: 10)
  - Returns: Paginated list of todos

- `POST /api/todos` - Create a new todo
  - Body: `{ "name": "string", "description": "string (optional)", "due_date": "ISO string (optional)" }`
  - Returns: Created todo

- `GET /api/todos/{id}` - Get a specific todo
  - Returns: Todo details

- `PUT /api/todos/{id}` - Update a todo
  - Body: `{ "name": "string (optional)", "description": "string (optional)", "due_date": "ISO string (optional)" }`
  - Returns: Updated todo

- `DELETE /api/todos/{id}` - Delete a todo
  - Returns: Success message

- `POST /api/todos/{id}/toggle-complete` - Toggle completion status
  - Returns: Updated todo

### Chat

- `POST /api/chat` - Chat with AI agent (requires auth)
  - Body: `{ "message": "string", "conversation_history": [] }`
  - Returns: `{ "response": "string" }`

## Database

The SQLite database (`todos.db`) is automatically created in the project root on first run.

### Models

- **User**: Stores user credentials and profile information
- **Todo**: Stores todo items with name, description, due date, and completion status

### Resetting the Database

To reset the database:
```bash
rm todos.db
uv run python run_backend.py
```

## Security

- Passwords are hashed using bcrypt
- JWT tokens expire after 30 minutes (configurable)
- All endpoints except `/api/auth/register` and `/api/auth/login` require authentication
- Users can only access/modify their own todos
- CORS is configured to allow requests from the frontend

## Development

### Running in Development Mode

The `run_backend.py` script runs with auto-reload enabled, so changes to Python files will automatically restart the server.

### Testing

```bash
# Run tests (when implemented)
pytest
```

## Configuration

All configuration is managed through environment variables (see `.env` file). The `config.py` module loads these values and provides defaults for development.

## Dependencies

Key dependencies are defined in `pyproject.toml`:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM
- `python-jose[cryptography]` - JWT handling
- `passlib[bcrypt]` - Password hashing
- `pydantic` - Data validation

See `pyproject.toml` for the complete list.

