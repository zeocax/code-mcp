"""Search operation handlers"""

import re
from typing import List, Dict, Any
import mcp.types as types
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.file_system import FileSystem
from core.code_parser import CodeParser


fs = FileSystem()
parser = CodeParser()


async def handle_search_code(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle search_code tool call"""
    pattern = arguments.get("pattern")
    directory = arguments.get("directory", ".")
    file_pattern = arguments.get("file_pattern", "*")
    case_sensitive = arguments.get("case_sensitive", True)
    
    if not pattern:
        return [types.TextContent(type="text", text="Error: pattern is required")]
    
    try:
        # Compile regex pattern
        flags = 0 if case_sensitive else re.IGNORECASE
        regex = re.compile(pattern, flags)
        
        # Search files
        results = []
        files = await fs.list_files(directory, file_pattern, recursive=True)
        
        for file_path in files[:100]:  # Limit to 100 files
            try:
                content = await fs.read_file(file_path)
                lines = content.splitlines()
                
                for i, line in enumerate(lines, 1):
                    if regex.search(line):
                        results.append(f"{file_path}:{i}: {line.strip()}")
                        if len(results) >= 100:  # Limit results
                            break
            except:
                continue
            
            if len(results) >= 100:
                results.append("... (limited to 100 results)")
                break
        
        if not results:
            return [types.TextContent(type="text", text="No matches found")]
        
        return [types.TextContent(type="text", text="\n".join(results))]
    except re.error as e:
        return [types.TextContent(type="text", text=f"Invalid regex pattern: {str(e)}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error searching: {str(e)}")]


async def handle_find_definition(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle find_definition tool call"""
    symbol = arguments.get("symbol")
    directory = arguments.get("directory", ".")
    language = arguments.get("language")
    
    if not symbol:
        return [types.TextContent(type="text", text="Error: symbol is required")]
    
    try:
        # Determine file pattern based on language
        if language == "python":
            file_pattern = "*.py"
        elif language == "javascript":
            file_pattern = "*.js"
        else:
            file_pattern = "*"
        
        results = []
        files = await fs.list_files(directory, file_pattern, recursive=True)
        
        for file_path in files[:50]:  # Limit files to search
            try:
                definitions = await parser.find_definitions(file_path, symbol)
                for defn in definitions:
                    results.append(f"{file_path}:{defn['line']}: {defn['type']} {defn['name']}")
            except:
                continue
        
        if not results:
            return [types.TextContent(type="text", text=f"No definition found for '{symbol}'")]
        
        return [types.TextContent(type="text", text="\n".join(results))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error finding definition: {str(e)}")]