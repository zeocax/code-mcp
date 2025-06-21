"""Tool registry for managing and dispatching tools"""

from typing import Dict, List, Callable, Any
import mcp.types as types


class ToolRegistry:
    """Central registry for all MCP tools"""
    
    def __init__(self):
        self._tools: Dict[str, types.Tool] = {}
        self._handlers: Dict[str, Callable] = {}
    
    def register(self, tool: types.Tool, handler: Callable):
        """Register a tool with its handler"""
        self._tools[tool.name] = tool
        self._handlers[tool.name] = handler
    
    def get_tools(self) -> List[types.Tool]:
        """Get all registered tools"""
        return list(self._tools.values())
    
    def get_handler(self, name: str) -> Callable:
        """Get handler for a tool"""
        return self._handlers.get(name)
    
    def has_tool(self, name: str) -> bool:
        """Check if a tool is registered"""
        return name in self._tools


# Global registry instance
registry = ToolRegistry()