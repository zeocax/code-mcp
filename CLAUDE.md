# Code Analysis MCP Server

## 项目概述
基于MCP（Model Context Protocol）的代码分析服务器，提供代码阅读、搜索、分析等功能。采用模块化设计，易于扩展。

## 架构设计

### 核心原则
1. **模块化**：功能解耦，每个模块负责单一职责
2. **可扩展**：易于添加新的分析器和工具
3. **简洁性**：保持代码简单直观
4. **性能优先**：使用异步处理，支持大文件

### 分层架构

```
┌─────────────────────────────────────┐
│         MCP Client (IDE)            │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│      MCP Protocol Layer             │
│         (server.py)                 │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│        Tool Registry                │
│    (register & dispatch)            │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│          Tool Handlers              │
│  ┌─────────┐ ┌─────────┐ ┌────────┐│
│  │FileTools│ │CodeTools│ │Analysis││
│  └─────────┘ └─────────┘ └────────┘│
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│         Core Services               │
│  ┌─────────┐ ┌─────────┐ ┌────────┐│
│  │FileSystem│ │Parser   │ │Cache   ││
│  └─────────┘ └─────────┘ └────────┘│
└─────────────────────────────────────┘
```

### 项目结构

```
code-mcp/
├── server.py              # MCP服务器入口
├── tools/                 # 工具定义
│   ├── __init__.py
│   ├── file_tools.py      # 文件操作工具
│   ├── code_tools.py      # 代码搜索/分析工具
│   └── registry.py        # 工具注册器
├── handlers/              # 工具处理器
│   ├── __init__.py
│   ├── file_handler.py    # 文件读写处理
│   ├── search_handler.py  # 搜索处理
│   └── analyze_handler.py # 分析处理
├── core/                  # 核心服务
│   ├── __init__.py
│   ├── file_system.py     # 文件系统操作
│   ├── code_parser.py     # 代码解析器
│   └── cache.py           # 缓存管理
├── utils/                 # 工具函数
│   ├── __init__.py
│   └── patterns.py        # 常用模式
├── requirements.txt
└── README.md
```

### 功能模块

#### 1. 文件操作 (file_tools)
- `read_file`: 读取文件内容
- `list_files`: 列出目录文件
- `file_info`: 获取文件信息

#### 2. 代码搜索 (code_tools)
- `search_code`: 搜索代码模式
- `find_definition`: 查找定义
- `find_references`: 查找引用

#### 3. 代码分析 (analysis_tools)
- `analyze_structure`: 分析代码结构
- `get_symbols`: 提取符号信息
- `calculate_metrics`: 计算代码指标

### 技术栈
- Python 3.8+
- MCP SDK
- 核心库：
  - `pathlib`: 文件路径处理
  - `ast`: Python代码解析
  - `re`: 正则表达式
  - `asyncio`: 异步处理

## 实现策略

### 第一阶段：基础框架
1. 创建项目结构
2. 实现工具注册机制
3. 基础文件操作工具

### 第二阶段：核心功能
1. 代码搜索功能
2. 简单的代码分析
3. 错误处理和日志

### 第三阶段：高级功能
1. 代码结构分析
2. 多语言支持
3. 性能优化和缓存

## 扩展性设计

### 添加新工具
1. 在 `tools/` 目录创建新的工具定义
2. 在 `handlers/` 实现处理逻辑
3. 注册到工具注册器

### 支持新语言
1. 在 `core/code_parser.py` 添加语言解析器
2. 更新文件类型映射
3. 实现特定语言的分析逻辑

## 使用示例

### 配置MCP客户端
```json
{
  "mcpServers": {
    "code-analyzer": {
      "command": "python",
      "args": ["/path/to/code-mcp/server.py"]
    }
  }
}
```

### 工具调用示例
```python
# 读取文件
await client.call_tool("read_file", {"path": "src/main.py"})

# 搜索代码
await client.call_tool("search_code", {
    "pattern": "def.*analyze",
    "directory": "./src"
})

# 分析结构
await client.call_tool("analyze_structure", {"path": "src/main.py"})
```

## 性能考虑
- 使用异步IO处理文件操作
- 实现简单的LRU缓存
- 对大文件进行流式处理
- 限制搜索结果数量

## 安全考虑
- 限制文件访问路径
- 验证输入参数
- 防止路径遍历攻击
- 限制资源使用
# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.