"""
聊天界面部件
"""

import hou
import logging
from PySide2.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton,
    QSplitter, QGroupBox, QListWidget, QListWidgetItem, QLabel, QScrollArea
)
from PySide2.QtCore import Qt, QSize, QTimer
from PySide2.QtGui import QFont, QTextCursor, QColor, QBrush, QIcon

from ..api.claude_api import get_api_client
from ..engine.node_generator import NodeGenerator
from ..engine.executor import HoudiniExecutor

logger = logging.getLogger(__name__)

class ClaudeChatWidget(QWidget):
    """Claude 聊天界面部件"""

    def __init__(self, parent: QWidget = None):
        """
        初始化聊天部件

        Args:
            parent: 父窗口部件
        """
        super().__init__(parent)

        self.api_client = get_api_client()
        self.node_generator = NodeGenerator()
        self.executor = HoudiniExecutor()

        self.message_history = []
        self.responses = []
        self.node_definitions = []

        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        # 顶部: 标题栏
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("Claude Assistant"))
        title_layout.addStretch()
        layout.addLayout(title_layout)

        # 中间: 分隔视图
        splitter = QSplitter(Qt.Horizontal)

        # 聊天区域
        chat_group = QGroupBox("聊天")
        chat_layout = QVBoxLayout(chat_group)
        chat_layout.setContentsMargins(4, 4, 4, 4)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Consolas", 12))
        self.chat_display.setMinimumHeight(300)
        chat_layout.addWidget(self.chat_display)

        input_layout = QHBoxLayout()
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText("输入您的需求（如：创建一个立方体节点）...")
        self.input_edit.setFont(QFont("Consolas", 12))
        input_layout.addWidget(self.input_edit)

        self.send_button = QPushButton("发送")
        self.send_button.setFixedWidth(80)
        self.send_button.clicked.connect(self.handle_send)
        input_layout.addWidget(self.send_button)

        self.clear_button = QPushButton("清除")
        self.clear_button.setFixedWidth(80)
        self.clear_button.clicked.connect(self.handle_clear)
        input_layout.addWidget(self.clear_button)

        chat_layout.addLayout(input_layout)
        splitter.addWidget(chat_group)
        splitter.setSizes([600, 200])

        # 响应区域
        response_group = QGroupBox("响应")
        response_layout = QVBoxLayout(response_group)
        response_layout.setContentsMargins(4, 4, 4, 4)

        self.response_list = QListWidget()
        self.response_list.itemDoubleClicked.connect(self.handle_response_select)
        response_layout.addWidget(self.response_list)

        # 执行控制
        execution_layout = QHBoxLayout()
        self.execute_button = QPushButton("执行代码")
        self.execute_button.setFixedWidth(120)
        self.execute_button.clicked.connect(self.handle_execute)
        self.execute_button.setEnabled(False)
        execution_layout.addWidget(self.execute_button)

        self.generate_nodes_button = QPushButton("生成节点")
        self.generate_nodes_button.setFixedWidth(120)
        self.generate_nodes_button.clicked.connect(self.handle_generate_nodes)
        self.generate_nodes_button.setEnabled(False)
        execution_layout.addWidget(self.generate_nodes_button)

        execution_layout.addStretch()
        response_layout.addLayout(execution_layout)
        splitter.addWidget(response_group)

        layout.addWidget(splitter)

        # 节点预览区域（可选）
        self.node_preview = QScrollArea()
        self.node_preview.setWidgetResizable(True)
        self.node_preview.setMinimumHeight(150)
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        self.node_preview.setWidget(preview_widget)
        layout.addWidget(self.node_preview)

        # 初始化界面
        self.update_chat_display()

    def handle_send(self):
        """处理发送消息"""
        text = self.input_edit.text().strip()
        if not text:
            return

        # 保存消息
        self.message_history.append({
            "role": "user",
            "content": text,
            "timestamp": hou.time()
        })

        # 清空输入
        self.input_edit.clear()

        # 更新聊天显示
        self.update_chat_display()

        # 发送到 API
        self.send_button.setEnabled(False)
        QTimer.singleShot(0, lambda: self.send_to_api(text))

    def send_to_api(self, text):
        """发送到 API"""
        try:
            # 显示加载状态
            self.show_loading_message()

            # 发送请求
            response = self.api_client.generate_code(text)

            # 处理响应
            self.responses.append(response)

            # 解析节点定义
            node_def = self.api_client.parse_node_definition(text)
            self.node_definitions.append(node_def)

            # 更新响应列表
            self.update_response_list()

            # 更新聊天显示
            self.update_chat_display()

        except Exception as e:
            logger.error(f"API 调用失败: {e}")
            self.show_error_message(f"API 调用失败: {e}")
        finally:
            self.send_button.setEnabled(True)

    def handle_execute(self):
        """执行代码"""
        if not self.responses:
            return

        selected = self.response_list.currentRow()
        if selected < 0:
            selected = 0

        code = self.responses[selected]
        try:
            self.executor.execute_code(code)
            self.show_success_message("代码执行成功")
        except Exception as e:
            logger.error(f"代码执行失败: {e}")
            self.show_error_message(f"代码执行失败: {e}")

    def handle_generate_nodes(self):
        """生成节点"""
        if not self.node_definitions:
            return

        selected = self.response_list.currentRow()
        if selected < 0:
            selected = 0

        node_def = self.node_definitions[selected]
        try:
            self.node_generator.generate_nodes(node_def)
            self.show_success_message("节点生成成功")
        except Exception as e:
            logger.error(f"节点生成失败: {e}")
            self.show_error_message(f"节点生成失败: {e}")

    def handle_response_select(self, item):
        """处理响应选择"""
        self.execute_button.setEnabled(True)
        self.generate_nodes_button.setEnabled(True)

    def handle_clear(self):
        """清空聊天"""
        self.message_history.clear()
        self.responses.clear()
        self.node_definitions.clear()
        self.response_list.clear()
        self.update_chat_display()
        self.execute_button.setEnabled(False)
        self.generate_nodes_button.setEnabled(False)

    def update_chat_display(self):
        """更新聊天显示"""
        self.chat_display.clear()

        for message in self.message_history:
            role = message["role"]
            content = message["content"]
            self.add_message(role, content)

        # 显示最近的响应
        if self.responses:
            self.add_message("assistant", self.responses[-1])

    def add_message(self, role: str, content: str):
        """添加消息到聊天显示"""
        color = "blue" if role == "user" else "red"
        header = "您" if role == "user" else "Claude"

        html = f'<div style="color: {color}; font-weight: bold;">{header}:</div>'
        html += f'<div style="margin-left: 10px; margin-bottom: 10px;">{content}</div>'
        html += '<hr style="border: 1px solid #ccc; margin: 10px 0;">'

        self.chat_display.append(html)
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )

    def update_response_list(self):
        """更新响应列表"""
        self.response_list.clear()
        for i, response in enumerate(self.responses):
            item = QListWidgetItem(f"响应 {i+1}: {response[:80]}...")
            self.response_list.addItem(item)

    def show_loading_message(self):
        """显示加载消息"""
        self.add_message("assistant", "正在思考...")

    def show_error_message(self, message):
        """显示错误消息"""
        self.add_message("assistant", f"错误: {message}")

    def show_success_message(self, message):
        """显示成功消息"""
        self.add_message("assistant", f"成功: {message}")

    def set_api_key(self, api_key: str):
        """设置 API 密钥"""
        self.api_client.set_api_key(api_key)

    def get_conversation_history(self):
        """获取会话历史"""
        return self.message_history
