"""AI-powered code modification handlers"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import List, Dict, Any
import mcp.types as types
from core.ai_service import ai_service
from core.project_manager import ProjectManager

# Initialize with explicit project root
pm = ProjectManager()
print(f"[DEBUG] AI Handler - ProjectManager initialized with root: {pm.project_root}")

async def handle_audit_architecture_consistency(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle audit_architecture_consistency tool call"""
    old_file = arguments.get("old_file")
    new_file = arguments.get("new_file")
    exemption_file = arguments.get("exemption_file")
    
    if not old_file or not new_file:
        return [types.TextContent(type="text", text="Error: old_file and new_file are required")]
    
    try:
        # Read both files
        with open(old_file, 'r', encoding='utf-8') as f:
            old_code = f.read()
        with open(new_file, 'r', encoding='utf-8') as f:
            new_code = f.read()
        
        # Use AI to audit consistency with exemption file
        audited_code = await ai_service.audit_architecture_consistency(old_code, new_code, exemption_file)
        
        # Write the audited code back to new_file
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write(audited_code)
        
        # Update file status to audited after successful audit
        status_updated = False
        status_error = None
        try:
            print(f"[DEBUG] Attempting to update file status for: {new_file}")
            status_updated = pm.update_file_status(new_file, audited=True)
            print(f"[DEBUG] update_file_status returned: {status_updated}")
        except Exception as e:
            status_error = str(e)
            print(f"[ERROR] Exception in update_file_status: {status_error}")
            import traceback
            traceback.print_exc()
        
        # Prepare result message
        critical_errors = audited_code.count("CRITICAL_ERROR")
        risk_infos = audited_code.count("RISK_INFO")
        
        result_msg = f"审计完成，共发现{critical_errors}处严重错误，{risk_infos}处风险信息"
        
        if status_updated:
            result_msg += "\n✓ 文件审计状态已更新"
        elif status_error:
            result_msg += f"\n⚠️ 文件状态更新失败: {status_error}"
        else:
            result_msg += "\n⚠️ 文件状态更新失败"
            
        return [types.TextContent(type="text", text=result_msg)]
        
    except FileNotFoundError as e:
        return [types.TextContent(type="text", text=f"Error: File not found - {str(e)}")]
    except ValueError as e:
        return [types.TextContent(type="text", text=f"Configuration error: {str(e)}")]
    except ImportError as e:
        return [types.TextContent(type="text", text=f"Missing dependency: {str(e)}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error during architecture consistency audit: {str(e)}")]