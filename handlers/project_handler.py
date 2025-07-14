"""Project management handlers"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import List, Dict, Any
import mcp.types as types
from core.project_manager import ProjectManager


# Initialize project manager
pm = ProjectManager()


# Plans handlers
async def handle_create_plan(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle create_plan tool call"""
    content = arguments.get("content")
    title = arguments.get("title")
    
    if not content:
        return [types.TextContent(type="text", text="Error: content is required")]
    
    try:
        plan_id = pm.create_plan(content, title)
        return [types.TextContent(type="text", text=f"Successfully created plan {plan_id}: {title or 'Untitled'}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error creating plan: {str(e)}")]


async def handle_read_plan(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle read_plan tool call"""
    plan_id = arguments.get("plan_id")
    
    try:
        if plan_id:
            # Read specific plan
            plan = pm.read_plan(plan_id)
            if plan:
                plan_text = f"Plan {plan.get('id', 'N/A')}: {plan.get('title', 'Untitled')}\n"
                plan_text += f"Content: {plan.get('content', 'N/A')}\n"
                if 'created_at' in plan:
                    plan_text += f"Created: {plan['created_at']}\n"
                if 'updated_at' in plan:
                    plan_text += f"Updated: {plan['updated_at']}"
                return [types.TextContent(type="text", text=plan_text)]
            else:
                return [types.TextContent(type="text", text=f"No plan found with ID: {plan_id}")]
        else:
            # Read all plans
            plans = pm.read_all_plans()
            if plans:
                result = "All plans:\n"
                for plan in plans:
                    result += f"\n[{plan.get('id', 'N/A')}] {plan.get('title', 'Untitled')}:\n"
                    result += f"  Content: {plan.get('content', 'N/A')}\n"
                    result += "-" * 40 + "\n"
                return [types.TextContent(type="text", text=result)]
            else:
                return [types.TextContent(type="text", text="No plans found")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error reading plan: {str(e)}")]


async def handle_update_plan(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle update_plan tool call"""
    plan_id = arguments.get("plan_id")
    content = arguments.get("content")
    title = arguments.get("title")
    
    if not plan_id or not content:
        return [types.TextContent(type="text", text="Error: plan_id and content are required")]
    
    try:
        success = pm.update_plan(plan_id, content, title)
        if success:
            return [types.TextContent(type="text", text=f"Successfully updated plan {plan_id}")]
        else:
            return [types.TextContent(type="text", text=f"Plan not found with ID: {plan_id}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error updating plan: {str(e)}")]


async def handle_delete_plan(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle delete_plan tool call"""
    plan_id = arguments.get("plan_id")
    
    if not plan_id:
        return [types.TextContent(type="text", text="Error: plan_id is required")]
    
    try:
        success = pm.delete_plan(plan_id)
        if success:
            return [types.TextContent(type="text", text=f"Successfully deleted plan {plan_id}")]
        else:
            return [types.TextContent(type="text", text=f"Plan not found with ID: {plan_id}")]
    except ValueError as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error deleting plan: {str(e)}")]


# Docs handlers
async def handle_create_doc(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle create_doc tool call"""
    directory = arguments.get("directory")
    content = arguments.get("content")
    
    if not directory or not content:
        return [types.TextContent(type="text", text="Error: directory and content are required")]
    
    try:
        success = pm.create_doc(directory, content)
        if success:
            return [types.TextContent(type="text", text=f"Successfully created documentation for {directory}")]
        else:
            return [types.TextContent(type="text", text=f"Failed to create documentation for {directory}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error creating documentation: {str(e)}")]


async def handle_read_doc(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle read_doc tool call"""
    directory = arguments.get("directory")
    
    try:
        if directory:
            # Read specific doc
            doc = pm.read_doc(directory)
            if doc:
                return [types.TextContent(type="text", text=f"Documentation for {directory}:\n{doc}")]
            else:
                return [types.TextContent(type="text", text=f"No documentation found for {directory}")]
        else:
            # Read all docs
            docs = pm.read_all_docs()
            if docs:
                result = "All documentation:\n"
                for dir_path, doc_content in docs.items():
                    result += f"\n{dir_path}:\n{doc_content}\n" + "-" * 40 + "\n"
                return [types.TextContent(type="text", text=result)]
            else:
                return [types.TextContent(type="text", text="No documentation found")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error reading documentation: {str(e)}")]


async def handle_update_doc(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle update_doc tool call"""
    directory = arguments.get("directory")
    content = arguments.get("content")
    
    if not directory or not content:
        return [types.TextContent(type="text", text="Error: directory and content are required")]
    
    try:
        success = pm.update_doc(directory, content)
        if success:
            return [types.TextContent(type="text", text=f"Successfully updated documentation for {directory}")]
        else:
            return [types.TextContent(type="text", text=f"Documentation not found for {directory}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error updating documentation: {str(e)}")]


# TODO handlers
async def handle_create_todo(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle create_todo tool call"""
    content = arguments.get("content")
    related_plan = arguments.get("related_plan")
    position = arguments.get("position", "end")
    
    if not content or not related_plan:
        return [types.TextContent(type="text", text="Error: content and related_plan are required")]
    
    try:
        todo_id = pm.create_todo(content, related_plan, position)
        return [types.TextContent(type="text", text=f"Successfully created todo: {todo_id} (linked to plan ID: {related_plan}) at {position}")]
    except ValueError as e:
        # Handle specific error when plan doesn't exist
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error creating todo: {str(e)}")]


async def handle_read_todos(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle read_todos tool call"""
    status = arguments.get("status", "pending")
    
    try:
        todos = pm.read_todos(status)
        if todos:
            result = f"TODOs ({status}):\n"
            for todo in todos:
                result += f"\n[{todo['id']}] {todo['content']}"
                if todo.get('related_plan'):
                    result += f" (Plan ID: {todo['related_plan']})"
                result += f"\n    Created: {todo['created_at']}"
                if todo.get('completed_at'):
                    result += f"\n    Completed: {todo['completed_at']}"
                if todo.get('git_log'):
                    result += f"\n    Git Log:\n{todo['git_log']}"
                result += "\n"
            return [types.TextContent(type="text", text=result)]
        else:
            return [types.TextContent(type="text", text=f"No {status} todos found")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error reading todos: {str(e)}")]


async def handle_finish_todo(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle finish_todo tool call"""
    todo_id = arguments.get("todo_id")
    git_log = arguments.get("git_log")
    
    if not todo_id or not git_log:
        return [types.TextContent(type="text", text="Error: todo_id and git_log are required")]
    
    try:
        success = pm.update_todo(todo_id, "completed", git_log)
        if success:
            return [types.TextContent(type="text", text=f"Successfully marked todo {todo_id} as completed")]
        else:
            return [types.TextContent(type="text", text=f"Todo {todo_id} not found")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error finishing todo: {str(e)}")]


async def handle_delete_todo(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle delete_todo tool call"""
    todo_id = arguments.get("todo_id")
    
    if not todo_id:
        return [types.TextContent(type="text", text="Error: todo_id is required")]
    
    try:
        success = pm.delete_todo(todo_id)
        if success:
            return [types.TextContent(type="text", text=f"Successfully deleted todo {todo_id}")]
        else:
            return [types.TextContent(type="text", text=f"Todo {todo_id} not found")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error deleting todo: {str(e)}")]


async def handle_move_todo(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle move_todo tool call"""
    todo_id = arguments.get("todo_id")
    position = arguments.get("position")
    
    if not todo_id or not position:
        return [types.TextContent(type="text", text="Error: todo_id and position are required")]
    
    if position not in ["start", "end"]:
        return [types.TextContent(type="text", text="Error: position must be 'start' or 'end'")]
    
    try:
        success = pm.move_todo(todo_id, position)
        if success:
            return [types.TextContent(type="text", text=f"Successfully moved todo {todo_id} to {position}")]
        else:
            return [types.TextContent(type="text", text=f"Todo {todo_id} not found")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error moving todo: {str(e)}")]


# Recent changes handlers
async def handle_update_recent_changes(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle update_recent_changes tool call"""
    current = arguments.get("current", [])
    archived = arguments.get("archived", [])
    
    try:
        success = pm.update_recent_changes(current, archived)
        if success:
            return [types.TextContent(type="text", text="Successfully updated recent changes")]
        else:
            return [types.TextContent(type="text", text="Failed to update recent changes")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error updating recent changes: {str(e)}")]


async def handle_get_recent_changes(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle get_recent_changes tool call"""
    try:
        changes = pm.get_recent_changes()
        result = "Recent Changes:\n\nCurrent:\n"
        for change in changes.get("current", []):
            result += f"- {change}\n"
        
        result += "\nArchived:\n"
        for change in changes.get("archived", []):
            result += f"- {change}\n"
        
        return [types.TextContent(type="text", text=result)]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error getting recent changes: {str(e)}")]


# File status handlers
async def handle_update_file_status(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle update_file_status tool call"""
    file_path = arguments.get("file_path")
    status = arguments.get("status")
    
    if not file_path or not status:
        return [types.TextContent(type="text", text="Error: file_path and status are required")]
    
    try:
        # Convert status string to enum
        status_enum = FileStatus(status)
        success = pm.update_file_status(file_path, status_enum)
        if success:
            return [types.TextContent(type="text", text=f"Successfully updated {file_path} status to {status}")]
        else:
            return [types.TextContent(type="text", text=f"Failed to update status for {file_path}")]
    except ValueError:
        return [types.TextContent(type="text", text=f"Invalid status: {status}. Valid values: plan, impl, reviewed, tested")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error updating file status: {str(e)}")]


async def handle_get_file_status(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle get_file_status tool call"""
    file_path = arguments.get("file_path")
    
    if not file_path:
        return [types.TextContent(type="text", text="Error: file_path is required")]
    
    try:
        status_info = pm.get_file_status(file_path)
        if status_info:
            result = f"File Status for {file_path}:\n"
            result += f"- Status: {status_info.status}\n"
            result += f"- Hash: {status_info.hash[:16]}...\n"
            result += f"- Last Modified: {status_info.last_modified}"
            return [types.TextContent(type="text", text=result)]
        else:
            return [types.TextContent(type="text", text=f"No status information found for {file_path}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error getting file status: {str(e)}")]


async def handle_list_file_status(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle list_file_status tool call"""
    directory = arguments.get("directory")
    
    try:
        table = pm.list_file_status(directory)
        return [types.TextContent(type="text", text=table)]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error listing file status: {str(e)}")]


# List variables handlers
async def handle_create_list_variable(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle create_list_variable tool call"""
    name = arguments.get("name")
    items = arguments.get("items", [])
    need_user_confirmation = arguments.get("need_user_confirmation", False)
    
    if not name:
        return [types.TextContent(type="text", text="Error: name is required")]
    
    try:
        success = pm.create_list_variable(name, items, need_user_confirmation)
        if success:
            return [types.TextContent(type="text", text=f"Successfully created list variable: {name}")]
        else:
            return [types.TextContent(type="text", text=f"Failed to create list variable: {name}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error creating list variable: {str(e)}")]


async def handle_read_list_variable(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle read_list_variable tool call"""
    name = arguments.get("name")
    
    try:
        if name:
            # Read specific variable
            var_data = pm.read_list_variable(name)
            if var_data:
                result = f"List Variable: {name}\n"
                result += f"Items ({len(var_data['items'])}):\n"
                for item in var_data['items']:
                    result += f"  - {item}\n"
                result += f"Need User Confirmation: {var_data['need_user_confirmation']}\n"
                result += f"Created: {var_data.get('created_at', 'Unknown')}\n"
                result += f"Updated: {var_data.get('updated_at', 'Unknown')}"
                return [types.TextContent(type="text", text=result)]
            else:
                return [types.TextContent(type="text", text=f"List variable not found: {name}")]
        else:
            # Read all variables
            all_vars = pm.read_all_list_variables()
            if all_vars:
                result = "All List Variables:\n"
                for var_name, var_data in all_vars.items():
                    result += f"\n{var_name}:\n"
                    result += f"  Items: {len(var_data['items'])} items\n"
                    result += f"  Need Confirmation: {var_data['need_user_confirmation']}\n"
                return [types.TextContent(type="text", text=result)]
            else:
                return [types.TextContent(type="text", text="No list variables found")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error reading list variable: {str(e)}")]


async def handle_update_list_variable(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle update_list_variable tool call"""
    name = arguments.get("name")
    items = arguments.get("items")
    need_user_confirmation = arguments.get("need_user_confirmation")
    
    if not name:
        return [types.TextContent(type="text", text="Error: name is required")]
    
    if items is None and need_user_confirmation is None:
        return [types.TextContent(type="text", text="Error: at least one of items or need_user_confirmation must be provided")]
    
    try:
        success = pm.update_list_variable(name, items, need_user_confirmation)
        if success:
            return [types.TextContent(type="text", text=f"Successfully updated list variable: {name}")]
        else:
            return [types.TextContent(type="text", text=f"List variable not found: {name}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error updating list variable: {str(e)}")]


async def handle_delete_list_variable(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle delete_list_variable tool call"""
    name = arguments.get("name")
    
    if not name:
        return [types.TextContent(type="text", text="Error: name is required")]
    
    try:
        success = pm.delete_list_variable(name)
        if success:
            return [types.TextContent(type="text", text=f"Successfully deleted list variable: {name}")]
        else:
            return [types.TextContent(type="text", text=f"List variable not found: {name}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error deleting list variable: {str(e)}")]


async def handle_append_to_list_variable(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle append_to_list_variable tool call"""
    name = arguments.get("name")
    item = arguments.get("item")
    
    if not name or not item:
        return [types.TextContent(type="text", text="Error: name and item are required")]
    
    try:
        success = pm.append_to_list_variable(name, item)
        if success:
            return [types.TextContent(type="text", text=f"Successfully appended to list variable: {name}")]
        else:
            return [types.TextContent(type="text", text=f"List variable not found: {name}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error appending to list variable: {str(e)}")]


async def handle_remove_from_list_variable(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle remove_from_list_variable tool call"""
    name = arguments.get("name")
    item = arguments.get("item")
    
    if not name or not item:
        return [types.TextContent(type="text", text="Error: name and item are required")]
    
    try:
        success = pm.remove_from_list_variable(name, item)
        if success:
            return [types.TextContent(type="text", text=f"Successfully removed from list variable: {name}")]
        else:
            return [types.TextContent(type="text", text=f"List variable or item not found: {name}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error removing from list variable: {str(e)}")]