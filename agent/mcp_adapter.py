"""MCP adapter for making API calls to the backend"""
from typing import Dict, Any
from .api_client import APIClient


async def create_todo_mcp_call(auth_token: str, api_base_url: str = "http://localhost:8000"):
    """Factory function to create a todo creation MCP call"""
    client = APIClient(auth_token, api_base_url)
    
    async def _call(arguments: dict) -> Dict[str, Any]:
        data = {k: v for k, v in arguments.items() if v is not None}
        return await client.post("/api/todos", json_data=data)
    
    return _call


async def list_todos_mcp_call(auth_token: str, api_base_url: str = "http://localhost:8000"):
    """Factory function to create a todo listing MCP call"""
    client = APIClient(auth_token, api_base_url)
    
    async def _call(arguments: dict) -> Dict[str, Any]:
        params = {k: v for k, v in arguments.items() if v is not None}
        return await client.get("/api/todos", params=params)
    
    return _call


async def get_todo_mcp_call(auth_token: str, api_base_url: str = "http://localhost:8000"):
    """Factory function to create a todo retrieval MCP call"""
    client = APIClient(auth_token, api_base_url)
    
    async def _call(arguments: dict) -> Dict[str, Any]:
        todo_id = arguments["todo_id"]
        return await client.get(f"/api/todos/{todo_id}")
    
    return _call


async def update_todo_mcp_call(auth_token: str, api_base_url: str = "http://localhost:8000"):
    """Factory function to create a todo update MCP call"""
    client = APIClient(auth_token, api_base_url)
    
    async def _call(arguments: dict) -> Dict[str, Any]:
        todo_id = arguments.pop("todo_id")
        data = {k: v for k, v in arguments.items() if v is not None}
        return await client.put(f"/api/todos/{todo_id}", json_data=data)
    
    return _call


async def delete_todo_mcp_call(auth_token: str, api_base_url: str = "http://localhost:8000"):
    """Factory function to create a todo deletion MCP call"""
    client = APIClient(auth_token, api_base_url)
    
    async def _call(arguments: dict) -> Dict[str, Any]:
        todo_id = arguments["todo_id"]
        await client.delete(f"/api/todos/{todo_id}")
        return {"message": f"Successfully deleted todo {todo_id}"}
    
    return _call

