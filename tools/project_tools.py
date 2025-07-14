"""Project management tools for plans, todos, changes and file status"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import mcp.types as types
from .registry import registry


# Plans tools
create_plan_tool = types.Tool(
    name="create_plan",
    description="创建计划",
    inputSchema={
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "计划内容"
            },
            "title": {
                "type": "string",
                "description": "计划标题（可选）"
            }
        },
        "required": ["content"]
    }
)

read_plan_tool = types.Tool(
    name="read_plan",
    description="读取计划",
    inputSchema={
        "type": "object",
        "properties": {
            "plan_id": {
                "type": "string",
                "description": "计划ID，如果为空则返回所有计划"
            }
        }
    }
)

update_plan_tool = types.Tool(
    name="update_plan",
    description="更新计划",
    inputSchema={
        "type": "object",
        "properties": {
            "plan_id": {
                "type": "string",
                "description": "计划ID"
            },
            "content": {
                "type": "string",
                "description": "新的计划内容"
            },
            "title": {
                "type": "string",
                "description": "新的计划标题（可选）"
            }
        },
        "required": ["plan_id", "content"]
    }
)

delete_plan_tool = types.Tool(
    name="delete_plan",
    description="删除计划",
    inputSchema={
        "type": "object",
        "properties": {
            "plan_id": {
                "type": "string",
                "description": "计划ID"
            }
        },
        "required": ["plan_id"]
    }
)

# Docs tools
create_doc_tool = types.Tool(
    name="create_doc",
    description="创建目录的文档（已实现功能的说明）",
    inputSchema={
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "目录路径"
            },
            "content": {
                "type": "string",
                "description": "文档内容"
            }
        },
        "required": ["directory", "content"]
    }
)

read_doc_tool = types.Tool(
    name="read_doc",
    description="读取目录的文档",
    inputSchema={
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "目录路径，如果为空则返回所有文档"
            }
        }
    }
)

update_doc_tool = types.Tool(
    name="update_doc",
    description="更新目录的文档",
    inputSchema={
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "目录路径"
            },
            "content": {
                "type": "string",
                "description": "新的文档内容"
            }
        },
        "required": ["directory", "content"]
    }
)

# TODO tools
create_todo_tool = types.Tool(
    name="create_todo",
    description="创建待办事项（必须关联到某个计划）",
    inputSchema={
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "待办事项内容"
            },
            "related_plan": {
                "type": "string",
                "description": "关联的计划ID（例如：plan_001）"
            },
            "position": {
                "type": "string",
                "description": "插入位置：start或end（默认end）",
                "enum": ["start", "end"]
            }
        },
        "required": ["content", "related_plan"]
    }
)

read_todos_tool = types.Tool(
    name="read_todos",
    description="读取待办事项",
    inputSchema={
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "description": "待办状态: pending（默认）, completed",
                "enum": ["pending", "completed"]
            }
        }
    }
)

finish_todo_tool = types.Tool(
    name="finish_todo",
    description="完成待办事项（标记为completed并记录git日志）",
    inputSchema={
        "type": "object",
        "properties": {
            "todo_id": {
                "type": "string",
                "description": "待办事项ID"
            },
            "git_log": {
                "type": "string",
                "description": "Git提交日志（必需）"
            }
        },
        "required": ["todo_id", "git_log"]
    }
)

delete_todo_tool = types.Tool(
    name="delete_todo",
    description="删除待办事项",
    inputSchema={
        "type": "object",
        "properties": {
            "todo_id": {
                "type": "string",
                "description": "待办事项ID"
            }
        },
        "required": ["todo_id"]
    }
)

move_todo_tool = types.Tool(
    name="move_todo",
    description="移动待办事项到列表开头或结尾",
    inputSchema={
        "type": "object",
        "properties": {
            "todo_id": {
                "type": "string",
                "description": "待办事项ID"
            },
            "position": {
                "type": "string",
                "description": "目标位置",
                "enum": ["start", "end"]
            }
        },
        "required": ["todo_id", "position"]
    }
)

# Recent changes tool
update_recent_changes_tool = types.Tool(
    name="update_recent_changes",
    description="更新最近的更改记录（由AI调用，合并现有记录和新的更改）",
    inputSchema={
        "type": "object",
        "properties": {
            "current": {
                "type": "array",
                "items": {"type": "string"},
                "description": "合并后的最近更改（C）"
            },
            "archived": {
                "type": "array",
                "items": {"type": "string"},
                "description": "归档的更改（D）"
            }
        },
        "required": ["current", "archived"]
    }
)

get_recent_changes_tool = types.Tool(
    name="get_recent_changes",
    description="获取最近的更改记录",
    inputSchema={
        "type": "object",
        "properties": {}
    }
)

# File status tools
update_file_status_tool = types.Tool(
    name="update_file_status",
    description="更新文件审计状态",
    inputSchema={
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "文件路径"
            },
            "audited": {
                "type": "boolean",
                "description": "是否已审计（true表示已审计，false表示未审计）"
            }
        },
        "required": ["file_path", "audited"]
    }
)

get_file_status_tool = types.Tool(
    name="get_file_status",
    description="获取文件审计状态",
    inputSchema={
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "文件路径"
            }
        },
        "required": ["file_path"]
    }
)

list_file_status_tool = types.Tool(
    name="list_file_status",
    description="列出文件审计状态（返回Markdown表格）",
    inputSchema={
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "目录路径（可选，不提供则列出所有已跟踪文件）"
            }
        }
    }
)

# List variables tools
create_list_variable_tool = types.Tool(
    name="create_list_variable",
    description="创建列表变量（如审计豁免规则等）",
    inputSchema={
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "列表变量名称"
            },
            "items": {
                "type": "array",
                "items": {"type": "string"},
                "description": "列表项内容"
            },
            "need_user_confirmation": {
                "type": "boolean",
                "description": "是否需要用户确认（默认false）"
            }
        },
        "required": ["name", "items"]
    }
)

read_list_variable_tool = types.Tool(
    name="read_list_variable",
    description="读取列表变量（需要用户确认的变量会提示）",
    inputSchema={
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "列表变量名称，如果为空则返回所有列表变量"
            }
        }
    }
)

update_list_variable_tool = types.Tool(
    name="update_list_variable",
    description="更新列表变量",
    inputSchema={
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "列表变量名称"
            },
            "items": {
                "type": "array",
                "items": {"type": "string"},
                "description": "新的列表项内容（可选）"
            },
            "need_user_confirmation": {
                "type": "boolean",
                "description": "是否需要用户确认（可选）"
            }
        },
        "required": ["name"]
    }
)

delete_list_variable_tool = types.Tool(
    name="delete_list_variable",
    description="删除列表变量",
    inputSchema={
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "列表变量名称"
            }
        },
        "required": ["name"]
    }
)

append_to_list_variable_tool = types.Tool(
    name="append_to_list_variable",
    description="向列表变量添加项",
    inputSchema={
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "列表变量名称"
            },
            "item": {
                "type": "string",
                "description": "要添加的项"
            }
        },
        "required": ["name", "item"]
    }
)

remove_from_list_variable_tool = types.Tool(
    name="remove_from_list_variable",
    description="从列表变量删除项",
    inputSchema={
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "列表变量名称"
            },
            "item": {
                "type": "string",
                "description": "要删除的项"
            }
        },
        "required": ["name", "item"]
    }
)



def register_project_tools():
    """Register all project management tools"""
    from handlers.project_handler import (
        handle_create_plan, handle_read_plan, handle_update_plan, handle_delete_plan,
        handle_create_doc, handle_read_doc, handle_update_doc,
        handle_create_todo, handle_read_todos, handle_finish_todo, handle_delete_todo, handle_move_todo,
        handle_update_recent_changes, handle_get_recent_changes,
        handle_update_file_status, handle_get_file_status, handle_list_file_status,
        handle_create_list_variable, handle_read_list_variable, handle_update_list_variable,
        handle_delete_list_variable, handle_append_to_list_variable, handle_remove_from_list_variable
    )
    
    # Register plan tools
    registry.register(create_plan_tool, handle_create_plan)
    registry.register(read_plan_tool, handle_read_plan)
    registry.register(update_plan_tool, handle_update_plan)
    registry.register(delete_plan_tool, handle_delete_plan)
    
    # Register doc tools
    registry.register(create_doc_tool, handle_create_doc)
    registry.register(read_doc_tool, handle_read_doc)
    registry.register(update_doc_tool, handle_update_doc)
    
    # Register todo tools
    registry.register(create_todo_tool, handle_create_todo)
    registry.register(read_todos_tool, handle_read_todos)
    registry.register(finish_todo_tool, handle_finish_todo)
    registry.register(delete_todo_tool, handle_delete_todo)
    registry.register(move_todo_tool, handle_move_todo)
    
    # Register recent changes tools
    registry.register(update_recent_changes_tool, handle_update_recent_changes)
    registry.register(get_recent_changes_tool, handle_get_recent_changes)
    
    # Register file status tools
    registry.register(update_file_status_tool, handle_update_file_status)
    registry.register(get_file_status_tool, handle_get_file_status)
    registry.register(list_file_status_tool, handle_list_file_status)
    
    # Register list variable tools
    registry.register(create_list_variable_tool, handle_create_list_variable)
    registry.register(read_list_variable_tool, handle_read_list_variable)
    registry.register(update_list_variable_tool, handle_update_list_variable)
    registry.register(delete_list_variable_tool, handle_delete_list_variable)
    registry.register(append_to_list_variable_tool, handle_append_to_list_variable)
    registry.register(remove_from_list_variable_tool, handle_remove_from_list_variable)