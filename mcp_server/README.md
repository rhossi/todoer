# MCP Server - Model Context Protocol Server

The MCP server provides a Model Context Protocol interface for todo management operations.

## Overview

The MCP server exposes todo management functionality as MCP tools, allowing AI agents and other MCP clients to interact with the todo API through a standardized protocol.

## Architecture

- **Protocol**: Model Context Protocol (MCP)
- **Transport**: stdio (standard input/output)
- **Authentication**: JWT tokens via environment variables
- **Backend Communication**: HTTP requests to FastAPI backend

## Project Structure

```
mcp_server/
├── __init__.py    # Package initialization
└── server.py      # MCP server implementation
```

## How It Works

The MCP server is **automatically started** by the agent when needed. It runs as a subprocess and communicates via stdio.

### Automatic Startup (Normal Operation)

When the backend chat endpoint receives a request, it:
1. Creates an MCP client connection
2. Starts the MCP server as a subprocess
3. Passes authentication credentials via environment variables
4. Maintains the connection for the request duration

**No manual action required** - just use the chat feature in the frontend.

### Manual Startup (For Testing/Debugging)

If you want to test the MCP server standalone:

1. First, get a JWT token by logging in:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -F "username=yourusername" \
  -F "password=yourpassword"
```

2. Set environment variables:
```bash
export MCP_AUTH_TOKEN="<token-from-login-response>"
export MCP_API_BASE_URL="http://localhost:8000"
```

3. Run the server:
```bash
uv run python mcp_server/server.py
```

**Note**: The MCP server uses stdio transport, so when run standalone it will wait for MCP protocol messages on stdin. It's primarily designed to be used as a subprocess by MCP clients.

## Available Tools

The MCP server provides the following tools:

### `create_todo`
Create a new todo item.

**Input:**
- `name` (string, required): The name/title of the todo
- `description` (string, optional): Optional description
- `due_date` (string, optional): Due date in ISO format (YYYY-MM-DDTHH:MM:SS)

**Returns:** Created todo information

### `list_todos`
List todos with optional filtering and sorting.

**Input:**
- `search` (string, optional): Search query
- `sort_by` (string, optional): `name`, `creation_date`, or `due_date` (default: `creation_date`)
- `sort_order` (string, optional): `asc` or `desc` (default: `desc`)

**Returns:** List of todos

### `get_todo`
Get a specific todo by ID.

**Input:**
- `todo_id` (integer, required): The ID of the todo

**Returns:** Todo details

### `update_todo`
Update an existing todo.

**Input:**
- `todo_id` (integer, required): The ID of the todo
- `name` (string, optional): Updated name
- `description` (string, optional): Updated description
- `due_date` (string, optional): Updated due date in ISO format
- `is_completed` (boolean, optional): Completion status

**Returns:** Updated todo information

### `delete_todo`
Delete a todo.

**Input:**
- `todo_id` (integer, required): The ID of the todo

**Returns:** Success confirmation

### `toggle_todo_complete`
Toggle the completion status of a todo.

**Input:**
- `todo_id` (integer, required): The ID of the todo

**Returns:** Updated todo with new completion status

## Environment Variables

The MCP server reads these environment variables (set automatically by the client):

- `MCP_AUTH_TOKEN`: JWT authentication token (required)
- `MCP_API_BASE_URL`: Base URL for the FastAPI backend (default: `http://localhost:8000`)

## Security

- Each MCP server instance uses the authenticated user's JWT token
- Users can only access/modify their own todos
- Tokens are passed securely via environment variables
- All API calls are authenticated

## Architecture Diagram

```
┌─────────────┐
│   Agent     │
│ (LangGraph) │
└──────┬──────┘
       │
       │ Creates subprocess
       │ Sets env vars
       ▼
┌─────────────┐      ┌─────────────┐
│ MCP Client  │─────▶│ MCP Server │
│  (stdio)    │      │ (subprocess)│
└─────────────┘      └──────┬──────┘
                            │ HTTP
                            │ JWT Auth
                            ▼
                     ┌─────────────┐
                     │ FastAPI     │
                     │ Backend     │
                     └─────────────┘
```

## Troubleshooting

### Server Won't Start

1. Ensure the backend is running (`uv run python run_backend.py`)
2. Check that Python can execute `mcp_server/server.py`
3. Verify environment variables are set correctly
4. Check backend logs for MCP server subprocess errors

### Authentication Errors

- Ensure `MCP_AUTH_TOKEN` is set and valid
- Token must be from a logged-in user
- Token expiration: 30 minutes (configurable)

### Connection Issues

- Verify `MCP_API_BASE_URL` points to the correct backend URL
- Check network connectivity
- Ensure backend CORS allows the request origin

## Dependencies

Key dependencies:
- `mcp` - Model Context Protocol library
- `httpx` - HTTP client for API requests
- `pydantic` - Data validation

See `pyproject.toml` for the complete list.

