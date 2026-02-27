"""
Claude-Houdini 集成安装脚本
"""

import os
import sys
import subprocess
from pathlib import Path

class Installer:
    """Claude-Houdini 集成安装器"""

    def __init__(self):
        """初始化安装器"""
        self.plugin_root = Path(__file__).parent
        self.houdini_path = self.find_houdini_path()
        self.python_path = self.find_python_path()

    def find_houdini_path(self) -> Path:
        """查找 Houdini 安装路径"""
        possible_paths = [
            Path(r"C:\Program Files\Side Effects Software\Houdini 20.5.654"),
            Path(r"C:\ProgramData\PCGM_Apps\APPs\Houdini\Houdini 20.5.654"),
            Path(r"C:\Users\pb.adcycwgr\AppData\Local\Houdini"),
        ]

        for path in possible_paths:
            if path.exists() and (path / "bin" / "houdini.exe").exists():
                print(f"找到 Houdini 安装路径: {path}")
                return path

        raise FileNotFoundError("无法找到 Houdini 安装路径")

    def find_python_path(self) -> Path:
        """查找 Houdini 内置 Python 解释器"""
        python_paths = [
            self.houdini_path / "python311" / "python.exe",
        ]

        for path in python_paths:
            if path.exists():
                print(f"找到 Python 解释器: {path}")
                return path

        raise FileNotFoundError("无法找到 Houdini 内置 Python 解释器")

    def install_dependencies(self):
        """安装依赖库"""
        print("=== 正在安装依赖库 ===")

        requirements_file = self.plugin_root / "requirements.txt"
        if not requirements_file.exists():
            raise FileNotFoundError("requirements.txt 文件不存在")

        command = [
            str(self.python_path),
            "-m", "pip", "install",
            "-r", str(requirements_file)
        ]

        print(f"执行命令: {' '.join(command)}")

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            print("✅ 依赖库安装成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 依赖库安装失败: {e}")
            print(f"错误输出: {e.stderr}")
            return False

    def create_config(self):
        """创建配置文件"""
        print("=== 创建配置文件 ===")

        config_file = self.plugin_root / "config.json"
        if config_file.exists():
            print("⚠️  配置文件已存在，跳过创建")
            return

        default_config = {
            "api": {
                "base_url": "https://ark.cn-beijing.volces.com/api/v3",
                "api_key": "your_api_key_here",
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

        with open(config_file, "w", encoding="utf-8") as f:
            import json
            json.dump(default_config, f, indent=4, ensure_ascii=False)

        print("✅ 配置文件创建成功")

    def update_python_path(self):
        """更新 Python 路径"""
        print("=== 更新 Python 路径 ===")

        # 检查 houdini.env 文件
        houdini_env = Path.home() / "Documents" / "houdini20.5" / "houdini.env"
        if not houdini_env.exists():
            print("⚠️  houdini.env 文件不存在，跳过路径设置")
            return

        # 读取现有配置
        with open(houdini_env, "r", encoding="utf-8") as f:
            content = f.read()

        # 检查是否已添加路径
        plugin_path = str(self.plugin_root)
        if plugin_path in content:
            print("✅ 路径已设置，跳过")
            return

        # 添加插件路径
        with open(houdini_env, "a", encoding="utf-8") as f:
            f.write(f"\n# Claude-Houdini 集成路径\n")
            f.write(f"PYTHONPATH = {plugin_path};@\n")

        print("✅ Python 路径更新成功")

    def test_integration(self):
        """测试集成是否成功"""
        print("=== 测试集成是否成功 ===")

        test_command = [
            str(self.python_path),
            "-c",
            "import sys; print('Python 路径:', sys.path); import claude_houdini; print('claude_houdini 模块导入成功'); print('版本:', claude_houdini.__version__)"
        ]

        try:
            result = subprocess.run(test_command, check=True, capture_output=True, text=True)
            print("✅ 集成测试成功")
            print(f"输出: {result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 集成测试失败: {e}")
            print(f"错误信息: {e.stderr}")
            return False

    def run(self):
        """运行完整安装流程"""
        print("=== 开始安装 Claude-Houdini 集成 ===")
        print(f"插件路径: {self.plugin_root}")

        try:
            self.create_config()
            self.update_python_path()
            if self.install_dependencies():
                self.test_integration()
            print("\n🎉 安装完成！")
            return True
        except Exception as e:
            print(f"\n❌ 安装过程中出错: {e}")
            return False

if __name__ == "__main__":
    try:
        installer = Installer()
        success = installer.run()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n安装过程已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n安装过程中出现错误: {e}")
        import traceback
        print(f"\n详细信息:\n{traceback.format_exc()}")
        sys.exit(1)
