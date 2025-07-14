"""AI-powered code modification handlers"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import List, Dict, Any
import mcp.types as types
from core.ai_service import ai_service
from core.project_manager import ProjectManager, FileStatus
import shutil
from datetime import datetime

pm = ProjectManager()

async def handle_audit_architecture_consistency(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle audit_architecture_consistency tool call"""
    old_file = arguments.get("old_file")
    new_file = arguments.get("new_file")
    exemption_list_name = arguments.get("exemption_list")
    
    if not old_file or not new_file:
        return [types.TextContent(type="text", text="Error: old_file and new_file are required")]
    
    try:
        # Read both files
        with open(old_file, 'r', encoding='utf-8') as f:
            old_code = f.read()
        with open(new_file, 'r', encoding='utf-8') as f:
            new_code = f.read()
        
        # Read user exemptions from list variable if provided
        user_exemptions = ""
        if exemption_list_name:
            exemption_data = pm.read_list_variable(exemption_list_name)
            if exemption_data:
                # Join list items into a single string
                user_exemptions = "\n".join(exemption_data["items"])
                
                # Check if user confirmation is needed
                if exemption_data.get("need_user_confirmation", False):
                    return [types.TextContent(type="text", text=f"Error: Exemption list '{exemption_list_name}' does not need user confirmation, please create a new exemption list with need_user_confirmation set to True")]
                    # Note: In a real implementation, this would trigger a confirmation dialog
                    # print(f"[INFO] Using exemption list '{exemption_list_name}' which requires user confirmation")
            else:
                return [types.TextContent(type="text", text=f"Error: Exemption list not found: {exemption_list_name}")]
        
        # Analyze differences
        # analysis = await ai_service.analyze_architecture_diff(old_code, new_code)
        
        # Use AI to audit consistency
        audited_code = await ai_service.audit_architecture_consistency(old_code, new_code, user_exemptions)
        
        # Write the audited code back to new_file
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write(audited_code)
        
        # Update file status to reviewed after successful audit
        try:
            pm.update_file_status(new_file, FileStatus.REVIEWED)
        except Exception as e:
            # Log error but don't fail the audit
            print(f"Warning: Failed to update file status: {str(e)}")
        
        # Prepare result message
        # result_lines = [
        #     f"Successfully completed architecture consistency audit for {new_file}",
        # ]
        
        # if backup:
        #     result_lines.append(f"Backup saved: {backup_path}")
        
        # result_lines.append("\n新架构文件已完成严格审计，所有不一致之处已通过注释和异常进行标记。")
        critical_errors = audited_code.count("CRITICAL_ERROR")
        risk_infos = audited_code.count("RISK_INFO")
        return [types.TextContent(type="text", text=f"审计完成，共发现{critical_errors}处严重错误，{risk_infos}处风险信息")]
        
    except FileNotFoundError as e:
        return [types.TextContent(type="text", text=f"Error: File not found - {str(e)}")]
    except ValueError as e:
        return [types.TextContent(type="text", text=f"Configuration error: {str(e)}")]
    except ImportError as e:
        return [types.TextContent(type="text", text=f"Missing dependency: {str(e)}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error during architecture consistency audit: {str(e)}")]