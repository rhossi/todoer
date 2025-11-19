"""ReAct LangGraph agent for todo management"""
import os
import json
from datetime import datetime
from pathlib import Path

# Load environment variables before other imports that depend on them
from dotenv import load_dotenv
project_root = Path(__file__).parent.parent
env_file = project_root / ".env"
load_dotenv(dotenv_path=env_file)

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langchain.agents import create_agent

from backend.config import settings
from .mcp_client import create_mcp_tools
from .utils import format_system_prompt


async def create_react_agent(
    auth_token: str, 
    api_base_url: str = "http://localhost:8000", 
    model_name: str = "gpt-4o-mini"
):
    """Create a ReAct agent with MCP tools using LangChain's create_agent"""
    
    # Get tools from MCP server
    tools, mcp_manager = await create_mcp_tools(auth_token, api_base_url)
    
    # Store manager for cleanup (could be improved with proper lifecycle management)
    # For now, we'll keep the connection alive for the agent's lifetime
    
    # Initialize LLM
    openai_api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required. "
            "Set it in .env file or environment."
        )
    
    llm = ChatOpenAI(model=model_name, temperature=0, openai_api_key=openai_api_key)
    
    # Create agent using LangChain's create_agent (simpler than manual StateGraph)
    agent = create_agent(
        llm,
        tools,
        system_prompt=format_system_prompt(datetime.now())
    )
    
    return agent


async def chat_with_agent(agent, user_message: str, conversation_history: list = None) -> str:
    """Chat with the agent"""
    import traceback
    import sys
    
    try:
        if conversation_history is None:
            conversation_history = []
        
        # Build messages list
        messages = []
        
        # Add conversation history
        for msg in conversation_history:
            if isinstance(msg, HumanMessage) or isinstance(msg, AIMessage):
                messages.append(msg)
            elif isinstance(msg, dict):
                # Handle dict format
                role = msg.get("role")
                content = msg.get("content", "")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))
        
        # Add user message
        messages.append(HumanMessage(content=user_message))
        
        # Invoke agent
        result = await agent.ainvoke({"messages": messages})
        
        # Extract the last AI message
        ai_messages = [msg for msg in result["messages"] if isinstance(msg, AIMessage)]
        if ai_messages:
            return ai_messages[-1].content
        
        return "I'm sorry, I couldn't process your request."
    except Exception as e:
        error_detail = str(e)
        error_traceback = traceback.format_exc()
        print(f"Agent chat error: {error_detail}", file=sys.stderr)
        print(f"Traceback: {error_traceback}", file=sys.stderr)
        sys.stderr.flush()
        raise

