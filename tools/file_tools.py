"""File operation tools"""

import mcp.types as types
from .registry import registry
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from handlers.file_handler import handle_read_file, handle_list_files, handle_file_info


# Define file operation tools
read_file_tool = types.Tool(
    name="read_file",
    description="Read contents of a file",
    inputSchema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to the file to read"
            },
            "encoding": {
                "type": "string",
                "description": "File encoding (default: utf-8)"
            }
        },
        "required": ["path"]
    }
)

list_files_tool = types.Tool(
    name="list_files",
    description="List files in a directory",
    inputSchema={
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "Directory path (default: current directory)"
            },
            "pattern": {
                "type": "string",
                "description": "File pattern to match (e.g., '*.py')"
            },
            "recursive": {
                "type": "boolean",
                "description": "Search recursively (default: false)"
            }
        }
    }
)

file_info_tool = types.Tool(
    name="file_info",
    description="Get information about a file",
    inputSchema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to the file"
            }
        },
        "required": ["path"]
    }
)


def register_file_tools():
    """Register all file operation tools"""
    registry.register(read_file_tool, handle_read_file)
    registry.register(list_files_tool, handle_list_files)
    registry.register(file_info_tool, handle_file_info)