import sys
import os

# 使用 Houdini 提供的 Qt 绑定 - Houdini 20.5 使用 PySide2
try:
    import hou
    from PySide2 import QtCore, QtWidgets, QtGui
    print("PySide2 导入成功（Houdini 20.5 官方绑定）")
except ImportError:
    print("警告: 无法导入 PySide2，尝试使用其他 Qt 绑定")
    try:
        from PySide6 import QtCore, QtWidgets, QtGui
    except ImportError:
        try:
            from PyQt5 import QtCore, QtWidgets, QtGui
        except ImportError:
            raise ImportError("无法找到任何 Qt 绑定（PySide2/PySide6/PyQt5）")

class ChatWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Claude for Houdini")
        self.setGeometry(300, 300, 800, 600)

        self.init_ui()
        self.message_history = []

    def init_ui(self):
        # 主布局
        main_layout = QtWidgets.QVBoxLayout(self)

        # 消息显示区域
        self.message_area = QtWidgets.QTextEdit()
        self.message_area.setReadOnly(True)
        self.message_area.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Consolas', monospace;
                font-size: 11pt;
            }
        """)
        main_layout.addWidget(self.message_area)

        # 输入区域
        input_layout = QtWidgets.QHBoxLayout()

        self.input_field = QtWidgets.QLineEdit()
        self.input_field.setPlaceholderText("输入您的需求...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #3d3d3d;
                color: #ffffff;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 8px;
                font-size: 11pt;
            }
            QLineEdit:focus {
                border-color: #007acc;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)

        self.send_button = QtWidgets.QPushButton("发送")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #003d66;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        main_layout.addLayout(input_layout)

    def add_message(self, sender, content):
        """添加消息到显示区域"""
        timestamp = QtCore.QDateTime.currentDateTime().toString("HH:mm:ss")

        # 构建消息 HTML
        if sender == "user":
            sender_style = "background-color: #007acc; color: white;"
        else:
            sender_style = "background-color: #444444; color: white;"

        message_html = f"""
            <div style="margin: 8px 0;">
                <span style="font-size: 8pt; color: #888888;">{timestamp}</span>
                <div style="display: inline-block; padding: 4px 8px; border-radius: 4px; margin-right: 8px; {sender_style}">
                    {sender}
                </div>
                <div style="display: inline; color: #ffffff;">{content}</div>
            </div>
        """

        self.message_area.append(message_html)

        # 滚动到底部
        cursor = self.message_area.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.message_area.setTextCursor(cursor)

    def send_message(self):
        """发送消息"""
        text = self.input_field.text().strip()
        if not text:
            return

        # 添加用户消息
        self.add_message("用户", text)
        self.input_field.clear()

        # 调用 Claude API 获取回复
        try:
            from claude_houdini.api.claude_api import ClaudeAPI
            api = ClaudeAPI()
            response = api.generate_houdini_code(text)
            self.add_message("Claude", response)
        except Exception as e:
            error_message = f"请求失败: {str(e)}"
            self.add_message("Claude", error_message)
            print(f"Claude API 错误: {str(e)}")

    def display_code_result(self, code, success, result):
        """显示代码执行结果"""
        if success:
            color = "#00ff00"
            status = "成功"
        else:
            color = "#ff4444"
            status = "失败"

        result_html = f"""
            <div style="margin: 8px 0; padding: 8px; background-color: #1a1a1a; border-radius: 4px;">
                <span style="color: {color}; font-weight: bold;">执行{status}:</span><br>
                <pre style="color: #cccccc; margin: 4px 0; font-family: monospace; font-size: 10pt;">
{code}
                </pre>
                <span style="color: #888888;">{result}</span>
            </div>
        """

        self.message_area.append(result_html)
        self.message_area.ensureCursorVisible()

def run():
    """在 Houdini 中运行聊天窗口"""
    try:
        # 确保我们在 Houdini 环境中
        import hou

        # 使用 Houdini 的 Qt 应用程序
        window = ChatWindow()
        window.show()

        return window

    except Exception as e:
        print(f"启动聊天窗口失败: {str(e)}")
        import traceback
        print(f"详细错误: {traceback.format_exc()}")
        return None
