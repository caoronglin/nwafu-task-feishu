# NWSUAF Task Feishu

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub release](https://img.shields.io/github/v/release/caoronglin/nwafu-task-feishu)](https://github.com/caoronglin/nwafu-task-feishu/releases)

> 西北农林科技大学课表自动导入飞书待办工具  
> 支持夏令时/冬令时自动切换，批量创建带准确时间的课程任务

## ✨ 特性

- 📅 **智能作息** - 自动判断夏令时/冬令时，应用正确作息时间
- 📊 **课表解析** - 支持飞书导出的课表 Excel 格式
- ✅ **批量创建** - 一键创建所有课程/实验任务到飞书待办
- 📁 **分组管理** - 自动创建"课程"和"实验"分组
- 🎯 **班级匹配** - 精确匹配多班级课程
- 🕐 **时区正确** - 所有时间使用北京时间（UTC+8）

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置密钥

```bash
cp .env.example .env
# 编辑 .env 填写飞书应用配置
```

**必需配置：**
```bash
FEISHU_APP_ID=cli_xxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FEISHU_USER_OPEN_ID=ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. 运行

```bash
python nwafu_task_feishu.py --excel 课表导出.xls --class "生技 2402"
```

## 📖 详细用法

### 基础命令

```bash
# 创建课程任务
python nwafu_task_feishu.py --excel calendar.xls --class "生技 2402"

# 创建课程 + 实验任务
python nwafu_task_feishu.py \
  --excel calendar.xls \
  --lab-excel lab.xls \
  --class "生技 2402"

# 删除所有任务
python nwafu_task_feishu.py --class "生技 2402" --delete-all
```

### 参数说明

| 参数 | 必需 | 说明 | 示例 |
|------|------|------|------|
| `--excel` | ✅ | 课表 Excel 文件路径 | `课表导出.xls` |
| `--class` | ✅ | 班级名称 | `"生技 2402"` |
| `--start-date` | ❌ | 开学日期 | `2026-03-02` |
| `--lab-excel` | ❌ | 实验课表路径 | `实验课表.xls` |
| `--action` | ❌ | 操作类型 | `create/delete/sync` |
| `--delete-all` | ❌ | 删除所有任务 | - |
| `--debug` | ❌ | 调试模式 | - |

## 📅 作息时间

### 夏令时（5 月 1 日 - 9 月 30 日）

| 节次 | 时间 |
|------|------|
| 1-2 节 | 08:00-09:40 |
| 3-4 节 | 10:10-11:50 |
| 5-6 节 | 14:30-16:10 |
| 7-8 节 | 16:30-18:10 |
| 9-10 节 | 19:00-20:35 |

### 冬令时（10 月 1 日 - 4 月 30 日）

| 节次 | 时间 |
|------|------|
| 1-2 节 | 08:00-09:40 |
| 3-4 节 | 10:10-11:50 |
| 5-6 节 | 14:00-15:40 |
| 7-8 节 | 16:00-17:40 |
| 9-10 节 | 19:00-20:35 |

**程序会根据日期自动判断使用哪个作息时间表。**

## 📁 文件结构

```
nwafu-task-feishu/
├── nwafu_task_feishu.py    # 主程序
├── requirements.txt         # Python 依赖
├── .env.example            # 环境变量模板
├── .gitignore              # Git 忽略配置
├── LICENSE                 # MIT 许可证
├── README.md               # 本文件
├── CHANGELOG.md            # 更新日志
├── CONTRIBUTING.md         # 贡献指南
└── SKILL.md                # CoPaw 技能描述
```

## 🔐 密钥获取

### 1. 创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 App ID 和 App Secret

### 2. 配置权限

在应用后台添加以下权限：
- 任务读写权限
- 用户信息读取权限

### 3. 获取用户 Open ID

可通过以下方式获取：
- 飞书开放平台 → 用户管理 → 查询用户
- 或调用飞书 API 获取当前用户信息

## ❓ 常见问题

### Q: 任务创建后看不到？
**A:** 检查 `FEISHU_USER_OPEN_ID` 是否正确，必须使用用户的 open_id。

### Q: 时间显示不对？
**A:** 确保服务器时区为 Asia/Shanghai，执行 `date` 查看当前时区。

### Q: 班级匹配不到？
**A:** 课表中的班级名称可能有空格差异，使用 `--debug` 查看解析结果。

### Q: 如何切换夏令时/冬令时？
**A:** 程序自动根据日期判断，无需手动切换。

### Q: 可以删除已创建的任务吗？
**A:** 使用 `--delete-all` 参数删除所有任务（谨慎使用）。

## 🛠️ 开发

### 本地测试

```bash
# 克隆仓库
git clone https://github.com/caoronglin/nwafu-task-feishu.git
cd nwafu-task-feishu

# 安装依赖
pip install -r requirements.txt

# 配置密钥
cp .env.example .env
# 编辑 .env

# 运行测试
python nwafu_task_feishu.py --excel test.xls --class "测试班级" --debug
```

### 运行测试

```bash
# TODO: 添加单元测试
python -m pytest tests/
```

## 📄 License

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 📞 联系

- GitHub Issues: [提交问题](https://github.com/caoronglin/nwafu-task-feishu/issues)
- 作者：薛麟麒
- 学校：西北农林科技大学生命学院

## 🙏 致谢

感谢所有为本项目做出贡献的开发者！

---

**Made with ❤️ for NWSUAF students**
