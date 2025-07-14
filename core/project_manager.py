"""Project management core module for tracking plans, todos, changes and file status"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import hashlib
from dataclasses import dataclass, asdict
from enum import Enum


class FileStatus(Enum):
    """File status enumeration"""
    AUDITED = "audited"


@dataclass
class Todo:
    """Todo item data class"""
    id: str
    content: str
    related_plan: str  # Plan ID (plan_xxx or legacy_xxx)
    status: str = "pending"
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()




class ProjectManager:
    """Manages project metadata including plans, todos, changes and file status"""
    
    def __init__(self, project_root: Optional[str] = None):
        """Initialize project manager
        
        Args:
            project_root: Root directory of the project. If None, uses current directory
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.meta_file = self.project_root / "project_meta.json"
        self._ensure_meta_file()
    
    def _ensure_meta_file(self):
        """Ensure project meta file exists with default structure"""
        if not self.meta_file.exists():
            default_meta = {
                "plans": {},
                "docs": {},
                "todos": [],
                "recent_changes": {
                    "current": [],
                    "archived": []
                },
                "file_status": {},
                "list_variables": {}
            }
            self._save_meta(default_meta)
    
    def _load_meta(self) -> Dict[str, Any]:
        """Load project metadata from file"""
        try:
            with open(self.meta_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self._ensure_meta_file()
            with open(self.meta_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    def _save_meta(self, meta: Dict[str, Any]):
        """Save project metadata to file"""
        with open(self.meta_file, 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of a file"""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except FileNotFoundError:
            return ""
    
    # Plans management
    def create_plan(self, content: str, title: Optional[str] = None) -> str:
        """Create a plan
        
        Args:
            content: Plan content
            title: Optional plan title
            
        Returns:
            Plan ID
        """
        meta = self._load_meta()
        
        # Convert plans to list format if needed
        if not isinstance(meta["plans"], list):
            self._convert_plans_to_list(meta)
        
        # Generate unique plan ID
        existing_ids = [p['id'] for p in meta["plans"] if 'id' in p]
        plan_number = len(existing_ids) + 1
        plan_id = f"plan_{plan_number:03d}"
        
        new_plan = {
            "id": plan_id,
            "content": content,
            "title": title or f"Plan {plan_number}",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        meta["plans"].append(new_plan)
        self._save_meta(meta)
        return plan_id
    
    def read_plan(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """Read plan by ID"""
        meta = self._load_meta()
        plans = meta["plans"]
        
        # Handle both list and dict formats
        if isinstance(plans, list):
            for plan in plans:
                if plan.get('id') == plan_id:
                    return plan
        else:
            # Legacy dict format
            for directory, plan_content in plans.items():
                if f"legacy_{directory}" == plan_id:
                    return {"id": plan_id, "content": plan_content, "directory": directory}
        return None
    
    def read_all_plans(self) -> List[Dict[str, Any]]:
        """Read all plans"""
        meta = self._load_meta()
        plans = meta["plans"]
        
        # Handle both list and dict formats
        if isinstance(plans, list):
            return plans
        else:
            # Convert dict to list format
            self._convert_plans_to_list(meta)
            return meta["plans"]
    
    def update_plan(self, plan_id: str, content: str, title: Optional[str] = None) -> bool:
        """Update plan by ID"""
        meta = self._load_meta()
        
        # Convert to list format if needed
        if not isinstance(meta["plans"], list):
            self._convert_plans_to_list(meta)
        
        for plan in meta["plans"]:
            if plan.get('id') == plan_id:
                plan["content"] = content
                if title is not None:
                    plan["title"] = title
                plan["updated_at"] = datetime.now().isoformat()
                self._save_meta(meta)
                return True
        return False
    
    def delete_plan(self, plan_id: str) -> bool:
        """Delete plan by ID"""
        meta = self._load_meta()
        
        # Convert to list format if needed
        if not isinstance(meta["plans"], list):
            self._convert_plans_to_list(meta)
        
        for i, plan in enumerate(meta["plans"]):
            if plan.get('id') == plan_id:
                # Check if any todos are linked to this plan
                linked_todos = [t for t in meta["todos"] if t.get('related_plan') == plan_id]
                if linked_todos:
                    raise ValueError(f"Cannot delete plan {plan_id}: {len(linked_todos)} todos are linked to it")
                meta["plans"].pop(i)
                self._save_meta(meta)
                return True
        return False
    
    def _convert_plans_to_list(self, meta: Dict[str, Any]):
        """Convert plans from dict to list format"""
        if isinstance(meta["plans"], dict):
            old_plans = meta["plans"]
            meta["plans"] = []
            for directory, plan_content in old_plans.items():
                meta["plans"].append({
                    "id": f"legacy_{directory}",
                    "content": plan_content,
                    "directory": directory,
                    "title": f"Legacy: {directory}",
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                })
    
    
    # Docs management
    def create_doc(self, directory: str, content: str) -> bool:
        """Create documentation for a directory"""
        meta = self._load_meta()
        meta["docs"][directory] = content
        self._save_meta(meta)
        return True
    
    def read_doc(self, directory: str) -> Optional[str]:
        """Read documentation for a directory"""
        meta = self._load_meta()
        return meta["docs"].get(directory)
    
    def read_all_docs(self) -> Dict[str, str]:
        """Read all documentation"""
        meta = self._load_meta()
        return meta["docs"]
    
    def update_doc(self, directory: str, content: str) -> bool:
        """Update documentation for a directory"""
        meta = self._load_meta()
        if directory in meta["docs"]:
            meta["docs"][directory] = content
            self._save_meta(meta)
            return True
        return False
    
    # TODO management
    def create_todo(self, content: str, related_plan: str, position: str = "end") -> str:
        """Create a new todo item (must be related to a plan)
        
        Args:
            content: Todo content
            related_plan: Plan ID (must start with 'plan_' or 'legacy_')
            position: Where to insert the todo - "start" or "end" (default)
            
        Returns:
            Todo ID
            
        Raises:
            ValueError: If the related plan doesn't exist
        """
        meta = self._load_meta()
        
        # Verify plan exists
        plan_exists = False
        if isinstance(meta["plans"], list):
            plan_exists = any(p.get('id') == related_plan for p in meta["plans"])
        else:
            # Legacy format check
            if related_plan.startswith('legacy_'):
                directory = related_plan.replace('legacy_', '')
                plan_exists = directory in meta["plans"]
        
        if not plan_exists:
            raise ValueError(f"Plan ID not found: {related_plan}")
        
        todo_id = f"todo_{len(meta['todos']) + 1:03d}"
        todo = Todo(id=todo_id, content=content, related_plan=related_plan)
        
        if position == "start":
            meta["todos"].insert(0, asdict(todo))
        else:
            meta["todos"].append(asdict(todo))
        
        self._save_meta(meta)
        return todo_id
    
    def read_todos(self, status: str = "pending") -> List[Dict[str, Any]]:
        """Read todos by status"""
        meta = self._load_meta()
        return [todo for todo in meta["todos"] if todo["status"] == status]
    
    def update_todo(self, todo_id: str, status: str, git_log: Optional[str] = None) -> bool:
        """Update todo status
        
        Args:
            todo_id: Todo ID to update
            status: New status (pending, completed)
            git_log: Git log entries when marking as completed
        """
        meta = self._load_meta()
        for todo in meta["todos"]:
            if todo["id"] == todo_id:
                todo["status"] = status
                if status == "completed":
                    todo["completed_at"] = datetime.now().isoformat()
                    if git_log:
                        todo["git_log"] = git_log
                self._save_meta(meta)
                return True
        return False
    
    def delete_todo(self, todo_id: str) -> bool:
        """Delete a todo item"""
        meta = self._load_meta()
        for i, todo in enumerate(meta["todos"]):
            if todo["id"] == todo_id:
                meta["todos"].pop(i)
                self._save_meta(meta)
                return True
        return False
    
    def move_todo(self, todo_id: str, position: str) -> bool:
        """Move a todo to start or end of the list
        
        Args:
            todo_id: Todo ID to move
            position: "start" or "end"
        """
        meta = self._load_meta()
        todo_index = None
        todo_item = None
        
        # Find the todo
        for i, todo in enumerate(meta["todos"]):
            if todo["id"] == todo_id:
                todo_index = i
                todo_item = todo
                break
        
        if todo_item is None:
            return False
        
        # Remove from current position
        meta["todos"].pop(todo_index)
        
        # Insert at new position
        if position == "start":
            meta["todos"].insert(0, todo_item)
        else:
            meta["todos"].append(todo_item)
        
        self._save_meta(meta)
        return True
    
    # Recent changes management
    def update_recent_changes(self, current: List[str], archived: List[str]) -> bool:
        """Update recent changes (called by AI after merge)"""
        meta = self._load_meta()
        meta["recent_changes"]["current"] = current
        meta["recent_changes"]["archived"] = archived
        self._save_meta(meta)
        return True
    
    def get_recent_changes(self) -> Dict[str, List[str]]:
        """Get recent changes"""
        meta = self._load_meta()
        return meta["recent_changes"]
    
    # File status management
    def update_file_status(self, file_path: str, audited: bool = True) -> bool:
        """Update file audit status"""
        meta = self._load_meta()
        
        # Convert relative path to absolute and then back to relative for storage
        abs_path = Path(file_path).absolute()
        try:
            rel_path = abs_path.relative_to(self.project_root).as_posix()
        except ValueError:
            # File is outside project root, use absolute path
            rel_path = str(abs_path)
        
        if audited:
            # Mark as audited with timestamp
            meta["file_status"][rel_path] = {
                "audited": True,
                "audited_at": datetime.now().isoformat()
            }
        else:
            # Remove audit status
            if rel_path in meta["file_status"]:
                del meta["file_status"][rel_path]
        
        self._save_meta(meta)
        return True
    
    def get_file_status(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Get file audit status"""
        meta = self._load_meta()
        
        # Convert to relative path for lookup
        abs_path = Path(file_path).absolute()
        try:
            rel_path = abs_path.relative_to(self.project_root).as_posix()
        except ValueError:
            rel_path = str(abs_path)
        
        return meta["file_status"].get(rel_path)
    
    def list_file_status(self, directory: Optional[str] = None) -> str:
        """List files and their audit status as markdown table
        
        Args:
            directory: Optional directory to filter files (relative to project root)
            
        Returns:
            Markdown table with files and audit status
        """
        meta = self._load_meta()
        file_statuses = meta.get("file_status", {})
        
        # Get all files in directory
        if directory:
            search_path = self.project_root / directory
            if not search_path.exists():
                return f"Directory not found: {directory}"
            
            # Find all Python files in directory
            all_files = []
            for file_path in search_path.rglob("*.py"):
                if file_path.is_file():
                    try:
                        rel_path = file_path.relative_to(self.project_root).as_posix()
                        all_files.append(rel_path)
                    except ValueError:
                        pass
        else:
            # List all tracked Python files
            all_files = [f for f in file_statuses.keys() if f.endswith('.py')]
        
        if not all_files:
            return "No Python files found"
        
        # Sort files
        all_files.sort()
        
        # Build markdown table
        table = "| File | Audited |\n"
        table += "|------|---------|\n"
        
        for file_path in all_files:
            status = file_statuses.get(file_path)
            audited = "✓" if status and status.get("audited") else "✗"
            table += f"| {file_path} | {audited} |\n"
        
        return table
    
    # List variables management
    def create_list_variable(self, name: str, items: List[str], need_user_confirmation: bool = False) -> bool:
        """Create a named list variable with optional confirmation requirement"""
        meta = self._load_meta()
        if "list_variables" not in meta:
            meta["list_variables"] = {}
        
        meta["list_variables"][name] = {
            "items": items,
            "need_user_confirmation": need_user_confirmation,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self._save_meta(meta)
        return True
    
    def read_list_variable(self, name: str) -> Optional[Dict[str, Any]]:
        """Read a named list variable"""
        meta = self._load_meta()
        if "list_variables" not in meta:
            return None
        
        return meta.get("list_variables", {}).get(name)
    
    def read_all_list_variables(self) -> Dict[str, Dict[str, Any]]:
        """Read all list variables"""
        meta = self._load_meta()
        return meta.get("list_variables", {})
    
    def update_list_variable(self, name: str, items: Optional[List[str]] = None, 
                           need_user_confirmation: Optional[bool] = None) -> bool:
        """Update a list variable's items and/or confirmation requirement"""
        meta = self._load_meta()
        if "list_variables" not in meta:
            return False
        
        if name in meta["list_variables"]:
            if items is not None:
                meta["list_variables"][name]["items"] = items
            if need_user_confirmation is not None:
                meta["list_variables"][name]["need_user_confirmation"] = need_user_confirmation
            meta["list_variables"][name]["updated_at"] = datetime.now().isoformat()
            self._save_meta(meta)
            return True
        return False
    
    def delete_list_variable(self, name: str) -> bool:
        """Delete a named list variable"""
        meta = self._load_meta()
        if "list_variables" not in meta:
            return False
        if name in meta["list_variables"]:
            del meta["list_variables"][name]
            self._save_meta(meta)
            return True
        return False
    
    def append_to_list_variable(self, name: str, item: str) -> bool:
        """Append an item to a list variable"""
        meta = self._load_meta()
        if "list_variables" not in meta:
            return False
        
        if name in meta["list_variables"]:
            meta["list_variables"][name]["items"].append(item)
            meta["list_variables"][name]["updated_at"] = datetime.now().isoformat()
            self._save_meta(meta)
            return True
        return False
    
    def remove_from_list_variable(self, name: str, item: str) -> bool:
        """Remove an item from a list variable"""
        meta = self._load_meta()
        if "list_variables" not in meta:
            return False
        
        if name in meta["list_variables"] and item in meta["list_variables"][name]["items"]:
            meta["list_variables"][name]["items"].remove(item)
            meta["list_variables"][name]["updated_at"] = datetime.now().isoformat()
            self._save_meta(meta)
            return True
        return False
    
