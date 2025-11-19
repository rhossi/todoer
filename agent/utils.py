"""Utility functions for the agent"""
from typing import Optional
from datetime import timedelta
from dateutil import parser


def normalize_date(date_str: Optional[str]) -> Optional[str]:
    """Normalize a date string to ISO format.
    
    Args:
        date_str: Date string in various formats
        
    Returns:
        ISO formatted date string, or None if input is None/empty
        
    Raises:
        ValueError: If date string cannot be parsed
    """
    if not date_str or not date_str.strip():
        return None
    
    try:
        parsed_date = parser.parse(date_str)
        return parsed_date.isoformat()
    except Exception:
        raise ValueError(
            f"Invalid date format: {date_str}. "
            "Use ISO format like YYYY-MM-DDTHH:MM:SS or YYYY-MM-DD"
        )


def format_system_prompt(now) -> str:
    """Generate system prompt with current date information."""
    current_date = now.strftime("%A, %B %d, %Y")
    current_time = now.strftime("%I:%M %p")
    tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    next_week = (now + timedelta(days=7)).strftime("%Y-%m-%d")
    
    return f"""You are a helpful assistant that helps users manage their todo list. 
You can create, read, update, and delete todos. Always be helpful and concise.

Current date and time: {current_date} at {current_time}
Today's date: {now.strftime("%Y-%m-%d")}
Tomorrow's date: {tomorrow}

IMPORTANT: When users mention dates or times, you MUST convert them to ISO 8601 format (YYYY-MM-DDTHH:MM:SS) before passing to tools.
- "tomorrow" means {tomorrow}T10:00:00 (or use a reasonable time)
- "next week" means {next_week}T10:00:00
- Always use the current year ({now.year}), not old years like 2023
- Format dates as YYYY-MM-DDTHH:MM:SS (e.g., "2025-11-17T14:30:00")
- If no time is specified, use 10:00:00 as default"""

