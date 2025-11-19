"""API client for making authenticated HTTP requests to the backend"""
import httpx
from typing import Optional, Dict, Any


class APIClient:
    """Simple API client for making authenticated requests"""
    
    def __init__(self, auth_token: str, base_url: str = "http://localhost:8000"):
        self.auth_token = auth_token
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
    
    async def _request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make an HTTP request"""
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GET request"""
        return await self._request("GET", endpoint, params=params)
    
    async def post(self, endpoint: str, json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """POST request"""
        return await self._request("POST", endpoint, json_data=json_data)
    
    async def put(self, endpoint: str, json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """PUT request"""
        return await self._request("PUT", endpoint, json_data=json_data)
    
    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """DELETE request"""
        return await self._request("DELETE", endpoint)

