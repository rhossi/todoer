"""MCP client adapter for connecting to the MCP server"""
import json
import os
import sys
from pathlib import Path
from typing import List, Any, Optional
from langchain_core.tools import tool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClientManager:
    """Manages MCP server connection and provides tool access"""
    
    def __init__(self, auth_token: str, api_base_url: str = "http://localhost:8000"):
        self.auth_token = auth_token
        self.api_base_url = api_base_url
        self._session: Optional[ClientSession] = None
        self._read = None
        self._write = None
        self._client_context = None
    
    async def connect(self):
        """Connect to the MCP server
        
        Each MCPClientManager instance creates its own isolated subprocess.
        The subprocess receives its own copy of environment variables, ensuring
        that concurrent users have separate MCP server instances with their own tokens.
        """
        if self._session:
            return  # Already connected
        
        # Create isolated environment for this subprocess
        # Each subprocess gets its own env dict, ensuring user isolation
        env = os.environ.copy()
        env["MCP_AUTH_TOKEN"] = self.auth_token  # User-specific token
        env["MCP_API_BASE_URL"] = self.api_base_url
        
        # Get the path to the MCP server script
        project_root = Path(__file__).parent.parent
        server_script = project_root / "mcp_server" / "server.py"
        
        # Create server parameters
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[str(server_script)],
            env=env
        )
        
        # Create client connection - store context manager to keep it alive
        self._client_context = stdio_client(server_params)
        self._read, self._write = await self._client_context.__aenter__()
        
        # Create and initialize session - store to keep it alive
        self._session = ClientSession(self._read, self._write)
        await self._session.__aenter__()
        await self._session.initialize()
    
    async def call_tool(self, tool_name: str, arguments: dict) -> str:
        """Call an MCP tool and return the result as a string"""
        if not self._session:
            await self.connect()
        
        result = await self._session.call_tool(tool_name, arguments)
        
        # Extract text content
        if result.content and len(result.content) > 0:
            text_content = result.content[0].text
            # Try to parse and reformat JSON for cleaner output
            try:
                if text_content.strip().startswith(("{", "[")):
                    parsed = json.loads(text_content)
                    return json.dumps(parsed, default=str, indent=2)
                return text_content
            except:
                return text_content
        return json.dumps({"error": "No content returned"})
    
    async def disconnect(self):
        """Disconnect from the MCP server"""
        if self._session:
            await self._session.__aexit__(None, None, None)
            self._session = None
        if self._client_context:
            await self._client_context.__aexit__(None, None, None)
            self._client_context = None


async def create_mcp_tools(auth_token: str, api_base_url: str = "http://localhost:8000") -> tuple[List[Any], MCPClientManager]:
    """Create LangChain tools from MCP server tools.
    
    Returns:
        Tuple of (list of LangChain tools, MCPClientManager instance)
    """
    manager = MCPClientManager(auth_token, api_base_url)
    await manager.connect()
    
    # Note: We don't need to query the server for tools since we define them ourselves.
    # The MCP server has the tools registered, and we'll call them directly.
    
    # Import date normalization utility
    from .utils import normalize_date
    
    # Create create_todo tool
    @tool
    async def create_todo(name: str, description: str = None, due_date: str = None) -> str:
        """Create a new todo item.
        
        Args:
            name: The name/title of the todo (required)
            description: Description of the todo (optional)
            due_date: Due date in ISO 8601 format or natural language (optional)
        """
        arguments = {"name": name}
        if description:
            arguments["description"] = description
        if due_date:
            try:
                arguments["due_date"] = normalize_date(due_date)
            except ValueError as e:
                return json.dumps({"error": str(e)})
        return await manager.call_tool("create_todo", arguments)
    
    # Create list_todos tool
    @tool
    async def list_todos(search: str = None, sort_by: str = "creation_date", sort_order: str = "desc") -> str:
        """List all todos.
        
        Args:
            search: Search query to filter todos (optional)
            sort_by: Sort by name, creation_date, or due_date (default: creation_date)
            sort_order: Sort order asc or desc (default: desc)
        """
        arguments = {}
        if search:
            arguments["search"] = search
        if sort_by:
            arguments["sort_by"] = sort_by
        if sort_order:
            arguments["sort_order"] = sort_order
        return await manager.call_tool("list_todos", arguments)
    
    # Create get_todo tool
    @tool
    async def get_todo(todo_id: int) -> str:
        """Get a specific todo by ID.
        
        Args:
            todo_id: The ID of the todo to retrieve
        """
        return await manager.call_tool("get_todo", {"todo_id": todo_id})
    
    # Create update_todo tool
    @tool
    async def update_todo(todo_id: int, name: str = None, description: str = None, due_date: str = None, is_completed: bool = None) -> str:
        """Update a todo. Use is_completed=True to mark as completed, is_completed=False to mark as uncompleted.
        
        Args:
            todo_id: The ID of the todo to update (required)
            name: Updated name (optional)
            description: Updated description (optional)
            due_date: Updated due date in ISO format or natural language (optional)
            is_completed: Set completion status - True to mark as completed, False to mark as uncompleted (optional)
        """
        arguments = {"todo_id": todo_id}
        if name is not None:
            arguments["name"] = name
        if description is not None:
            arguments["description"] = description
        if due_date is not None:
            try:
                arguments["due_date"] = normalize_date(due_date)
            except ValueError as e:
                return json.dumps({"error": str(e)})
        if is_completed is not None:
            arguments["is_completed"] = is_completed
        return await manager.call_tool("update_todo", arguments)
    
    # Create toggle_todo_complete tool
    @tool
    async def toggle_todo_complete(todo_id: int) -> str:
        """Toggle the completion status of a todo (if completed, mark as uncompleted; if uncompleted, mark as completed).
        
        Args:
            todo_id: The ID of the todo to toggle
        """
        return await manager.call_tool("toggle_todo_complete", {"todo_id": todo_id})
    
    # Create delete_todo tool
    @tool
    async def delete_todo(todo_id: int) -> str:
        """Delete a todo by ID.
        
        Args:
            todo_id: The ID of the todo to delete
        """
        return await manager.call_tool("delete_todo", {"todo_id": todo_id})
    
    langchain_tools = [create_todo, list_todos, get_todo, update_todo, toggle_todo_complete, delete_todo]
    
    return langchain_tools, manager
