# 贡献指南

感谢你对本项目的关注！欢迎通过以下方式贡献：

## 🤝 如何贡献

### 1. 报告问题
发现 Bug 或有功能建议？请创建 [Issue](https://github.com/caoronglin/nwafu-task-feishu/issues)

**报告 Bug 时请提供：**
- 问题描述
- 复现步骤
- 预期行为
- 实际行为
- 环境信息（Python 版本、操作系统等）

### 2. 提交代码
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交变更 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 3. 改进文档
文档同样重要！如果你发现文档有误或不完整，欢迎提交 PR 改进。

## 📋 开发规范

### 代码风格
- 遵循 PEP 8 规范
- 使用 4 个空格缩进
- 函数和类添加文档字符串
- 变量和函数名使用小写 + 下划线

### 提交信息格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

**type 类型：**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具链相关

**示例：**
```
feat(schedule): 添加夏令时支持

- 实现夏令时/冬令时自动判断
- 更新作息时间配置

Closes #123
```

## 🧪 测试

提交代码前请确保：
- [ ] 代码可以正常运行
- [ ] 已测试主要功能
- [ ] 无敏感信息泄露

## 📝 发布流程

1. 更新 `CHANGELOG.md`
2. 更新版本号（`SKILL.md` 和代码中的版本）
3. 创建 Git tag
4. 推送到 GitHub
5. 创建 GitHub Release

## 💬 讨论

有任何问题或想法，欢迎在 [Discussions](https://github.com/caoronglin/nwafu-task-feishu/discussions) 中交流！

## 📄 License

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。
