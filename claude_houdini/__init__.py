"""
Claude-Houdini 集成插件
将 Claude AI 接入 Houdini 中，提供聊天界面和自动化节点生成功能

Author: Claude Code
Version: 0.1.0
"""

__version__ = "0.1.0"
__author__ = "Claude Code"
__email__ = "contact@example.com"

# 导入核心模块
from . import config
from . import api
from . import ui
from . import engine

# 导出核心功能
__all__ = [
    "config",
    "api",
    "ui",
    "engine",
    "run_claude_chat"
]

def run_claude_chat():
    """
    启动 Claude 聊天界面

    Returns:
        ChatWindow: 聊天窗口实例
    """
    from .ui.chat_window import run
    return run()

def create_claude_panel():
    """
    创建 Claude 面板（Houdini 集成版本）

    Returns:
        QWidget: Claude 聊天面板
    """
    from .ui.chat_window import ChatWindow
    return ChatWindow()

# Houdini 插件初始化函数
def hou_init():
    """
    Houdini 插件初始化函数
    """
    import hou
    import os
    import sys

    # 确保插件目录在 Python 路径中
    plugin_dir = os.path.dirname(os.path.abspath(__file__))
    if plugin_dir not in sys.path:
        sys.path.append(plugin_dir)

    hou.ui.displayMessage("Claude-Houdini 集成已加载")
    return True

# 简化导入
from .api.claude_api import ClaudeAPI
from .engine.node_generator import NodeGenerator
from .engine.executor import HoudiniExecutor
