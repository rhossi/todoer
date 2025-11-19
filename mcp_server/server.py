import asyncio
import httpx
import os
from typing import Any, Sequence
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field
import json


class TodoCreateInput(BaseModel):
    name: str = Field(description="The name/title of the todo item")
    description: str | None = Field(None, description="Optional description of the todo")
    due_date: str | None = Field(None, description="Optional due date in ISO format (YYYY-MM-DDTHH:MM:SS)")


class TodoUpdateInput(BaseModel):
    todo_id: int = Field(description="The ID of the todo to update")
    name: str | None = Field(None, description="Updated name/title")
    description: str | None = Field(None, description="Updated description")
    due_date: str | None = Field(None, description="Updated due date in ISO format")
    is_completed: bool | None = Field(None, description="Set completion status (True/False)")


class TodoToggleCompleteInput(BaseModel):
    todo_id: int = Field(description="The ID of the todo to toggle completion status")


class TodoDeleteInput(BaseModel):
    todo_id: int = Field(description="The ID of the todo to delete")


class TodoListInput(BaseModel):
    search: str | None = Field(None, description="Search query to filter todos")
    sort_by: str | None = Field("creation_date", description="Sort by: name, creation_date, or due_date")
    sort_order: str | None = Field("desc", description="Sort order: asc or desc")


class TodoGetInput(BaseModel):
    todo_id: int = Field(description="The ID of the todo to retrieve")


# Store for authentication token
# Note: Each MCP server subprocess has its own TokenStore instance.
# The token is read from the subprocess's environment variables at initialization,
# which are set uniquely for each user's MCP client connection.
class TokenStore:
    def __init__(self):
        # Read from environment variables (set by MCP client for this subprocess)
        # Each subprocess gets its own isolated environment, so concurrent users
        # have separate token stores with their own authentication tokens.
        self.token: str | None = os.getenv("MCP_AUTH_TOKEN")
        self.api_base_url: str = os.getenv("MCP_API_BASE_URL", "http://localhost:8000")
    
    def set_token(self, token: str):
        self.token = token
    
    def get_headers(self) -> dict:
        if not self.token:
            raise ValueError("No authentication token available. Please authenticate first.")
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }


token_store = TokenStore()


async def create_todo_tool(arguments: dict) -> list[TextContent]:
    """Create a new todo item"""
    try:
        input_data = TodoCreateInput(**arguments)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{token_store.api_base_url}/api/todos",
                json=input_data.model_dump(exclude_none=True),
                headers=token_store.get_headers()
            )
            response.raise_for_status()
            result = response.json()
            return [TextContent(
                type="text",
                text=f"Successfully created todo: {json.dumps(result, indent=2)}"
            )]
    except httpx.HTTPStatusError as e:
        return [TextContent(
            type="text",
            text=f"Error creating todo: {e.response.status_code} - {e.response.text}"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error creating todo: {str(e)}"
        )]


async def list_todos_tool(arguments: dict) -> list[TextContent]:
    """List all todos for the authenticated user"""
    try:
        input_data = TodoListInput(**arguments)
        params = {}
        if input_data.search:
            params["search"] = input_data.search
        if input_data.sort_by:
            params["sort_by"] = input_data.sort_by
        if input_data.sort_order:
            params["sort_order"] = input_data.sort_order
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{token_store.api_base_url}/api/todos",
                params=params,
                headers=token_store.get_headers()
            )
            response.raise_for_status()
            result = response.json()
            return [TextContent(
                type="text",
                text=f"Todos: {json.dumps(result, indent=2, default=str)}"
            )]
    except httpx.HTTPStatusError as e:
        return [TextContent(
            type="text",
            text=f"Error listing todos: {e.response.status_code} - {e.response.text}"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error listing todos: {str(e)}"
        )]


async def get_todo_tool(arguments: dict) -> list[TextContent]:
    """Get a specific todo by ID"""
    try:
        input_data = TodoGetInput(**arguments)
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{token_store.api_base_url}/api/todos/{input_data.todo_id}",
                headers=token_store.get_headers()
            )
            response.raise_for_status()
            result = response.json()
            return [TextContent(
                type="text",
                text=f"Todo: {json.dumps(result, indent=2, default=str)}"
            )]
    except httpx.HTTPStatusError as e:
        return [TextContent(
            type="text",
            text=f"Error getting todo: {e.response.status_code} - {e.response.text}"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error getting todo: {str(e)}"
        )]


