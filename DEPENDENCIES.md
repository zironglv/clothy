# 第三方依赖说明

Clothy 使用以下第三方开源库：

## Python 依赖

| 库名 | 版本 | 许可证 | 用途 |
|------|------|--------|------|
| [Pillow](https://python-pillow.org/) | >=10.0.0 | PIL License | 图像处理（缩放、格式转换）|
| [requests](https://docs.python-requests.org/) | >=2.31.0 | Apache 2.0 | HTTP 请求（图片下载）|
| [PyYAML](https://pyyaml.org/) | >=6.0 | MIT | YAML 配置解析 |
| [python-dateutil](https://github.com/dateutil/dateutil) | >=2.8.0 | Apache 2.0 | 日期处理 |

## 可选依赖

如果使用 AI 功能，需要配置阿里云 DashScope API：

| 服务 | 模型 | 用途 |
|------|------|------|
| [通义千问](https://tongyi.aliyun.com/) | qwen-max | 文本理解 |
| [Qwen-VL](https://github.com/QwenLM/Qwen-VL) | qwen-vl-plus | 图像识别 |

**注意**：AI 服务需要单独申请 API Key，遵循阿里云服务协议。

---

## 许可证兼容性

本项目采用 MIT 协议，与上述依赖的许可证兼容：

| 许可证 | 兼容性 |
|--------|--------|
| MIT | ✅ 完全兼容 |
| Apache 2.0 | ✅ 完全兼容 |
| PIL License | ✅ 兼容（需保留声明）|

---

## 致谢

感谢以上开源项目的贡献者！

---

*最后更新: 2026-03-25*