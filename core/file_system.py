"""File system operations"""

import os
import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import fnmatch


class FileSystem:
    """Handles file system operations"""
    
    def __init__(self):
        self.supported_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h',
            '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala',
            '.r', '.m', '.mm', '.sql', '.sh', '.yaml', '.yml', '.json', '.xml'
        }
    
    async def read_file(self, path: str, encoding: str = 'utf-8') -> str:
        """Read file contents"""
        path_obj = Path(path)
        if not path_obj.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        # Read file asynchronously
        loop = asyncio.get_event_loop()
        content = await loop.run_in_executor(
            None, path_obj.read_text, encoding
        )
        return content
    
    async def list_files(self, directory: str = ".", pattern: str = "*", recursive: bool = False) -> List[str]:
        """List files matching pattern"""
        path_obj = Path(directory)
        if not path_obj.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        files = []
        
        if recursive:
            for root, dirs, filenames in os.walk(path_obj):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for filename in filenames:
                    if fnmatch.fnmatch(filename, pattern):
                        file_path = os.path.join(root, filename)
                        # Only include supported code files
                        if any(file_path.endswith(ext) for ext in self.supported_extensions):
                            files.append(os.path.relpath(file_path, directory))
        else:
            for item in path_obj.iterdir():
                if item.is_file() and fnmatch.fnmatch(item.name, pattern):
                    if any(item.name.endswith(ext) for ext in self.supported_extensions):
                        files.append(item.name)
        
        return sorted(files)
    
    async def get_file_info(self, path: str) -> Dict[str, Any]:
        """Get file information"""
        path_obj = Path(path)
        if not path_obj.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        stat = path_obj.stat()
        
        info = {
            'name': path_obj.name,
            'path': str(path_obj.absolute()),
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'type': path_obj.suffix or 'unknown'
        }
        
        # Add line count for text files
        if path_obj.suffix in self.supported_extensions:
            try:
                content = await self.read_file(path)
                info['lines'] = len(content.splitlines())
            except:
                pass
        
        return info