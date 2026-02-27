"""
Houdini 内测试脚本 - 需要在 Houdini 中运行
"""

import sys
import os

# 确保项目路径正确 - 处理 Houdini -script 模式下 __file__ 未定义的情况
try:
    project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
except:
    import hou
    project_path = os.path.abspath(os.path.join(os.path.dirname(hou.hipFile.path()), '..', 'python3.11libs', 'claude_houdini'))

if project_path not in sys.path:
    sys.path.append(project_path)

def test_claude_houdini_integration():
    """在 Houdini 中测试完整集成"""
    print("=" * 60)
    print("Claude-Houdini 集成项目 - Houdini 内测试")
    print("=" * 60)

    results = []

    # 测试 1: 导入模块
    print("\n" + "="*30)
    print("测试: 导入 Claude-Houdini 模块")
    print('-'*30)
    try:
        import claude_houdini
        from claude_houdini import __version__
        print(f"成功导入 claude_houdini v{__version__}")

        from claude_houdini.config import config
        print(f"配置加载成功: Houdini 20.5.654")
        results.append(True)
    except Exception as e:
        print(f"模块导入失败: {str(e)}")
        import traceback
        print(f"详细错误: {traceback.format_exc()}")
        results.append(False)

    # 测试 2: API 实例化
    print("\n" + "="*30)
    print("测试: 实例化 API 对象")
    print('-'*30)
    try:
        from claude_houdini.api.claude_api import ClaudeAPI
        api = ClaudeAPI()
        print("ClaudeAPI 实例化成功")
        results.append(True)
    except Exception as e:
        print(f"ClaudeAPI 实例化失败: {str(e)}")
        results.append(False)

    try:
        from claude_houdini.api.houdini_api import HoudiniAPI
        houdini_api = HoudiniAPI()
        print("HoudiniAPI 实例化成功")
        results.append(True)
    except Exception as e:
        print(f"HoudiniAPI 实例化失败: {str(e)}")
        results.append(False)

    # 测试 3: 获取当前网络面板
    print("\n" + "="*30)
    print("测试: 获取当前网络面板")
    print('-'*30)
    try:
        from claude_houdini.api.houdini_api import HoudiniAPI
        houdini_api = HoudiniAPI()
        network = houdini_api.get_current_network_pane()
        if network:
            print(f"成功获取网络面板: {network.path()}")
        else:
            print("警告: 未找到有效的网络面板")
        results.append(True)
    except Exception as e:
        print(f"获取网络面板失败: {str(e)}")
        import traceback
        print(f"详细错误: {traceback.format_exc()}")
        results.append(False)

    # 测试 4: 显示 UI
    print("\n" + "="*30)
    print("测试: 创建聊天窗口")
    print('-'*30)
    try:
        from claude_houdini.ui.chat_window import run
        window = run()
        if window:
            print("聊天窗口创建成功")
            results.append(True)
        else:
            print("聊天窗口创建失败")
            results.append(False)
    except Exception as e:
        print(f"聊天窗口创建失败: {str(e)}")
        import traceback
        print(f"详细错误: {traceback.format_exc()}")
        results.append(False)

    # 测试 5: 节点生成引擎
    print("\n" + "="*30)
    print("测试: 节点生成引擎")
    print('-'*30)
    try:
        from claude_houdini.engine.node_generator import NodeGenerator
        engine = NodeGenerator()
        print("节点生成引擎实例化成功")
        results.append(True)
    except Exception as e:
        print(f"节点生成引擎失败: {str(e)}")
        import traceback
        print(f"详细错误: {traceback.format_exc()}")
        results.append(False)

    # 测试结果总结
    print("\n" + "="*60)
    print("测试结果总结")
    print("="*60)

    passed = sum(1 for r in results if r)
    total = len(results)

    print(f"测试数量: {total}")
    print(f"通过: {passed}")
    print(f"失败: {total - passed}")
    print(f"成功率: {(passed / total) * 100:.1f}%")

    if passed == total:
        print("\n✅ 所有测试通过！Claude-Houdini 集成项目正常")
    else:
        print("\n⚠️  部分测试失败，可能需要进一步优化")

    return passed == total

def create_test_node():
    """测试创建简单节点"""
    print("\n" + "="*30)
    print("测试: 创建测试节点")
    print('-'*30)

    try:
        from claude_houdini.api.houdini_api import HoudiniAPI
        houdini_api = HoudiniAPI()

        network = houdini_api.get_current_network_pane()
        if network:
            node = houdini_api.create_node(network, "geo", "Test_Geo")
            if node:
                print(f"✅ 成功创建节点: {node.path()}")
                return True
            else:
                print("❌ 创建节点失败")
                return False
        else:
            print("⚠️  未找到有效的网络面板，无法创建节点")
            return False

    except Exception as e:
        print(f"❌ 创建节点失败: {str(e)}")
        import traceback
        print(f"详细错误: {traceback.format_exc()}")
        return False

def run_comprehensive_test():
    """运行全面测试"""
    all_passed = test_claude_houdini_integration()

    # 只有在网络面板可用时才创建测试节点
    if all_passed:
        import hou
        try:
            pane_tab = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
            if pane_tab:
                node_created = create_test_node()
                all_passed = all_passed and node_created
        except Exception as e:
            print(f"获取网络面板失败: {str(e)}")

    return all_passed

if __name__ == "__main__":
    print("Claude-Houdini 集成项目 - 测试开始\n")
    success = run_comprehensive_test()
    print("\n测试完成")
    if not success:
        print("\n⚠️  部分测试失败，请检查上述输出")
    else:
        print("\n✅ 所有测试通过！")
