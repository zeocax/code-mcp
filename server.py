#!/usr/bin/env python3
"""MCP server for code analysis with modular architecture"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Import tool registry and tools
from tools.registry import registry
from tools.file_tools import register_file_tools
from tools.code_tools import register_code_tools
from tools.ai_tools import register_ai_tools


# Initialize server
server = Server("code-analyzer")

# Register all tools
#print("[DEBUG] Registering tools...")
# register_file_tools()
#print(f"[DEBUG] File tools registered: {len([t for t in registry.get_tools() if 'file' in t.name])}")
# register_code_tools()
# print(f"[DEBUG] Code tools registered: {len([t for t in registry.get_tools() if 'code' in t.name or 'find' in t.name or 'analyze' in t.name])}")
register_ai_tools()
print(f"[DEBUG] AI tools registered: {len([t for t in registry.get_tools() if 'architecture' in t.name])}")
print(f"[DEBUG] Total tools registered: {len(registry.get_tools())}")


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
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls through registry"""
    
    if not registry.has_tool(name):
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
    
    handler = registry.get_handler(name)
    if not handler:
        return [types.TextContent(type="text", text=f"No handler found for tool: {name}")]
    
    try:
        # Call the appropriate handler
        return await handler(arguments or {})
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error executing tool {name}: {str(e)}")]


async def main():
    """Run the server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="code-analyzer",
                server_version="0.2.0",
                capabilities={
                    "tools": {}  # Explicitly declare tool support
                }
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())