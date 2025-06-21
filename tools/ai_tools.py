"""AI-powered code tools"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import mcp.types as types
from .registry import registry
from handlers.ai_handler import handle_audit_architecture_consistency

# Define AI-powered tools
audit_architecture_consistency_tool = types.Tool(
    name="audit_architecture_consistency",
    description="以资深软件架构师的视角对新架构代码进行严格的一致性审计，通过添加注释和异常标记所有与原架构不一致的地方",
    inputSchema={
        "type": "object",
        "properties": {
            "old_file": {
                "type": "string",
                "description": "原架构文件路径（作为审计的参考基准）"
            },
            "new_file": {
                "type": "string", 
                "description": "新架构文件路径（将被审计并标记不一致之处）"
            },
            "backup": {
                "type": "boolean",
                "description": "审计前是否创建备份文件（默认：true）"
            }
        },
        "required": ["old_file", "new_file"]
    }
)

def register_ai_tools():
    """Register all AI-powered tools"""
    registry.register(audit_architecture_consistency_tool, handle_audit_architecture_consistency)