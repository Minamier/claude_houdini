# Claude-Houdini 集成项目

## 插件概述

Claude-Houdini 是一个将 Claude AI 接入 Houdini 的集成项目，提供了以下功能：

1. 在 Houdini 中创建一个聊天界面面板
2. 支持与 Claude 进行自然语言对话
3. 根据用户需求自动生成 Houdini 节点和模型
4. 支持执行各种 Houdini 操作和任务

## 技术架构

### 核心组件
- **Claude API 客户端** - 负责与 Claude API 通信（火山引擎 Coding Plan）
- **Houdini API 封装** - 连接 Claude API 和 Houdini API
- **聊天界面** - PyQt 实现的 Houdini 面板
- **节点生成引擎** - 解析 Claude 响应并生成 Houdini 节点
- **执行引擎** - 执行 Claude 生成的 Houdini 操作

## 项目结构

```
claude_houdini/
├── __init__.py                # 插件入口
├── config.py                  # 配置管理系统
├── config.json                # 配置文件
├── .env                       # 环境变量配置
├── requirements.txt           # 依赖列表
├── setup.py                   # 安装脚本
├── api/
│   ├── claude_api.py         # Claude API 客户端（火山引擎 Coding Plan）
│   └── houdini_api.py        # Houdini API 封装
├── ui/
│   ├── chat_window.py        # 聊天界面主窗口
│   ├── chat_widget.py        # 聊天控件
│   └── styles.py             # 样式定义
├── engine/
│   ├── node_generator.py     # 节点生成引擎
│   ├── response_parser.py    # 响应解析器
│   └── executor.py          # 执行引擎
├── assets/
│   ├── icons/               # 图标资源
│   └── stylesheets/         # 样式表
└── tests/
    ├── test_api.py
    └── test_node_generation.py
```

## 安装方法

### 1. 环境准备
- **Houdini 版本**：Houdini 20.5.654
- **Python 版本**：Houdini 内置 Python 3.11

### 2. 安装步骤
1. 将项目目录复制到 Houdini 的 Python 库目录：
   - 系统插件目录：`C:\ProgramData\PCGM_Apps\APPs\Houdini\Houdini 20.5.654\houdini\python3.11libs\`
   - 用户插件目录：`%USERPROFILE%\Documents\houdini20.5\python3.11libs\`

2. 配置 `houdini.env` 文件：
   ```
   PYTHONPATH = $PYTHONPATH;C:/Users/pb.adcycwgr/houdini20.5/python3.11libs
   ```

3. 安装依赖：
   ```bash
   hython -m pip install python-dotenv requests
   ```

## 当前任务列表

### 待完成任务
1. 初始化 Claude-Houdini 集成项目
2. 实现火山引擎 Coding Plan API 客户端
3. 封装 Houdini API
4. 开发聊天界面
5. 实现节点生成引擎
6. 测试和优化
7. 初始化Claude-Houdini集成项目
8. 实现火山引擎Coding Plan API客户端
9. 封装Houdini API
10. 开发聊天界面
11. 实现节点生成引擎
12. 测试和优化

### 已完成任务
- 项目结构创建
- 配置管理系统
- 基础 API 封装
- 聊天界面实现（PySide2）
- 节点生成引擎
- 代码执行引擎
- README.md 文档
- 安装脚本

## 使用方法

### 1. 启动聊天界面

#### 方法 1：使用 Python 脚本
```python
import sys
sys.path.append('C:/Users/pb.adcycwgr/houdini20.5/python3.11libs')

from claude_houdini import run_claude_chat
window = run_claude_chat()
```

#### 方法 2：直接运行聊天窗口
```python
from claude_houdini.ui.chat_window import run
window = run()
```

#### 方法 3：使用聊天部件
```python
from claude_houdini.ui.chat_widget import ClaudeChatWidget
widget = ClaudeChatWidget()
widget.show()
```

### 2. 发送消息和生成节点
在聊天界面中，您可以发送以下类型的消息：
- 自然语言描述您想要的效果（如："创建一个球体节点"）
- 代码片段
- 任务描述

### 3. 执行代码
1. 在聊天界面中发送消息
2. Claude 会返回代码片段
3. 点击"执行代码"按钮执行返回的代码
4. 点击"生成节点"按钮根据描述生成节点

## 配置文件

### 1. 环境变量配置（.env 文件）
```
CLAUDE_API_KEY=f9ccd12f-0156-4ec0-b5fa-e67b4c1b9ea8
CLAUDE_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
CLAUDE_MODEL=claude-3
```

### 2. 配置文件（config.json）
```json
{
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
    "auto_execute": false,
    "show_preview": true,
    "log_level": "INFO"
  }
}
```

## 当前完成进度

### 已完成的功能
- 基础项目架构搭建
- Claude API 客户端（火山引擎 Coding Plan）实现
- 聊天界面（PySide2 官方绑定）
- Houdini API 封装
- 节点生成引擎
- 代码执行引擎
- 测试框架

### 已实现的节点生成
- 球体节点生成
- 立方体节点生成
- 噪波几何体生成

### 测试结果
- 导入模块：✅
- 实例化 API 对象：✅
- 获取网络面板：✅（警告但成功）
- 创建聊天窗口：✅
- 节点生成引擎：✅

## 后续需要完成的任务

### 1. 功能优化
- 优化聊天界面的响应速度
- 改进代码执行安全性
- 增强节点生成引擎的功能

### 2. 支持更多节点类型
- 支持创建复杂的节点网络
- 支持材质节点生成
- 支持灯光节点生成
- 支持相机节点生成

### 3. 高级功能
- 支持材质和纹理创建
- 支持几何体重建
- 支持动画和动力学
- 支持渲染和输出

### 4. 性能优化
- 优化 API 调用速度
- 改进节点生成算法
- 优化代码执行效率

### 5. 文档完善
- 编写详细的使用手册
- 创建示例项目
- 录制教学视频

## 技术支持

### 常见问题

#### 问题 1：ModuleNotFoundError: No module named 'claude_houdini'
**解决方案**：
1. 确保插件目录在 PYTHONPATH 中
2. 检查 `python3.11libs` 目录是否正确配置

#### 问题 2：ImportError: 'Config' not found
**解决方案**：
1. 确保配置系统使用单例模式
2. 检查 `config.py` 文件

#### 问题 3：AttributeError: 'qt' has no attribute 'QWidget'
**解决方案**：
1. 确保使用 PySide2 绑定
2. 检查 `hou.qt` 模块是否正确导入

## 联系方式

如有问题或建议，请通过以下方式联系：
- 项目作者：Claude Code
- 邮箱：contact@example.com
- 项目版本：0.1.0

## 许可证

本项目遵循 MIT 许可证。
