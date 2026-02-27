"""
节点生成测试模块
"""

import sys
import logging
import unittest

sys.path.append("C:/Users/pb.adcycwgr/houdini20.5/python3.11libs")

from claude_houdini.engine.node_generator import NodeGenerator
from claude_houdini.api.houdini_api import HoudiniAPI

logging.basicConfig(level=logging.DEBUG)

class TestNodeGenerator(TestCase):
    """节点生成器测试"""

    def setUp(self):
        """测试前设置"""
        print("\n=== 开始测试节点生成器 ===")
        self.generator = NodeGenerator()
        self.houdini_api = HoudiniAPI()

    def test_node_generator_initialization(self):
        """测试节点生成器初始化"""
        print("\n=== 测试节点生成器初始化 ===")
        self.assertIsInstance(self.generator, NodeGenerator)
        self.assertIsNotNone(self.generator.api)

    def test_node_type_validation(self):
        """测试节点类型验证"""
        print("\n=== 测试节点类型验证 ===")

        valid_types = ["box", "sphere", "xform", "merge"]
        for node_type in valid_types:
            self.assertTrue(self.generator.validate_node_type(node_type))

        invalid_types = ["invalid_node_type", "non_existent_node", "test_node"]
        for node_type in invalid_types:
            self.assertFalse(self.generator.validate_node_type(node_type))

    def test_node_network_validation(self):
        """测试节点网络验证"""
        print("\n=== 测试节点网络验证 ===")

        valid_network = {
            "nodes": [
                {"name": "box1", "type": "box"},
                {"name": "xform1", "type": "xform"}
            ],
            "connections": [
                {"from": "box1", "to": "xform1"}
            ]
        }

        self.assertTrue(self.generator.validate_node_network(valid_network))

        invalid_network = {
            "nodes": [
                {"name": "invalid_node", "type": "invalid_type"}
            ]
        }

        self.assertFalse(self.generator.validate_node_network(invalid_network))

    def test_resource_estimation(self):
        """测试资源估算"""
        print("\n=== 测试资源估算 ===")

        simple_network = {
            "nodes": [{"name": "box1", "type": "box"}],
            "connections": []
        }

        complex_network = {
            "nodes": [{"name": f"node{i}", "type": "box"} for i in range(30)],
            "connections": [{"from": f"node{i}", "to": f"node{i+1}"} for i in range(29)]
        }

        simple_est = self.generator.estimate_resource_usage(simple_network)
        complex_est = self.generator.estimate_resource_usage(complex_network)

        self.assertEqual(simple_est["node_count"], 1)
        self.assertEqual(complex_est["node_count"], 30)
        self.assertLess(simple_est["node_count"], complex_est["node_count"])

    def test_complexity_estimation(self):
        """测试复杂度估算"""
        print("\n=== 测试复杂度估算 ===")

        simple_network = {
            "nodes": [{"name": "node1", "type": "box"}],
            "connections": []
        }

        medium_network = {
            "nodes": [{"name": f"node{i}", "type": "box"} for i in range(10)],
            "connections": []
        }

        complex_network = {
            "nodes": [{"name": f"node{i}", "type": "box"} for i in range(30)],
            "connections": []
        }

        self.assertEqual(self.generator.estimate_complexity(simple_network), "简单")
        self.assertEqual(self.generator.estimate_complexity(medium_network), "中等")
        self.assertEqual(self.generator.estimate_complexity(complex_network), "复杂")

    def test_simple_node_chain(self):
        """测试简单节点链生成"""
        print("\n=== 测试简单节点链生成 ===")

        node_types = ["box", "xform", "merge"]
        nodes = self.generator.generate_simple_chain(node_types, prefix="test_chain")

        self.assertEqual(len(nodes), len(node_types))

    def test_procedural_object_generation(self):
        """测试程序化物体生成"""
        print("\n=== 测试程序化物体生成 ===")

        object_nodes = self.generator.generate_procedural_object("box", 3, 1.5)
        self.assertGreater(len(object_nodes), 0)

    def test_parse_and_generate(self):
        """测试代码解析与生成"""
        print("\n=== 测试代码解析与生成 ===")

        code = """
import hou
network = hou.node("/obj")
box = network.createNode("box")
xform = network.createNode("xform")
box.setParms({"size": 2})
xform.setParms({"tx": 3})
box.setNextInput(xform)
[box, xform]
"""

        nodes = self.generator.parse_and_generate(code)
        self.assertIsInstance(nodes, list)
        self.assertGreater(len(nodes), 0)

    def tearDown(self):
        """测试后清理"""
        print("\n=== 测试完成 ===")

if __name__ == "__main__":
    import unittest

    test_loader = unittest.TestLoader()
    test_names = [
        'test_node_generator_initialization',
        'test_node_type_validation',
        'test_node_network_validation',
        'test_resource_estimation',
        'test_complexity_estimation',
        'test_simple_node_chain',
        'test_procedural_object_generation',
        'test_parse_and_generate'
    ]

    tests = [test_loader.loadTestsFromName(name, module=__name__) for name in test_names]
    test_suite = unittest.TestSuite(tests)

    runner = unittest.TextTestRunner()
    runner.run(test_suite)
