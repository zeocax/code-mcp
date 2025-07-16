"""AI service for code analysis and modification"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, Any, Optional
from config.ai_config import ai_config

# Prompt templates
AUDIT_ARCHITECTURE_CONSISTENCY_PROMPT = """# 角色
你是一位拥有十年经验、极度注重细节的资深软件架构师，对 "原始框架" 和 "目标框架" 均有深入骨髓的理解。你负责执行最严格的代码一致性审计，任何功能、逻辑、命名或配置上的偏差都不能被容忍。

# 背景
我正在进行代码迁移，需要你以专家的视角审计 "新架构代码"。我要求最终的计算结果、行为、变量命名和关键预设值，都必须与 "原架构代码" 绝对一致。

# 核心任务
你的核心任务是**审计并修改 "新架构代码"**，而不是直接运行它。你将逐行审查代码，并根据下方定义的规则，通过**添加注释**和/或**引发异常**的方式，在代码中直接标记出所有不一致之处。
注意：你不需要判断原架构代码是否存在问题，只需要判断新架构代码是否与原架构代码一致。

# 不一致性判断标准

### A类：关键逻辑不一致
* **命名不一致**: 任何变量、函数、参数或类的命名与原代码不符（除非是区分不同框架的命名）。
* **算法流程改变**: 新代码的控制流与原作不符。
* **计算结果明确不等**: 使用的API或操作组合在数学上与原作不等价。
* **核心功能缺失**: 原作的关键功能在目标框架中没有对等实现。
* **预设内容不一致**: 硬编码的字符串、数值、字典键等关键常量与原作不符。

### B类：实现差异的潜在风险
* **API 行为不等价**: API的默认参数或边缘情况下的行为可能不同。
* **张量操作差异**: 功能相似但底层机制不同的张量操作。
* **随机性处理差异**: 可能影响复现性的随机数生成或使用方式。
* **数值精度问题**: 可能引入非预期精度变化的dtype或运算。

### C类：豁免情况（不应当标记为CRITICAL_ERROR）
* **开发者预留的未实现部分**: 如果在 "新架构代码" 中遇到已有的 raise NotImplementedError("xxx")，这代表开发者已主动标记该部分为"暂时放弃"或"待实现"。这**不是**你需要审计的不一致。
* **TODO实例**: 在 "新架构代码" 中，允许将变量名赋值为一个特别的TodoPlaceholder类的实例`TODO`，这代表开发者已主动跳过审计。这**不是**你需要审计的不一致。
* **__开头的函数**: 在 "新架构代码" 中，如果遇到 `__` 开头的**函数**，这代表开发者已主动标记该部分为"私有"或"内部实现"。这个时候根据函数注释和内容来判断调用这个函数的地方的兼容处理是否合理，如果合理则跳过审计，如果不合理则标记为关键不一致。（明显不合理的有过于简化，或者没有实现）
* **[必要的修改]**: 在 "新架构代码" 中，如果遇到 `[必要的修改]` 的注释，这代表开发者已主动标记该部分为"必要的修改"。你需要这个是否是明显不合理的简化或者跳过某个实现，如果是的话应当移除这个标记同样标记为关键不一致。
* **原架构代码中错误的实现**: 如果某些逻辑在原架构代码中是错误的，此时新架构代码中也有对应的实现，此时**不应当**标记为不一致。
* **用户提供的豁免规则**: 除去上述情况，用户可以提供豁免规则，这些规则将作为C类豁免情况的一部分，你不应该将这些规则中的条目标记为不一致。

用户提供的豁免规则：
{exemption_rules}


# 代码处理流程与规则

你必须严格遵循以下流程处理 "新架构代码"：

