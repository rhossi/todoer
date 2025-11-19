# Todoer - Full-Stack Todo Application

A modern full-stack todo management application with AI-powered natural language interface, built with FastAPI, Next.js, and Model Context Protocol (MCP).

## Features

- 🎨 **Modern Neon-Dark UI** - Beautiful, responsive design with custom neon-dark theme
- 🔐 **JWT Authentication** - Secure user authentication and authorization
- ✅ **Todo Management** - Full CRUD operations with search, filter, and sort
- 🤖 **AI Chat Interface** - Natural language todo management via conversational AI
- 🔌 **MCP Integration** - Model Context Protocol tools for AI agent interaction
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile devices

## Project Structure

```
.
├── backend/          # FastAPI backend API
│   └── README.md     # Backend documentation
├── frontend/         # Next.js frontend application
│   └── README.md     # Frontend documentation
├── mcp_server/       # MCP server for AI tools
│   └── README.md     # MCP server documentation
├── agent/            # LangGraph agent (used by backend)
├── run_backend.py    # Backend startup script
├── start_backend.sh  # Backend startup shell script
├── start.sh          # Start all services
├── pyproject.toml    # Python dependencies
└── README.md         # This file
```

## Quick Start

### Prerequisites

- Python 3.12
- Node.js 18+
- uv (Python package manager)
- OpenAI API key (for chat functionality)

### Installation

1. **Clone the repository** (if applicable):
```bash
git clone <repository-url>
cd todoer
```

2. **Install Python dependencies**:
```bash
uv sync
```

3. **Install frontend dependencies**:
```bash
cd frontend
npm install
cd ..
```

4. **Set up environment variables**:
```bash
# Copy the example file
cp .env.example .env

# Edit .env and fill in your actual values
# Especially important: OPENAI_API_KEY
```

**Note:** The `.env` file is not committed to git (it's in `.gitignore`). Each developer needs to create their own `.env` file.

See `.env.example` for all available configuration options.

### Starting the Application

**Important:** The database (`todos.db`) will be automatically created on first startup. You don't need to create it manually.

#### Option 1: Start Everything (Recommended)

Use the convenience script to start all services:
```bash
./start.sh
```

This will start:
- Backend API server (port 8000) - creates database automatically if it doesn't exist
- Frontend development server (port 3000)

#### Option 2: Start Services Individually

**Backend:**
```bash
# Using uv
uv run python run_backend.py

# Or using the shell script
./start_backend.sh
```

**Frontend:**
```bash
cd frontend
npm run dev
```

### Accessing the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Architecture

```
┌─────────────┐
│  Next.js    │  Frontend (React/TypeScript)
│  Frontend   │  Port 3000
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────┐      ┌──────────────┐
│   FastAPI   │◄─────│  ReAct Agent │
│   Backend   │      │  (LangGraph) │
│  Port 8000  │      └──────┬───────┘
└──────┬──────┘             │
       │                    │ MCP Tools
       │                    │
       ▼                    ▼
┌─────────────┐      ┌──────────────┐
│  SQLite DB  │      │  MCP Server   │
│  todos.db   │      │  (subprocess)│
└─────────────┘      └──────────────┘
```

## Component Documentation

- **[Backend README](backend/README.md)** - FastAPI backend setup and API documentation
- **[Frontend README](frontend/README.md)** - Next.js frontend setup and development guide
- **[MCP Server README](mcp_server/README.md)** - MCP server architecture and tools

## Usage

### Authentication

1. Open http://localhost:3000
2. Click "Login or Register"
3. Create an account or login with existing credentials
4. JWT tokens are automatically managed

### Todo Management

**Via UI:**
- Click "Create Todo" to add new todos
- Double-click any todo to edit
- Use search box to find todos
- Filter by completion status
- Sort by name, creation date, or due date
- Click delete button to remove todos

**Via Chat:**
1. Click the floating chat button (💬)
2. Type natural language commands:
   - "Create a todo called 'Buy groceries'"
   - "List all my todos"
   - "Show me todos due today"
   - "Delete todo with id 5"
   - "Update todo 3 to be completed"

## API Endpoints

See [Backend README](backend/README.md) for complete API documentation.

### Key Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/todos` - List todos
- `POST /api/todos` - Create todo
- `PUT /api/todos/{id}` - Update todo
- `DELETE /api/todos/{id}` - Delete todo
- `POST /api/chat` - Chat with AI agent

## Technologies

- **Backend**: FastAPI, SQLAlchemy, Python-JOSE, Passlib, LangChain, LangGraph
- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS
- **MCP**: Model Context Protocol
- **Database**: SQLite
- **AI**: OpenAI GPT (via LangChain)

## Development

### Backend Development

```bash
# Run with auto-reload
uv run python run_backend.py

# Run tests (when implemented)
pytest
```

### Frontend Development

```bash
cd frontend
npm run dev

# Lint
npm run lint

# Build for production
npm run build
```

### Database

The SQLite database (`todos.db`) is **automatically created** when you first start the backend server. The database file is:
- **Not committed to git** (excluded via `.gitignore`)
- **Created automatically** on first startup via the `init_db()` function
- **Located in the project root** directory

Each developer will have their own local database file. To reset your local database:
```bash
rm todos.db
uv run python run_backend.py
```

## Security

- Passwords hashed with bcrypt
- JWT tokens with configurable expiration
- User isolation (users can only access their own todos)
- CORS configured for frontend origin
- Environment variables for sensitive configuration

## License

MIT

## Support

For issues or questions:
1. Check the component-specific README files
2. Review the API documentation at http://localhost:8000/docs
3. Check backend logs for errors
