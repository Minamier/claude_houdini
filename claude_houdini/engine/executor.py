"""
Houdini 代码执行引擎
负责执行 Claude 生成的 Houdini Python 代码
"""

import sys
import traceback
import hou


class HoudiniExecutor:
    """Houdini 代码执行器"""

    @staticmethod
    def execute_code(code: str) -> dict:
        """
        执行 Houdini Python 代码

        Args:
            code: 要执行的代码字符串

        Returns:
            dict: 执行结果，包含 success、output 和 error 字段
        """
        try:
            # 准备执行环境
            local_vars = {
                "hou": hou,
                "sys": sys
            }

            # 执行代码
            exec(code, globals(), local_vars)

            return {
                "success": True,
                "output": "代码执行成功",
                "error": None
            }

        except Exception as e:
            return {
                "success": False,
                "output": None,
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    @staticmethod
    def evaluate_expression(expression: str):
        """
        计算表达式

        Args:
            expression: 要计算的表达式

        Returns:
            表达式计算结果
        """
        try:
            return eval(expression, globals(), {
                "hou": hou,
                "sys": sys
            })
        except Exception as e:
            print(f"表达式计算失败: {str(e)}")
            return None

    @staticmethod
    def run_tool(tool_name: str, parameters: dict = None):
        """
        运行 Houdini 工具

        Args:
            tool_name: 工具名称
            parameters: 工具参数

        Returns:
            工具运行结果
        """
        try:
            if parameters is None:
                parameters = {}

            # 查找工具
            tool = hou.findTool(tool_name)
            if tool:
                # 运行工具
                result = tool(parameters)
                return {
                    "success": True,
                    "result": result
                }
            else:
                return {
                    "success": False,
                    "error": f"未找到工具: {tool_name}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def execute_node_network(network_path: str):
        """
        执行节点网络

        Args:
            network_path: 节点网络路径

        Returns:
            执行结果
        """
        try:
            # 获取节点网络
            network = hou.node(network_path)
            if network:
                # 执行所有节点
                for node in network.allSubChildren():
                    if hasattr(node, "execute"):
                        node.execute()

                return {
                    "success": True,
                    "output": f"节点网络 {network_path} 执行成功"
                }
            else:
                return {
                    "success": False,
                    "error": f"未找到节点网络: {network_path}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
