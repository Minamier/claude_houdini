import sys
import os

# 确保项目目录在 Python 路径中
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
parent_path = os.path.abspath(os.path.join(project_path, '..'))
print(f"项目路径: {project_path}")
if parent_path not in sys.path:
    sys.path.insert(0, parent_path)
print(f"Python 路径: {sys.path}")

def test_config():
    """测试配置文件"""
    from claude_houdini.config import Config

    try:
        config = Config()
        print("配置对象创建成功")
        print(f"Houdini 版本: {config.houdini_version}")
        print(f"API Key: {config.coding_plan_key}")
        print("配置测试成功")
        return True
    except Exception as e:
        print(f"配置测试失败: {str(e)}")
        return False

def test_claude_api_import():
    """测试 Claude API 模块导入"""
    try:
        from claude_houdini.api.claude_api import ClaudeAPI
        print("Claude API 模块导入成功")
        return True
    except Exception as e:
        print(f"Claude API 模块导入失败: {str(e)}")
        return False

def test_houdini_api_import():
    """测试 Houdini API 模块导入"""
    try:
        from claude_houdini.api.houdini_api import HoudiniAPI
        print("Houdini API 模块导入成功")
        return True
    except Exception as e:
        print(f"Houdini API 模块导入失败: {str(e)}")
        return False

def test_ui_import():
    """测试 UI 模块导入"""
    try:
        from claude_houdini.ui.chat_window import ChatWindow
        print("UI 模块导入成功")
        return True
    except Exception as e:
        print(f"UI 模块导入失败: {str(e)}")
        return False

def test_engine_import():
    """测试引擎模块导入"""
    try:
        from claude_houdini.engine.node_generator import NodeGenerator
        print("引擎模块导入成功")
        return True
    except Exception as e:
        print(f"引擎模块导入失败: {str(e)}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Claude-Houdini 集成项目 - 基础测试")
    print("=" * 60)

    # 基础测试，不包含依赖 Qt 的 UI 测试
    tests = [
        test_config,
        test_claude_api_import,
        test_houdini_api_import,
        test_engine_import
    ]

    # 检查是否可以安全导入 UI 组件（仅在 Houdini 环境中尝试）
    try:
        import hou
        tests.append(test_ui_import)
    except ImportError:
        print("警告: Houdini 环境未检测到，跳过 UI 组件测试")

    results = []
    for test_func in tests:
        print(f"\n{'='*30}")
        print(f"测试: {test_func.__doc__}")
        print('-'*30)
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"测试执行失败: {str(e)}")
            results.append(False)

    print("\n" + "=" * 60)
    print("测试结果总结")
    print("=" * 60)

    passed = sum(1 for r in results if r)
    total = len(results)

    print(f"通过: {passed}")
    print(f"失败: {total - passed}")
    print(f"成功率: {(passed / total) * 100:.1f}%")

    if passed == total:
        print("\n所有基础测试通过！项目基础架构正常")
    else:
        print("\n部分测试失败，请检查相关模块")

    return passed == total

if __name__ == "__main__":
    run_all_tests()