async def update_todo_tool(arguments: dict) -> list[TextContent]:
    """Update an existing todo item"""
    try:
        input_data = TodoUpdateInput(**arguments)
        todo_id = input_data.todo_id
        update_data = input_data.model_dump(exclude={"todo_id"}, exclude_none=True)
        
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{token_store.api_base_url}/api/todos/{todo_id}",
                json=update_data,
                headers=token_store.get_headers()
            )
            response.raise_for_status()
            result = response.json()
            return [TextContent(
                type="text",
                text=f"Successfully updated todo: {json.dumps(result, indent=2, default=str)}"
            )]
    except httpx.HTTPStatusError as e:
        return [TextContent(
            type="text",
            text=f"Error updating todo: {e.response.status_code} - {e.response.text}"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error updating todo: {str(e)}"
        )]


async def toggle_todo_complete_tool(arguments: dict) -> list[TextContent]:
    """Toggle the completion status of a todo"""
    try:
        input_data = TodoToggleCompleteInput(**arguments)
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{token_store.api_base_url}/api/todos/{input_data.todo_id}/toggle-complete",
                headers=token_store.get_headers()
            )
            response.raise_for_status()
            result = response.json()
            return [TextContent(
                type="text",
                text=f"Successfully toggled todo completion: {json.dumps(result, indent=2, default=str)}"
            )]
    except httpx.HTTPStatusError as e:
        return [TextContent(
            type="text",
            text=f"Error toggling todo completion: {e.response.status_code} - {e.response.text}"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error toggling todo completion: {str(e)}"
        )]


async def delete_todo_tool(arguments: dict) -> list[TextContent]:
    """Delete a todo item"""
    try:
        input_data = TodoDeleteInput(**arguments)
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{token_store.api_base_url}/api/todos/{input_data.todo_id}",
                headers=token_store.get_headers()
            )
            response.raise_for_status()
            return [TextContent(
                type="text",
                text=f"Successfully deleted todo {input_data.todo_id}"
            )]
    except httpx.HTTPStatusError as e:
        return [TextContent(
            type="text",
            text=f"Error deleting todo: {e.response.status_code} - {e.response.text}"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error deleting todo: {str(e)}"
        )]


# Create MCP server
server = Server("todo-mcp-server")

# Register tools using decorator pattern
@server.list_tools()
async def list_tools() -> list[Tool]:
    """Return list of available tools"""
    return [
        Tool(
            name="create_todo",
            description="Create a new todo item. Requires authentication token.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "The name/title of the todo item"},
                    "description": {"type": "string", "description": "Optional description"},
                    "due_date": {"type": "string", "description": "Optional due date in ISO format"}
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="list_todos",
            description="List all todos for the authenticated user. Supports search and sorting.",
            inputSchema={
                "type": "object",
                "properties": {
                    "search": {"type": "string", "description": "Search query"},
                    "sort_by": {"type": "string", "enum": ["name", "creation_date", "due_date"], "description": "Sort field"},
                    "sort_order": {"type": "string", "enum": ["asc", "desc"], "description": "Sort order"}
                }
            }
        ),
        Tool(
            name="get_todo",
            description="Get a specific todo by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "todo_id": {"type": "integer", "description": "The ID of the todo"}
                },
                "required": ["todo_id"]
            }
        ),
        Tool(
            name="update_todo",
            description="Update an existing todo item. Use is_completed=True to mark as completed, is_completed=False to mark as uncompleted.",
            inputSchema={
                "type": "object",
                "properties": {
                    "todo_id": {"type": "integer", "description": "The ID of the todo"},
                    "name": {"type": "string", "description": "Updated name"},
                    "description": {"type": "string", "description": "Updated description"},
                    "due_date": {"type": "string", "description": "Updated due date in ISO format"},
                    "is_completed": {"type": "boolean", "description": "Set completion status (True to mark as completed, False to mark as uncompleted)"}
                },
                "required": ["todo_id"]
            }
        ),
        Tool(
            name="toggle_todo_complete",
            description="Toggle the completion status of a todo (if completed, mark as uncompleted; if uncompleted, mark as completed)",
            inputSchema={
                "type": "object",
                "properties": {
                    "todo_id": {"type": "integer", "description": "The ID of the todo to toggle"}
                },
                "required": ["todo_id"]
            }
        ),
        Tool(
            name="delete_todo",
            description="Delete a todo item",
            inputSchema={
                "type": "object",
                "properties": {
                    "todo_id": {"type": "integer", "description": "The ID of the todo to delete"}
                },
                "required": ["todo_id"]
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    tool_map = {
        "create_todo": create_todo_tool,
        "list_todos": list_todos_tool,
        "get_todo": get_todo_tool,
        "update_todo": update_todo_tool,
        "toggle_todo_complete": toggle_todo_complete_tool,
        "delete_todo": delete_todo_tool,
    }
    
    if name not in tool_map:
        raise ValueError(f"Unknown tool: {name}")
    
    return await tool_map[name](arguments)


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

