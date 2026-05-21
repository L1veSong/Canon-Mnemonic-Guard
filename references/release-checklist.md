# 版本发布检查清单

每次版本号变更后必须逐项执行，不可跳过。

## 全文件版本号同步

```bash
grep -rn "v[0-9]\.[0-9]\.[0-9]" SKILL.md README.md CHANGELOG.md
```

| 文件 | 位置 | 常见遗漏 |
|------|------|---------|
| SKILL.md | frontmatter `version:` | ✅ |
| SKILL.md | 标题 | ⚠️ |
| SKILL.md | 注入格式 `自省引擎 vX.X.X` | ❌ 高频 |
| SKILL.md | 激活消息 | ❌ 高频 |
| SKILL.md | 典则线当前标记 | ❌ 高频 |
| README.md | 标题 | ❌ 最高频 |
| README.md | badge | ⚠️ |
| CHANGELOG.md | 新条目 | ✅ |

**实战案例：** v2.2.9 发布时 README 标题仍写 v2.2.6；注入/激活消息仍写 v2.2.3。

## ZIP 命名

```
Canon-Mnemonic-Guard-vX.X.X.zip  （不含 hermes 前缀）
```

## 更新公告

中文，无隐私。格式：特性标题 + 要点 + 技术栈表 + 安装命令 + GitHub 链接。
