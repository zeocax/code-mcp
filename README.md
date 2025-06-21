# Code Analysis MCP Server

A modular MCP (Model Context Protocol) server for code analysis with file operations, code search, and structure analysis capabilities.

## Features

### 📁 File Operations
- **read_file**: Read contents of any code file
- **list_files**: List files in directories with pattern matching
- **file_info**: Get detailed file information (size, type, line count)

### 🔍 Code Search
- **search_code**: Search for patterns in code using regex
- **find_definition**: Find symbol definitions (functions, classes, variables)

### 📊 Code Analysis
- **analyze_structure**: Analyze code structure (imports, classes, functions)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/code-mcp.git
cd code-mcp

# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate  # On Unix/macOS
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

### 1. With Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "code-analyzer": {
      "command": "python",
      "args": ["/absolute/path/to/code-mcp/server.py"]
    }
  }
}
```

Then restart Claude Desktop.

### 2. With Continue.dev (VS Code)

Add to your Continue configuration:

```json
{
  "models": [...],
  "mcpServers": {
    "code-analyzer": {
      "command": "python",
      "args": ["/absolute/path/to/code-mcp/server.py"]
    }
  }
}
```

### 3. With Other MCP Clients

Any MCP-compatible client can use this server by pointing to the `server.py` file.

## Available Tools

### 📖 read_file
Read the contents of a file.

```json
{
  "tool": "read_file",
  "arguments": {
    "path": "src/main.py",
    "encoding": "utf-8"  // optional, default: utf-8
  }
}
```

### 📂 list_files
List files in a directory with optional pattern matching.

```json
{
  "tool": "list_files",
  "arguments": {
    "directory": "./src",      // optional, default: current dir
    "pattern": "*.py",         // optional, default: *
    "recursive": true          // optional, default: false
  }
}
```

### ℹ️ file_info
Get detailed information about a file.

```json
{
  "tool": "file_info",
  "arguments": {
    "path": "src/main.py"
  }
}
```

### 🔍 search_code
Search for patterns in code files using regex.

```json
{
  "tool": "search_code",
  "arguments": {
    "pattern": "def.*test",        // regex pattern
    "directory": "./src",          // optional
    "file_pattern": "*.py",        // optional
    "case_sensitive": false        // optional, default: true
  }
}
```

### 🎯 find_definition
Find where a symbol is defined.

```json
{
  "tool": "find_definition",
  "arguments": {
    "symbol": "MyClass",
    "directory": "./src",          // optional
    "language": "python"           // optional: python, javascript
  }
}
```

### 🏗️ analyze_structure
Analyze the structure of a code file.

```json
{
  "tool": "analyze_structure",
  "arguments": {
    "path": "src/main.py",
    "include_docstrings": true     // optional, default: false
  }
}
```

### 🤖 update_with_architecture
Compare old and new architecture versions and intelligently update the new file.

```json
{
  "tool": "update_with_architecture",
  "arguments": {
    "old_file": "src/legacy/module.py",    // Reference file (old architecture)
    "new_file": "src/modern/module.py",    // Target file (will be updated)
    "backup": true                         // optional, default: true
  }
}
```

## AI Configuration

To use the AI-powered tools, you need to configure your API keys:

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```env
   AI_PROVIDER=openai
   OPENAI_API_KEY=your-openai-api-key
   # or
   AI_PROVIDER=anthropic  
   ANTHROPIC_API_KEY=your-anthropic-api-key
   ```

### Thinking Models Support

The tool automatically handles "thinking" models (like o1, o1-preview) that include reasoning in their responses:
- Thinking sections are automatically removed
- Only the actual code is extracted
- Supports various thinking formats: `<think>`, `[thinking]`, etc.

3. Install AI dependencies:
   ```bash
   pip install openai anthropic
   ```

4. Test LLM connectivity:
   ```bash
   ./test_llm.sh
   # or
   python tests/test_llm.py
   ```

## Examples

### In Claude Desktop

After configuring, you can ask Claude:

- "Read the file src/main.py"
- "Search for all functions that contain 'test' in the src directory"
- "Find where the class 'UserModel' is defined"
- "Analyze the structure of app.py"
- "List all Python files in the project"

### Programmatic Usage

```python
# Example of calling tools programmatically
import asyncio
from mcp import Client

async def main():
    client = Client()
    
    # Read a file
    result = await client.call_tool("read_file", {
        "path": "src/main.py"
    })
    
    # Search for patterns
    result = await client.call_tool("search_code", {
        "pattern": "TODO|FIXME",
        "directory": "./",
        "recursive": True
    })
    
    # Analyze structure
    result = await client.call_tool("analyze_structure", {
        "path": "src/main.py",
        "include_docstrings": True
    })

asyncio.run(main())
```

## Architecture

The server follows a modular architecture:

```
├── server.py          # Main MCP server
├── tools/             # Tool definitions
│   ├── file_tools.py  # File operations
│   └── code_tools.py  # Code analysis tools
├── handlers/          # Request handlers
│   ├── file_handler.py
│   ├── search_handler.py
│   └── analyze_handler.py
└── core/              # Core services
    ├── file_system.py # File system operations
    └── code_parser.py # Code parsing logic
```

## Supported Languages

- Python (.py)
- JavaScript/TypeScript (.js, .ts, .jsx, .tsx)
- Java (.java)
- C/C++ (.c, .cpp, .h)
- Go (.go)
- Rust (.rs)
- Ruby (.rb)
- And more...

## Security

- File access is restricted to prevent directory traversal
- Large files are handled efficiently with streaming
- Search results are limited to prevent memory issues

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT