# 贡献指南

感谢你对 Clothy 感兴趣！欢迎参与贡献。

## 🌟 贡献方式

### 报告问题
- 使用 [GitHub Issues](https://github.com/zironglv/clothy/issues)
- 描述清楚问题复现步骤
- 附上错误日志或截图

### 提交代码
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 改进文档

### 改进文档
- 修正错别字
- 补充使用示例
- 翻译文档

## 📝 代码规范

### Python 代码
- 遵循 PEP 8 规范
- 使用类型注解
- 添加 docstring

```python
def add_item(self, name: str, category: str) -> Dict[str, Any]:
    """
    添加单品到衣橱
    
    Args:
        name: 单品名称
        category: 品类（top/bottom/outer/shoes/accessory）
    
    Returns:
        包含单品信息的字典
    """
    pass
```

### 提交信息
使用约定式提交：

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修复 bug |
| `docs` | 文档更新 |
| `style` | 代码格式（不影响功能）|
| `refactor` | 代码重构 |
| `test` | 测试相关 |
| `chore` | 构建/工具相关 |

示例：
```
feat: 支持从淘宝订单导入商品
fix: 修复成员识别失败的问题
docs: 更新 README 安装说明
```

## 🧪 测试

运行测试：
```bash
python test_v050.py
```

确保所有测试通过后再提交 PR。

## 📋 开发路线

### v0.5.0（当前）
- [x] 多人衣橱管理
- [x] AI 服装识别
- [x] 搭配推荐
- [x] 淘宝导入

### v0.6.0（计划）
- [ ] 穿搭日历
- [ ] 天气自动获取
- [ ] 更多 AI 模型支持

### v1.0.0（未来）
- [ ] 移动端适配
- [ ] 社交分享
- [ ] 穿搭社区

## 💬 讨论

- [GitHub Discussions](https://github.com/zironglv/clothy/discussions) — 功能讨论、问答
- [GitHub Issues](https://github.com/zironglv/clothy/issues) — Bug 报告、功能请求

---

再次感谢你的贡献！🎉