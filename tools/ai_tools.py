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
    description="以资深软件架构师的视角对新架构代码进行严格的一致性审计，通过添加注释和异常标记所有与原架构不一致的地方。在审计完成后会修改新架构代码，提供参考注释，并将将不一致内容使用raise NotImplementedError替换。",
    inputSchema={
        "type": "object",
        "properties": {
            "old_file": {
                "type": "string",
                "description": "原架构文件路径（作为审计的参考基准），绝对路径"
            },
            "new_file": {
                "type": "string", 
                "description": "新架构文件路径（将被审计并标记不一致之处），绝对路径"
            },
            "exemption_list": {
                "type": "string",
                "description": "豁免规则列表变量名称（从list_variables中读取），可选"
            }
        },
        "required": ["old_file", "new_file"]
    }
)

def register_ai_tools():
    """Register all AI-powered tools"""
    registry.register(audit_architecture_consistency_tool, handle_audit_architecture_consistency)