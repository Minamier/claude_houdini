import hou

class HoudiniAPI:
    def __init__(self):
        pass

    def create_node(self, parent, node_type, name=None):
        """在指定位置创建节点"""
        try:
            node = parent.createNode(node_type, name)
            return node
        except Exception as e:
            print(f"创建节点失败: {str(e)}")
            return None

    def connect_nodes(self, from_node, from_output, to_node, to_input):
        """连接节点"""
        try:
            from_node.outputConnectors()[from_output].connectTo(to_node.inputConnectors()[to_input])
            return True
        except Exception as e:
            print(f"连接节点失败: {str(e)}")
            return False

    def set_node_parm(self, node, parm_name, value):
        """设置节点参数"""
        try:
            parm = node.parm(parm_name)
            if parm:
                if isinstance(value, str):
                    parm.setString(value)
                elif isinstance(value, int):
                    parm.set(value)
                elif isinstance(value, float):
                    parm.set(value)
                else:
                    parm.set(value)
                return True
        except Exception as e:
            print(f"设置参数失败: {str(e)}")
        return False

    def get_current_network_pane(self):
        """获取当前网络视图面板"""
        try:
            if hasattr(hou, 'ui') and hasattr(hou, 'paneTabType'):
                pane_tab = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
                if pane_tab:
                    return pane_tab.pwd()
        except Exception as e:
            print(f"获取当前网络面板失败: {str(e)}")
        return None
