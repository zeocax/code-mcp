"""AI-powered code modification handlers"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import List, Dict, Any
import mcp.types as types
from core.file_system import FileSystem
from core.ai_service import ai_service
import shutil
from datetime import datetime

fs = FileSystem()

async def handle_audit_architecture_consistency(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle audit_architecture_consistency tool call"""
    old_file = arguments.get("old_file")
    new_file = arguments.get("new_file")
    backup = arguments.get("backup", True)
    
    if not old_file or not new_file:
        return [types.TextContent(type="text", text="Error: old_file and new_file are required")]
    
    try:
        # Read both files
        old_code = await fs.read_file(old_file)
        new_code = await fs.read_file(new_file)
        
        # Create backup if requested
        if backup:
            backup_path = f"{new_file}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(new_file, backup_path)
        
        # Analyze differences
        # analysis = await ai_service.analyze_architecture_diff(old_code, new_code)
        
        # Use AI to audit consistency
        audited_code = await ai_service.audit_architecture_consistency(old_code, new_code)
        
        # Write the audited code back to new_file
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write(audited_code)
        
        # Prepare result message
        result_lines = [
            f"Successfully completed architecture consistency audit for {new_file}",
        ]
        
        if backup:
            result_lines.append(f"Backup saved: {backup_path}")
        
        result_lines.append("\n新架构文件已完成严格审计，所有不一致之处已通过注释和异常进行标记。")
        
        return [types.TextContent(type="text", text="\n".join(result_lines))]
        
    except FileNotFoundError as e:
        return [types.TextContent(type="text", text=f"Error: File not found - {str(e)}")]
    except ValueError as e:
        return [types.TextContent(type="text", text=f"Configuration error: {str(e)}")]
    except ImportError as e:
        return [types.TextContent(type="text", text=f"Missing dependency: {str(e)}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error during architecture consistency audit: {str(e)}")]