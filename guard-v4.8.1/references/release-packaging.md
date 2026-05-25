# Guard 发布打包模式

> 本会话 (2026-05-25) Guard v4.7.1 发布实战提炼。Guard 无 README/CHANGELOG 时首次创建发布管线。

## 桌面发布流程（6步）

```
1. TDD基线: 验证 SKILL.md 内容自洽 → RED 全部通过才进 GREEN
2. 创建 README.md + CHANGELOG.md (如缺失)
3. 全文件版本号 grep: grep -rn 'v[0-9]\.[0-9]\.[0-9]' SKILL.md README.md CHANGELOG.md
4. 桌面包: mkdir ~/Desktop/guard-vX.Y.Z && cp SKILL.md README.md CHANGELOG.md references/ → 桌面
5. ZIP: cd ~/Desktop && zip -r guard-vX.Y.Z.zip guard-vX.Y.Z/
6. git: cd ~/Desktop/guard-vX.Y.Z && git init && git add -A && git commit -m "..."
```

## 验证清单

- [ ] 桌面包包含 SKILL.md + README.md + CHANGELOG.md
- [ ] references/ 目录完整（如有）
- [ ] unzip -l 验证 ZIP 文件数与桌面包一致
- [ ] git log --oneline 确认提交存在

## 常见遗漏

| 遗漏 | 检测方式 |
|------|---------|
| references/ 未打包 | `find 桌面包 -type f` 对比源目录 |
| 版本号标题滞后 | `grep -rn 'v[0-9]\.[0-9]\.[0-9]'` 扫描全部 MD |
| ZIP 内容不对 | `unzip -l` 验证文件数 |
| git 未初始化 | `git status` 报 not a git repository |