1.  以 "原架构代码" 为唯一标准，从上到下审查 "新架构代码" 的每一部分。
2.  根据上文 **“不一致性判断标准”** 来判断当前代码块是否存在问题。
3.  根据判断结果，从以下三种操作中选择一种来处理当前代码块：

    * **操作 A：标记关键不一致 (中断执行)**
        * **何时使用**：当代码满足“A类：关键逻辑不一致”中的内容，且不满足“C类：豁免情况”中的任意一条时。
        * **具体步骤**：
            1.  在有问题的代码行上方，添加一行注释，格式为：# CRITICAL_ERROR: [不一致类别] - 不一致的原因描述。
            2.  将原始的有问题的代码行注释，标注为： # 不一致的实现。
            3.  将原架构代码中对应的代码以注释的形式添加到新架构代码中，标注为： # 原架构中的对应代码。
            4.  在被注释掉的代码行下方，添加 raise NotImplementedError("与上方注释一致的不一致原因描述")。

    * **操作 B：标记潜在风险 (仅作提示)**
        * **何时使用**：当代码满足“B类：实现差异的潜在风险”中的任意一条时。
        * **具体步骤**：
            1.  在有问题的代码行上方，添加一行注释，格式为：# RISK_INFO: [风险类别] - 风险描述。
            2.  **保留**原始代码行，不做修改。

    * **操作 C：忽略或放行**
        * **何时使用**：当代码完全符合原架构代码，或满足“C类：豁免情况”时。
        * **具体步骤**：不进行任何修改，保留代码原样。

### **处理示例**

**如果输入的 "新架构代码" 是这样：**

```python
# ... (部分代码)
self.lr = 0.01
output = F.relu(input)
raise NotImplementedError("loss function not implemented yet")
```

**你的输出应该是这样：**

```python
# ... (部分代码)
# CRITICAL_ERROR: [命名不一致] - 变量 'lr' 在原作中为 'learning_rate'。
# 不一致的实现:
# self.lr = 0.01
# 原架构中的对应代码:
# self.learning_rate = s0.01
raise NotImplementedError("变量 'lr' 在原作中为 'learning_rate'。")
raise NotImplementedError("loss function not implemented yet")
```

# 最终输出格式
* 不输出任何额外的分析报告或解释。
* 仅输出经过你**严格按照上述流程和规则修改过**的、完整的"新架构代码"。

# 输入信息

=== 原架构代码 (逻辑参考基准 - "原始框架") ===

```python
{old_code}
```

=== 新架构代码 (需要审计和修改 - "目标框架") ===

