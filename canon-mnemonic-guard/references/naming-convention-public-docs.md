# 对外命名规范

> 来源：CMG Dashboard 开发（2026-05-30）· ban 规则 `ban_no_cmg_abbreviation`

## 规则

在对外分发的文本中，**禁止使用项目缩写**。必须使用完整名称：

| 语境 | 使用 |
|------|------|
| 英文语境 | Canon-Mnemonic-Guard |
| 中文语境 | 三省引擎 |
| 技术文档内 | Canon-Mnemonic-Guard（可附中文括号） |

## 适用范围

以下文本属于「对外分发」，禁止缩写：
- README.md / CHANGELOG.md
- Dashboard 等可视化界面
- GitHub 发布公告
- 子组件 SKILL.md 的 description 字段
- 任何会被用户以外的人看到的文本

## 例外

内部会话中快速指代可以使用缩写，因为是 AI 与开发者之间的内部沟通。

## 检查方法

发布前扫描所有对外文件：
```bash
grep -rn 'CMG' README.md CHANGELOG.md *.html 2>/dev/null | grep -v 'CMG_'
# 排除变量名 CMG_GUARD / CMG_SKILL 等，其他命中全部替换
```

## 关联

- SKILL.md 坑点 41
- hermes-agent-skill-authoring SKILL.md 坑点 41
- CMG ban 规则 `ban_no_cmg_abbreviation` (rules/ban/)
