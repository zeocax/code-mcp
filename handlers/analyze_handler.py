"""Code analysis handlers"""

from typing import List, Dict, Any
import mcp.types as types
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.code_parser import CodeParser


parser = CodeParser()


async def handle_analyze_structure(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle analyze_structure tool call"""
    path = arguments.get("path")
    include_docstrings = arguments.get("include_docstrings", False)
    
    if not path:
        return [types.TextContent(type="text", text="Error: path is required")]
    
    try:
        structure = await parser.analyze_structure(path, include_docstrings)
        
        # Format output
        lines = []
        lines.append(f"File: {structure['file']}")
        lines.append(f"Language: {structure['language']}")
        lines.append("")
        
        if structure.get('imports'):
            lines.append("Imports:")
            for imp in structure['imports']:
                lines.append(f"  - {imp}")
            lines.append("")
        
        if structure.get('classes'):
            lines.append("Classes:")
            for cls in structure['classes']:
                lines.append(f"  {cls['name']} (line {cls['line']})")
                for method in cls.get('methods', []):
                    lines.append(f"    - {method['name']}() (line {method['line']})")
            lines.append("")
        
        if structure.get('functions'):
            lines.append("Functions:")
            for func in structure['functions']:
                lines.append(f"  - {func['name']}() (line {func['line']})")
        
        return [types.TextContent(type="text", text="\n".join(lines))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error analyzing structure: {str(e)}")]