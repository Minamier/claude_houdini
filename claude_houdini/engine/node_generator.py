import ast
import traceback
from ..api.houdini_api import HoudiniAPI

class NodeGenerator:
    def __init__(self):
        self.houdini_api = HoudiniAPI()

    def execute_code(self, code):
        """安全执行生成的 Houdini Python 代码"""
        try:
            # 安全检查：只允许使用 hou 模块和基本操作
            allowed_modules = ["hou"]
            tree = ast.parse(code)

            # 检查导入语句
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        if name.name not in allowed_modules:
                            return False, f"禁止导入模块: {name.name}"
                elif isinstance(node, ast.ImportFrom):
                    if node.module not in allowed_modules:
                        return False, f"禁止导入模块: {node.module}"

            # 执行代码
            exec_globals = {"__builtins__": __builtins__, "hou": __import__("hou")}
            exec(code, exec_globals)

            return True, "代码执行成功"

        except Exception as e:
            error_msg = f"代码执行失败: {str(e)}\n{traceback.format_exc()}"
            return False, error_msg

    def generate_simple_node_network(self, description):
        """根据描述生成简单的节点网络"""
        network = self.houdini_api.get_current_network_pane()
        if network is None:
            return False, "未找到有效的网络面板"

        try:
            # 简单示例：根据描述创建基础几何体节点
            if "球体" in description or "sphere" in description.lower():
                sphere_node = self.houdini_api.create_node(network, "geo", "Sphere")
                if sphere_node:
                    sphere_node.moveToGoodPosition()
                    return True, f"创建球体节点: {sphere_node.path()}"

            elif "立方体" in description or "box" in description.lower():
                box_node = self.houdini_api.create_node(network, "geo", "Box")
                if box_node:
                    box_node.moveToGoodPosition()
                    return True, f"创建立方体节点: {box_node.path()}"

            elif "噪波" in description or "noise" in description.lower():
                geo_node = self.houdini_api.create_node(network, "geo", "NoiseGeo")
                if geo_node:
                    geo_node.moveToGoodPosition()

                    # 在 geo 内部创建节点
                    sphere = geo_node.createNode("sphere")
                    noise = geo_node.createNode("noise")
                    output = geo_node.createNode("output")

                    sphere.setPosition((0, 0))
                    noise.setPosition((1, 0))
                    output.setPosition((2, 0))

                    sphere.outputConnectors()[0].connectTo(noise.inputConnectors()[0])
                    noise.outputConnectors()[0].connectTo(output.inputConnectors()[0])

                    geo_node.layoutChildren()

                    return True, f"创建噪波几何体节点: {geo_node.path()}"

            else:
                return False, f"无法识别的几何类型: {description}"

        except Exception as e:
            return False, f"生成节点网络失败: {str(e)}"
