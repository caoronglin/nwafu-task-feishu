---
name: nwafu-task-feishu
description: 西北农林科技大学课表导入飞书待办技能。支持校历作息时间（夏令时/冬令时自动切换）、课程表解析、飞书任务创建、分组管理等功能。
version: 1.0.0
author: 薛麟麒
tags: 西北农林科技大学，课表，飞书，待办，任务管理，校历，作息时间
---

## 📚 技能描述

西北农林科技大学（NWSUAF）课表自动导入飞书待办技能。根据校历规定的作息时间（夏令时/冬令时自动切换），将课程表 Excel 中的课程信息批量创建为飞书待办任务，支持按课程/实验分组管理。

## 🎯 功能特性

- ✅ **作息时间自动切换**：根据校历自动应用夏令时（5 月 1 日 -9 月 30 日）或冬令时（10 月 1 日 -4 月 30 日）
- ✅ **课程表解析**：支持从飞书导出的课表 Excel 文件中解析课程信息
- ✅ **飞书任务创建**：批量创建带准确时间的飞书待办任务
- ✅ **分组管理**：自动创建"课程"和"实验"分组，任务按类型归类
- ✅ **班级匹配**：支持多班级课程，精确匹配用户所在班级
- ✅ **北京时间**：所有时间使用北京时间（UTC+8）

## 📋 触发词

nwafu task feishu，西农课表，西北农林科技大学课表，课表导入飞书，飞书待办，创建课程任务，校历作息，夏令时冬令时，课程分组，实验分组，批量创建任务，课表自动化，NWSUAF，nwafu schedule

## 🔧 前置准备

### 1. 飞书应用配置

在飞书开放平台创建应用，获取以下权限：
- 任务读写权限
- 用户信息读取权限

### 2. 环境变量配置

复制 `.env.example` 为 `.env` 并填写配置：

```bash
cp .env.example .env
```

### 3. 依赖安装

```bash
pip install -r requirements.txt
```

## 💻 使用方法

### 基础用法

```bash
python nwafu_task_feishu.py --excel 课表文件.xls --class 生技 2402
```

### 完整参数

```bash
python nwafu_task_feishu.py \
  --excel /path/to/calendar.xls \
  --class "生技 2402" \
  --start-date 2026-03-02 \
  --lab-excel /path/to/lab.xls \
  --action create  # create, delete, sync
```

### 参数说明

| 参数 | 必需 | 说明 |
|------|------|------|
| `--excel` | ✅ | 课表 Excel 文件路径 |
| `--class` | ✅ | 用户班级名称（如"生技 2402"） |
| `--start-date` | ❌ | 开学日期（默认：2026-03-02） |
| `--lab-excel` | ❌ | 实验课表 Excel 文件路径 |
| `--action` | ❌ | 操作类型：create（创建）、delete（删除）、sync（同步） |
| `--delete-all` | ❌ | 删除所有已创建的任务 |

## 📅 作息时间规则

### 夏令时（5 月 1 日 - 9 月 30 日）

| 节次 | 时间 |
|------|------|
| 1-2 节 | 08:00-09:40 |
| 3-4 节 | 10:10-11:50 |
| 5-6 节 | 14:30-16:10 |
| 7-8 节 | 16:30-18:10 |
| 9-10 节 | 19:00-20:35 |
| 11-12 节 | 20:45-22:20 |

### 冬令时（10 月 1 日 - 4 月 30 日）

| 节次 | 时间 |
|------|------|
| 1-2 节 | 08:00-09:40 |
| 3-4 节 | 10:10-11:50 |
| 5-6 节 | 14:00-15:40 |
| 7-8 节 | 16:00-17:40 |
| 9-10 节 | 19:00-20:35 |
| 11-12 节 | 20:45-22:20 |

## 📁 文件结构

```
nwafu-task-feishu/
├── SKILL.md                 # 技能描述
├── README.md                # 使用说明
├── nwafu_task_feishu.py     # 主脚本
├── requirements.txt         # Python 依赖
├── .env.example             # 环境变量模板
├── .gitignore              # Git 忽略文件
└── cache-YYYY-MM-DD/       # 缓存目录（不上传）
```

## 🔐 密钥管理

### 方式一：.env 文件（推荐）

```bash
cp .env.example .env
# 编辑 .env 填写密钥
```

### 方式二：系统环境变量

```bash
export FEISHU_APP_ID=your_app_id
export FEISHU_APP_SECRET=your_app_secret
export FEISHU_USER_OPEN_ID=your_open_id
```

### 方式三：命令行参数

```bash
python nwafu_task_feishu.py --app-id xxx --app-secret xxx --user-id xxx
```

## ⚠️ 注意事项

1. **密钥安全**：不要将 `.env` 文件提交到 Git
2. **班级名称**：必须与课表中的班级名称完全一致（注意空格）
3. **开学日期**：根据实际校历调整开学日期
4. **任务删除**：删除操作不可恢复，请谨慎使用
5. **时区设置**：服务器时区应设置为 Asia/Shanghai（北京时间）

## 🐛 常见问题

### Q: 任务创建后看不到？
A: 检查 `FEISHU_USER_OPEN_ID` 是否正确，必须使用用户的 open_id

### Q: 时间不对？
A: 检查服务器时区是否为 Asia/Shanghai，执行 `date` 查看

### Q: 班级匹配不到？
A: 课表中的班级名称可能有空格差异，用 `--debug` 查看解析结果

### Q: 夏令时/冬令时切换？
A: 脚本自动根据日期判断，5 月 1 日 -9 月 30 日用夏令时，其他用冬令时

## 📝 示例

### 示例 1：创建课程任务

```bash
python nwafu_task_feishu.py \
  --excel 课表导出.xls \
  --class "生技 2402" \
  --action create
```

### 示例 2：创建课程 + 实验任务

```bash
python nwafu_task_feishu.py \
  --excel 课表导出.xls \
  --lab-excel 实验课表.xls \
  --class "生技 2402" \
  --action create
```

### 示例 3：删除所有任务

```bash
python nwafu_task_feishu.py \
  --class "生技 2402" \
  --delete-all
```

## 📄 License

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
