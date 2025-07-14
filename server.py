#!/usr/bin/env python3
"""MCP server for code analysis with modular architecture"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
from mcp.server.session import ServerSession

# Import tool registry and tools
from tools.registry import registry
from tools.ai_tools import register_ai_tools
from tools.project_tools import register_project_tools

# Import prompt registry and prompts
from prompts.registry import prompt_registry
from prompts.project_prompts import PROJECT_PROMPTS


# Initialize server
server = Server("code-analyzer")

# Register all tools
register_ai_tools()
register_project_tools()

# Register all prompts
for prompt in PROJECT_PROMPTS:
    prompt_registry.register(prompt)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List all registered tools"""
    tools = registry.get_tools()
    # Debug logging
    print(f"[DEBUG] Returning {len(tools)} tools to MCP client")
    for tool in tools:
        print(f"[DEBUG] - {tool.name}")
    return tools


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None, ctx: Any = None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource] | types.CreateMessageRequest:
    """Handle tool calls through registry"""
    
    if not registry.has_tool(name):
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
    
    handler = registry.get_handler(name)
    if not handler:
        return [types.TextContent(type="text", text=f"No handler found for tool: {name}")]
    
    try:
        # Call the appropriate handler with server context
        result = await handler(arguments or {}, server=server)
        
        # Check if handler returned a CreateMessageRequest for sampling
        if isinstance(result, types.CreateMessageRequest):
            return result
            
        return result
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error executing tool {name}: {str(e)}")]


@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """List all registered prompts"""
    prompts = prompt_registry.get_prompts()
    print(f"[DEBUG] Returning {len(prompts)} prompts to MCP client")
    for prompt in prompts:
        print(f"[DEBUG] - {prompt.name}")
        current_path = os.path.dirname(os.path.abspath(__file__))
        print(f"[DEBUG] Total prompts registered: {len(prompts)}", file=open(os.path.join(current_path, "prompts.log"), "a"))
    return prompts


@server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict | None) -> types.GetPromptResult:
    """Get a specific prompt by name"""
    prompt = prompt_registry.get_prompt(name)
    if not prompt:
        raise ValueError(f"Unknown prompt: {name}")
    
    # Build the prompt messages based on the template
    messages = []
    
    if prompt.name == "merge_recent_changes":
        # Get existing changes argument
        if not arguments:
            raise ValueError("Arguments required for merge_recent_changes prompt")
        
        existing_changes = arguments.get("existing_changes")
        if not existing_changes:
            raise ValueError("existing_changes argument is required")
        
        # Import the prompt template
        from prompts.project_prompts import MERGE_RECENT_CHANGES_TEMPLATE
        
        # Format the prompt with existing changes
        prompt_text = MERGE_RECENT_CHANGES_TEMPLATE.format(
            existing_changes=existing_changes
        )
        
        messages.append(types.PromptMessage(
            role="user",
            content=types.TextContent(
                type="text",
                text=prompt_text
            )
        ))
    elif prompt.name == "audit_architecture_consistency":
        # Get required arguments
        if not arguments:
            raise ValueError("Arguments required for audit_architecture_consistency prompt")
        
        old_file = arguments.get("old_file")
        new_file = arguments.get("new_file")
        current_path = os.path.dirname(os.path.abspath(__file__))
        print(f"[DEBUG] old_file: {old_file}, new_file: {new_file}", file=open(os.path.join(current_path, "prompts.log"), "a"))

        if not old_file or not new_file:
            raise ValueError("Both old_file and new_file arguments are required")
        
        try:
            # Read both files
            with open(old_file, 'r', encoding='utf-8') as f:
                old_code = f.read()
            with open(new_file, 'r', encoding='utf-8') as f:
                new_code = f.read()
            
            # Import the prompt template
            from core.ai_service import AUDIT_ARCHITECTURE_CONSISTENCY_PROMPT
            
            # Format the prompt with both code files
            prompt_text = AUDIT_ARCHITECTURE_CONSISTENCY_PROMPT.format(
                old_code=old_code,
                new_code=new_code
            )
            
            messages.append(types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=prompt_text
                )
            ))
        except Exception as e:
            messages.append(types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Error reading files: {str(e)}"
                )
            ))
    else:
        # For any other prompts (though we only have one now)
        messages.append(types.PromptMessage(
            role="user",
            content=types.TextContent(
                type="text",
                text=f"请提供{prompt.description}"
            )
        ))
    
    print(f"[DEBUG] messages: {messages}", file=open(os.path.join(current_path, "prompts.log"), "a"))
    return types.GetPromptResult(
        description=prompt.description,
        messages=messages
    )


async def main():
    """Run the server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="code-analyzer",
                server_version="0.3.0",
                capabilities={
                    "tools": {},  # Tool support
                    # "prompts": {}  # Prompt support
                }
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())