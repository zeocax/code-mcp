"""Prompt registry for managing prompts"""

from typing import Dict, List, Optional
import mcp.types as types


class PromptRegistry:
    """Central registry for all MCP prompts"""
    
    def __init__(self):
        self._prompts: Dict[str, types.Prompt] = {}
    
    def register(self, prompt: types.Prompt):
        """Register a prompt"""
        self._prompts[prompt.name] = prompt
    
    def get_prompts(self) -> List[types.Prompt]:
        """Get all registered prompts"""
        return list(self._prompts.values())
    
    def get_prompt(self, name: str) -> Optional[types.Prompt]:
        """Get a specific prompt by name"""
        return self._prompts.get(name)
    
    def has_prompt(self, name: str) -> bool:
        """Check if a prompt is registered"""
        return name in self._prompts


# Global prompt registry instance
prompt_registry = PromptRegistry()