```python
{new_code}
```"""

class AIService:
    """Service for AI-powered code operations"""
    
    def __init__(self):
        self.config = ai_config
        self._client = None
    
    def _get_client(self):
        """Get AI client based on provider"""
        if self._client:
            return self._client
            
        provider = self.config.provider
        
        if provider == 'openai':
            try:
                import openai
                import httpx
                
                api_key = self.config.get_api_key('openai')
                if not api_key:
                    raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
                
                # Create client with optional base URL
                client_kwargs = {'api_key': api_key}
                if self.config.openai_base_url:
                    client_kwargs['base_url'] = self.config.openai_base_url
                
                # Configure proxy if available
                proxy_url = self.config.openai_proxy or self.config.https_proxy or self.config.http_proxy
                print(f"Proxy URL: {proxy_url}")
                if proxy_url:
                    # Create httpx client with proxy
                    http_client = httpx.Client(
                        proxy=proxy_url
                    )
                    client_kwargs['http_client'] = http_client
                
                self._client = openai.OpenAI(**client_kwargs)
            except ImportError as e:
                if 'httpx' in str(e):
                    raise ImportError("httpx library not installed. Run: pip install httpx")
                else:
                    raise ImportError("OpenAI library not installed. Run: pip install openai")
        
        elif provider == 'anthropic':
            try:
                import anthropic
                api_key = self.config.get_api_key('anthropic')
                if not api_key:
                    raise ValueError("Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable.")
                self._client = anthropic.Anthropic(api_key=api_key)
            except ImportError:
                raise ImportError("Anthropic library not installed. Run: pip install anthropic")
        
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")
        
        return self._client
    
    async def audit_architecture_consistency(self, old_code: str, new_code: str, exemption_file: str = None) -> str:
        """Use AI to audit new architecture code for consistency with old architecture, marking discrepancies"""
        client = self._get_client()
        provider = self.config.provider
        
        # Read exemption rules if file is provided
        exemption_rules = ""
        if exemption_file:
            try:
                from pathlib import Path
                exemption_path = Path(exemption_file)
                if exemption_path.exists():
                    with open(exemption_path, 'r', encoding='utf-8') as f:
                        exemption_rules = f.read().strip()
            except Exception as e:
                print(f"Warning: Failed to read exemption file: {e}")
        
        # If no exemption rules provided
        if not exemption_rules:
            exemption_rules = "无用户自定义豁免规则"
        
        # Format prompt with all parameters
        prompt = AUDIT_ARCHITECTURE_CONSISTENCY_PROMPT.format(
            old_code=old_code,
            new_code=new_code,
            exemption_rules=exemption_rules
        )
        
        try:
            if provider == 'openai':
                # Build request parameters
                params = {
                    'model': self.config.model,
                    'messages': [
                        {"role": "system", "content": "You are a senior software architect with 10 years of experience. Conduct strict code audits to identify and mark any inconsistencies between architecture implementations."},
                        {"role": "user", "content": prompt}
                    ],
                    'temperature': self.config.temperature if self.config.temperature else None
                }
                
                # Only add max_tokens if it's set
                if self.config.max_tokens is not None:
                    params['max_tokens'] = self.config.max_tokens
                
                response = client.chat.completions.create(**params)
                content = response.choices[0].message.content.strip()
                return self._extract_code_from_response(content)
            
            elif provider == 'anthropic':
                # Build request parameters
                params = {
                    'model': self.config.model,
                    'messages': [
                        {"role": "user", "content": prompt}
                    ],
                    'temperature': self.config.temperature if self.config.temperature else None
                }
                
                # Only add max_tokens if it's set
                if self.config.max_tokens is not None:
                    params['max_tokens'] = self.config.max_tokens
                
                response = client.messages.create(**params)
                content = response.content[0].text.strip()
                return self._extract_code_from_response(content)
            
        except Exception as e:
            raise Exception(f"Architecture audit service error: {str(e)}")
    
    def _extract_code_from_response(self, response: str) -> str:
        """Extract code from response, handling thinking tags"""
        import re
        
        # Remove common thinking patterns
        # Pattern 1: <thinking>...</thinking> or <think>...</think>
        response = re.sub(r'<thinking>.*?</thinking>', '', response, flags=re.DOTALL)
        response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
        
        # Pattern 2: [thinking]...[/thinking] or [think]...[/think]
        response = re.sub(r'\[thinking\].*?\[/thinking\]', '', response, flags=re.DOTALL)
        response = re.sub(r'\[think\].*?\[/think\]', '', response, flags=re.DOTALL)
        
        # Pattern 3: ```thinking...``` blocks
        response = re.sub(r'```thinking.*?```', '', response, flags=re.DOTALL)
        
        # Extract code from markdown code blocks if present
        code_blocks = re.findall(r'```(?:python|py|javascript|js|typescript|ts|java|cpp|c)?\n(.*?)```', response, re.DOTALL)
        if code_blocks:
            # Return the first code block found
            return code_blocks[0].strip()
        
        # If no code blocks, return the cleaned response
        return response.strip()
    
    async def analyze_architecture_diff(self, old_code: str, new_code: str) -> Dict[str, Any]:
        """Analyze differences between architectures"""
        # Simple analysis without AI for now
        old_lines = old_code.splitlines()
        new_lines = new_code.splitlines()
        
        return {
            'old_lines': len(old_lines),
            'new_lines': len(new_lines),
            'size_change': len(new_lines) - len(old_lines),
            'has_old_code': len(old_code) > 0,
            'has_new_code': len(new_code) > 0
        }

# Global service instance
ai_service = AIService()