# CMG Dashboard 快速上手

> Canon-Mnemonic-Guard 可视化管理后台。Phase 1-3 已完成。

## 启动

```bash
# CLI（需要 ~/bin 在 PATH 中）
cmg-dash

# 或完整路径
python3 ~/.hermes/dashboard/server.py --port 8765

# Hermes 对话中
!dashboard
```

浏览器自动打开 `http://localhost:8765`。

## 功能

| Tab | 功能 |
|-----|------|
| 规则库 | 75 条规则可搜索/排序/筛选，关键词悬停展开，删除按钮（hover 出现） |
| 引擎配置 | 17 个 Hook 可视化开关 + 拦截通知模式切换 + 一键保存到 config.yaml |
| 添加规则 | Web 表单创建新规则（写入 rules/<type>/ 目录） |

## 文件

```
~/.hermes/dashboard/
├── server.py     # HTTP 服务器（零依赖，Python 标准库）
├── generate.py   # 静态 HTML 生成器（备用，离线模式）
└── ~/bin/cmg-dash  # CLI 快捷启动脚本
```

## 注意事项

- 配置修改需要重启 Hermes 生效（YAML 配置文件特性）
- 添加/删除规则即时生效，表格自动刷新
- 亮色/暗色切换自动记忆（localStorage）
