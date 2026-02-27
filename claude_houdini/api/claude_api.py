import requests
import json
import time
from ..config import config

class ClaudeAPI:
    def __init__(self):
        self.config = config
        self.session = requests.Session()
        self.session.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.get('api.api_key', '')}"
        }

    def send_message(self, prompt, messages=None, temperature=0.7):
        """发送消息到 Claude API"""
        try:
            url = f"{self.config.get('api.base_url', 'https://ark.cn-beijing.volces.com/api/v3')}/api/coding-plan/v1/chat/completions"

            if messages is None:
                messages = []

            messages.append({
                "role": "user",
                "content": prompt
            })

            data = {
                "model": "claude-3",
                "messages": messages,
                "temperature": temperature,
                "max_tokens": 2048
            }

            response = self.session.post(url, json=data, timeout=30)
            response.raise_for_status()

            result = response.json()

            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return "未收到有效响应"

        except Exception as e:
            return f"请求失败: {str(e)}"

    def generate_houdini_code(self, description):
        """根据描述生成 Houdini Python 代码"""
        prompt = f"""
作为 Houdini Python 专家，帮我编写实现以下需求的代码：

{description}

要求：
1. 使用 Houdini Python API (hou module)
2. 代码必须是可直接执行的
3. 避免使用外部依赖（除了 Houdini 内置模块）
4. 包含适当的错误处理
5. 使用中文注释
        """

        return self.send_message(prompt)
