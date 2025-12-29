"""
Standard API Response Utilities
Provides consistent response format across all endpoints
"""
from typing import Any, Optional, List, Dict
from math import ceil


def standard_response(
    status: str,
    message: str,
    data: Any = None
) -> Dict[str, Any]:
    """
    Create standard API response
    
    Args:
        status: "success" or "error"
        message: Description of the operation result
        data: Response data (dict, list, or None)
    
    Returns:
        Standardized response dictionary
    """
    return {
        "status": status,
        "message": message,
        "data": data
    }


def success_response(message: str, data: Any = None) -> Dict[str, Any]:
    """
    Create success response
    
    Args:
        message: Success message
        data: Response data
    
    Returns:
        Success response dictionary
    """
    return standard_response("success", message, data)


def error_response(message: str, data: Any = None) -> Dict[str, Any]:
    """
    Create error response
    
    Args:
        message: Error message
        data: Additional error data
    
    Returns:
        Error response dictionary
    """
    return standard_response("error", message, data)


def paginated_response(
    message: str,
    items: List[Any],
    total: int,
    page: int,
    size: int
) -> Dict[str, Any]:
    """
    Create paginated response
    
    Args:
        message: Success message
        items: List of items for current page
        total: Total number of items
        page: Current page number
        size: Items per page
    
    Returns:
        Paginated response dictionary
    """
    pages = ceil(total / size) if size > 0 else 0
    
    return {
        "status": "success",
        "message": message,
        "data": items,
        "pagination": {
            "total": total,
            "page": page,
            "size": size,
            "pages": pages
        }
    }
