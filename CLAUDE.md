# Code Analysis MCP Server

## 项目概述
基于MCP（Model Context Protocol）的代码分析服务器，提供代码阅读、搜索、分析等功能。采用模块化设计，易于扩展。

## 更新日志

### 2024-12-23 - Prompts功能规划
- 计划添加MCP Prompts支持，让服务器能够提供预定义的prompt模板
- 设计统一的MCPRegistry架构，同时管理tools和prompts
- 目标：保持向后兼容的同时，添加prompt模板功能

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

## 审计豁免规则支持

### 概述
审计架构一致性功能支持通过外部文件定义豁免规则。用户可以创建和维护 `AUDIT_EXEMPTIONS.md` 文件来自定义审计过程中的豁免条件。

### 使用方法
1. 在项目根目录创建 `AUDIT_EXEMPTIONS.md` 文件
2. 按照文件模板格式定义豁免规则
3. 调用 `audit_architecture_consistency` 工具时会自动读取该文件
4. 也可以通过 `exemption_file` 参数指定其他豁免规则文件

## 待实现功能：MCP Prompts支持

### 背景
MCP协议支持prompts功能，允许服务器提供预定义的prompt模板供客户端使用。这能让用户快速访问常用的代码分析prompt。

### 实施计划

#### 1. 统一的MCPRegistry架构
创建新的注册系统，同时管理tools和prompts：
```python
class MCPRegistry:
    def __init__(self):
        self._tools = {}
        self._tool_handlers = {}
        self._prompts = {}
```

#### 2. Prompt模板设计
计划添加的prompt模板：
- **code_review**: 代码审查prompt
- **explain_code**: 代码解释prompt
- **find_bugs**: 查找潜在问题prompt
- **architecture_review**: 架构评审prompt
- **refactor_suggestions**: 重构建议prompt

#### 3. 服务器更新
需要在server.py中添加：
```python
@server.list_prompts()
async def handle_list_prompts():
    return registry.get_prompts()

@server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict):
    return registry.get_prompt(name)
```

#### 4. 向后兼容策略
- 保持现有ToolRegistry接口不变
- 逐步迁移到新的MCPRegistry
- 确保所有现有功能继续正常工作

### 技术决策
- 选择统一的MCPRegistry而非分离的registries，以提供更好的扩展性
- 使用包装器模式确保向后兼容
- Prompt模板采用参数化设计，支持动态内容

# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.