# Clothy - AI 穿搭闺蜜 👗

> OpenClaw 生态首个生活场景 Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

你的专属 AI 穿搭顾问，像闺蜜一样懂你的风格。支持**多人衣橱管理**，全家人的穿搭一个 Skill 搞定！

---

## ✨ 核心特性

### 🏠 多人衣橱管理
一个 Skill 管理全家人的穿搭：
- 支持成人、儿童、老人独立画像
- 智能识别目标成员
- 数据隔离存储

### 📸 智能衣橱管理
- **拍照录入** — 拍下衣服自动识别类型、颜色、风格
- **多模态 AI** — 支持视觉大模型识别，无 API 时本地降级
- **自动分类** — 上衣/下装/外套/鞋子智能归档

### 🌤️ 每日穿搭推荐
- 场景感知推荐（约会、通勤、休闲）
- 天气适配
- 风格匹配

### 🛒 逛街种草咨询
- 实时参谋 — 拍照问要不要买
- 搭配建议 — 和现有衣橱对比
- 购买决策 — 理性消费建议

### 📊 衣橱分析洞察
- 配置分析 — 颜色分布、季节占比、风格偏向
- 购物指南 — 缺什么、多什么
- 理性消费 — 避免重复购买

### 🏪 关注店铺追踪
- 收藏喜欢的淘宝店铺
- 监控新品上架
- 智能推荐

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- SQLite 3
- （可选）阿里云 DashScope API Key — 用于 AI 识别

### 安装

```bash
# 克隆仓库
git clone https://github.com/zironglv/clothy.git
cd clothy

# 安装依赖
pip install -r requirements.txt
```

### 配置

```bash
# 设置 AI API Key（可选，不设置则使用本地分析）
export DASHSCOPE_API_KEY="your-api-key"
```

### 运行

```python
from main import Clothy

# 创建实例
app = Clothy()

# 录入单品
result = app.process("录入一件白色T恤")
print(result['text'])

# 获取推荐
result = app.process("今天穿什么")
print(result['text'])
```

---

## 📖 功能示例

### 多人衣橱

```python
# 添加家庭成员
app.process("添加家庭成员 老公")
app.process("添加家庭成员 小孩")

# 智能识别成员
app.process("给老公录入一件蓝色衬衫")  # 自动录入到老公衣橱
app.process("今天小孩穿什么")          # 自动推荐小孩穿搭
```

### 拍照录入

```python
# 发送图片 + 文字
result = app.process("录入", context={'image': '/path/to/image.jpg'})
```

### 衣橱分析

```python
result = app.process("分析我的衣橱")
# 输出：
# 📊 衣橱分析报告
# 总计 28 件单品
# 🎨 颜色分布：白色 35%、蓝色 25%、黑色 20%...
# 📅 季节覆盖：春夏秋 85%、冬季 15%
# 💡 建议：缺一件黑色基础款打底衫
```

---

## 🏗️ 项目结构

```
stylebuddy/
├── main.py                 # 主入口
├── SKILL.md               # Skill 定义文件
├── requirements.txt       # Python 依赖
├── src/
│   ├── core/
│   │   ├── command_parser.py    # 命令解析
│   │   ├── member_manager.py    # 成员管理
│   │   ├── session_manager.py   # 会话管理
│   │   ├── main_router.py       # 主路由
│   │   └── recommender.py       # 搭配推荐
│   ├── services/
│   │   ├── clothing_recognizer.py  # AI 识别
│   │   ├── message_builder.py      # 消息构建
│   │   ├── image_service.py        # 图片处理
│   │   └── taobao_importer.py      # 淘宝导入
│   ├── models/
│   │   └── profile.py          # 用户画像
│   └── storage/
│       └── database.py         # 数据库
└── tests/
    └── test_v050.py            # 功能测试
```

---

## ⚙️ 配置说明

### 环境变量

| 变量名 | 说明 | 必需 |
|--------|------|------|
| `DASHSCOPE_API_KEY` | 阿里云 DashScope API Key | 否（无则本地分析）|

### AI 模型配置

默认使用阿里云通义千问系列模型：

- **视觉模型**: `qwen-vl-plus` — 图片识别
- **文本模型**: `qwen-max` — 文本理解

可在 `clothing_recognizer.py` 中修改。

---

## 🔒 隐私说明

### 数据存储
- 所有数据存储在本地 SQLite 数据库
- 图片存储在本地 `wardrobe_images/` 目录
- **不会上传用户数据到云端**（除 AI 识别请求）

### AI 识别
- 调用 AI API 时仅发送图片用于识别
- 不保存图片到远程服务器
- 可选择不使用 AI，改用本地分析

### 淘宝关联
- 淘宝导入需要用户提供数据（订单/收藏夹截图或数据）
- 不直接调用淘宝 API
- 不存储淘宝账号信息

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

### 开发环境

```bash
# 克隆并安装开发依赖
git clone https://github.com/zironglv/clothy.git
cd clothy
pip install -r requirements.txt

# 运行测试
python test_v050.py
```

### 提交规范

- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关

---

## 📄 开源协议

本项目基于 **MIT 协议** 开源。

### 你可以：
- ✅ 商业使用
- ✅ 修改代码
- ✅ 分发代码
- ✅ 私人使用

### 你需要：
- 📋 保留版权声明
- 📋 包含 LICENSE 文件

---

## 🙏 致谢

### 依赖项目

- [Pillow](https://python-pillow.org/) — 图像处理
- [requests](https://docs.python-requests.org/) — HTTP 请求
- [PyYAML](https://pyyaml.org/) — YAML 解析

### AI 模型

- [通义千问](https://tongyi.aliyun.com/) — 阿里云大语言模型
- [Qwen-VL](https://github.com/QwenLM/Qwen-VL) — 视觉语言模型

---

## 📮 联系方式

- **Issues**: [GitHub Issues](https://github.com/zironglv/clothy/issues)
- **Discussions**: [GitHub Discussions](https://github.com/zironglv/clothy/discussions)

---

<p align="center">
  Made with ❤️ by OpenClaw Community
</p>