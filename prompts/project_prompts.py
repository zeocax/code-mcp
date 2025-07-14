"""Project management prompts"""

import mcp.types as types


# Merge recent changes prompt
MERGE_RECENT_CHANGES_PROMPT = types.Prompt(
    name="merge_recent_changes",
    description="智能合并最近的更改记录，将现有记录与新更改合并，保留最重要的记录并归档旧记录",
    arguments=[
        types.PromptArgument(
            name="existing_changes",
            description="现有的最近更改记录（JSON格式）",
            required=True
        )
    ]
)


# Project prompts list
PROJECT_PROMPTS = [
    MERGE_RECENT_CHANGES_PROMPT
]


# Prompt template for merge_recent_changes
MERGE_RECENT_CHANGES_TEMPLATE = """你是一个智能的项目更改记录管理助手。你需要合并最近的更改记录。

现有的最近更改记录（A）：
{existing_changes}

基于你对项目的了解，你知道的新更改（B）应该从当前会话的上下文中获取。

请执行以下任务：

1. 分析现有的更改记录（A）和你知道的新更改（B）
2. 合并A和B，生成真正的最近更改（C）：
   - 保留最重要和最近的5-10条记录
   - 确保记录清晰、简洁、有意义
   - 避免重复或过于相似的记录
   
3. 将其余的旧记录归档到archived（D）：
   - 将不再属于"最近"的记录移到归档
   - 保持归档记录的时间顺序

4. 调用update_recent_changes工具，传入：
   - current: 合并后的最近更改列表（C）
   - archived: 更新后的归档列表（D）

注意事项：
- 保持更改记录的描述性和具体性
- 优先保留对项目有重大影响的更改
- 合理判断哪些更改应该归档
- 确保调用工具时使用正确的参数格式"""