# CMG 四名冲突检测 — 设计文档

> v5.5.5 新增。两个触发点覆盖先后安装顺序，三种解决方式给用户选择。

## 保护范围

CMG 四包的核心名：

```
canon                   ← 典则线
guard                   ← 护栏线
mnemonic                ← 忆存线
canon-mnemonic-guard    ← 外观层（统一入口）
```

四个名字均不可改——三线命名是 CMG 的品牌契约，改了等于拆散三省架构。

## 检测范围

扫描 `~/.hermes/skills/` + `~/.agents/skills/` 下所有 `SKILL.md`，解析 `name:` 字段，与 CMG 四名逐一比对。同名且不同来源 = 冲突。

## 双触发点

| 触发时机 | 触发点 | 覆盖场景 |
|----------|--------|---------|
| CMG 安装时 | `init.py` Phase 0.5 | gstack 等先装，CMG 后装 → 安装阶段发现 + 交互修复 |
| CMG 每次加载 / `!diagnose` | Phase 6 诊断 | CMG 先装，第三方后装 → 启动/诊断发现 + 警告 |

无论谁先谁后，总有一个环节能抓到。

## 三选一解决

```
A) 将第三方改名为 <source>-<name>     ← 推荐
   不影响功能，只改 frontmatter name:
B) 将 CMG 的改名为 cmg-<name>        ← 需同步四包 related_skills
C) 两者都改
D) 跳过 ← 后续手动处理
```

**CMG 不替用户做决定，但给一键方案。** 不改第三方文件内容（指令、引用全在正文里，name: 只是标识符），改了也不影响 skill 功能。

## 实现

- `scripts/check-name-conflicts.py` — 独立工具，支持 `--fix` 交互模式 + `--quiet` 静默模式
- `init.py` — 调用 `check-name-conflicts.py --quiet`，冲突则 `--fix`
- `SKILL.md` — Phase 6 诊断步骤已集成
