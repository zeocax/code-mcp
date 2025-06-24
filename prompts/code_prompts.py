"""Architecture consistency audit prompt template"""

import mcp.types as types

# Define architecture consistency audit prompt
audit_architecture_consistency_prompt = types.Prompt(
    name="audit_architecture_consistency",
    description="以资深软件架构师的视角对新架构代码进行严格的一致性审计，通过添加注释和异常标记所有与原架构不一致的地方",
    arguments=[
        types.PromptArgument(
            name="old_file",
            description="原架构文件路径（作为审计的参考基准）",
            required=True
        ),
        types.PromptArgument(
            name="new_file",
            description="新架构文件路径（将被审计并标记不一致之处）",
            required=True
        )
    ]
)

# Collect all prompts
ALL_PROMPTS = [
    audit_architecture_consistency_prompt
]