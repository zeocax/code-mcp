"""Code search and analysis tools"""

import mcp.types as types
from .registry import registry
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from handlers.search_handler import handle_search_code, handle_find_definition
from handlers.analyze_handler import handle_analyze_structure


# Define code operation tools
search_code_tool = types.Tool(
    name="search_code",
    description="Search for patterns in code files",
    inputSchema={
        "type": "object",
        "properties": {
            "pattern": {
                "type": "string",
                "description": "Search pattern (regex supported)"
            },
            "directory": {
                "type": "string",
                "description": "Directory to search in (default: current)"
            },
            "file_pattern": {
                "type": "string",
                "description": "File pattern to include (e.g., '*.py')"
            },
            "case_sensitive": {
                "type": "boolean",
                "description": "Case sensitive search (default: true)"
            }
        },
        "required": ["pattern"]
    }
)

find_definition_tool = types.Tool(
    name="find_definition",
    description="Find definition of a symbol in code",
    inputSchema={
        "type": "object",
        "properties": {
            "symbol": {
                "type": "string",
                "description": "Symbol name to find"
            },
            "directory": {
                "type": "string",
                "description": "Directory to search in"
            },
            "language": {
                "type": "string",
                "description": "Programming language (python, javascript, etc.)"
            }
        },
        "required": ["symbol"]
    }
)

analyze_structure_tool = types.Tool(
    name="analyze_structure",
    description="Analyze code structure (classes, functions, etc.)",
    inputSchema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to the file to analyze"
            },
            "include_docstrings": {
                "type": "boolean",
                "description": "Include docstrings in analysis (default: false)"
            }
        },
        "required": ["path"]
    }
)


def register_code_tools():
    """Register all code operation tools"""
    registry.register(search_code_tool, handle_search_code)
    registry.register(find_definition_tool, handle_find_definition)
    registry.register(analyze_structure_tool, handle_analyze_structure)