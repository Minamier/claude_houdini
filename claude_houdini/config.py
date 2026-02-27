"""
配置管理模块
"""

import os
import json
from pathlib import Path

# 插件根目录
PLUGIN_ROOT = Path(__file__).parent

# 默认配置
DEFAULT_CONFIG = {
    "api": {
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "api_key": "",
        "model": "doubao-seed-code-preview-latest",
        "timeout": 60,
        "max_tokens": 4096
    },
    "ui": {
        "window_title": "Claude Assistant",
        "window_width": 800,
        "window_height": 600,
        "font_size": 14,
        "theme": "houdini"
    },
    "engine": {
        "auto_execute": False,
        "show_preview": True,
        "log_level": "INFO"
    }
}

class ConfigManager:
    """配置管理器"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        self._config = DEFAULT_CONFIG.copy()
        self._config_path = PLUGIN_ROOT / "config.json"

        # 加载配置文件
        self._load_config()

    def _load_config(self):
        """加载配置文件"""
        if self._config_path.exists():
            try:
                with open(self._config_path, "r", encoding="utf-8") as f:
                    self._config.update(json.load(f))
            except Exception as e:
                print(f"警告: 无法加载配置文件 {self._config_path}: {e}")
        else:
            # 保存默认配置
            self._save_config()

    def _save_config(self):
        """保存配置文件"""
        try:
            with open(self._config_path, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"警告: 无法保存配置文件 {self._config_path}: {e}")

    def get(self, key_path, default=None):
        """
        获取配置值

        Args:
            key_path: 配置路径 (如 "api.api_key")
            default: 默认值

        Returns:
            配置值
        """
        keys = key_path.split(".")
        value = self._config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def set(self, key_path, value):
        """
        设置配置值

        Args:
            key_path: 配置路径 (如 "api.api_key")
            value: 新值
        """
        keys = key_path.split(".")
        config_dict = self._config

        for i, key in enumerate(keys[:-1]):
            if key not in config_dict or not isinstance(config_dict[key], dict):
                config_dict[key] = {}
            config_dict = config_dict[key]

        config_dict[keys[-1]] = value
        self._save_config()

    def get_api_config(self):
        """获取 API 配置"""
        return self.get("api", {})

    def get_ui_config(self):
        """获取 UI 配置"""
        return self.get("ui", {})

    def get_engine_config(self):
        """获取引擎配置"""
        return self.get("engine", {})

# 单例实例
config = ConfigManager()

# 快速访问 API 配置
def get_api_config():
    """获取 API 配置"""
    return config.get_api_config()

def get_ui_config():
    """获取 UI 配置"""
    return config.get_ui_config()

def get_engine_config():
    """获取引擎配置"""
    return config.get_engine_config()

# 环境变量支持
def load_env_vars():
    """从环境变量加载配置"""
    api_key = os.getenv("CLAUDE_API_KEY")
    if api_key:
        config.set("api.api_key", api_key)

    model = os.getenv("CLAUDE_MODEL")
    if model:
        config.set("api.model", model)

# 初始化时加载环境变量
load_env_vars()
