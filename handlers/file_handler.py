"""File operation handlers"""

import os
from pathlib import Path
from typing import List, Dict, Any
import mcp.types as types
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.file_system import FileSystem


fs = FileSystem()


async def handle_read_file(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle read_file tool call"""
    path = arguments.get("path")
    encoding = arguments.get("encoding", "utf-8")
    
    if not path:
        return [types.TextContent(type="text", text="Error: path is required")]
    
    try:
        content = await fs.read_file(path, encoding)
        return [types.TextContent(type="text", text=content)]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error reading file: {str(e)}")]


async def handle_list_files(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle list_files tool call"""
    directory = arguments.get("directory", ".")
    pattern = arguments.get("pattern", "*")
    recursive = arguments.get("recursive", False)
    
    try:
        files = await fs.list_files(directory, pattern, recursive)
        if not files:
            return [types.TextContent(type="text", text="No files found")]
        
        result = "\n".join(files)
        return [types.TextContent(type="text", text=result)]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error listing files: {str(e)}")]


async def handle_file_info(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle file_info tool call"""
    path = arguments.get("path")
    
    if not path:
        return [types.TextContent(type="text", text="Error: path is required")]
    
    try:
        info = await fs.get_file_info(path)
        result = f"""File: {info['name']}
Path: {info['path']}
Size: {info['size']:,} bytes
Modified: {info['modified']}
Type: {info['type']}
Lines: {info.get('lines', 'N/A')}"""
        return [types.TextContent(type="text", text=result)]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error getting file info: {str(e)}")]