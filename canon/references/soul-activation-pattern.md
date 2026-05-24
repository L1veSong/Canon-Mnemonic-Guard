# SOUL 一行激活模式

> 通用方案：让 Skill 安装后在每次对话中自动生效，不改 Hermes 架构、不侵入用户文件、不依赖 cron。

## 问题

Hermes 技能系统靠任务匹配加载，没有「always-load」机制。用户安装 Skill 后，Skill 不会在每次对话中自动出现。对于需要持续守护的 Skill（如 CMG 护栏），这等于没装。

## 方案

在 SOUL.md 末尾追加一行纯文本标记。Hermes 每次对话读取 SOUL.md 时看到这行 → Agent 自动加载对应 Skill。

```
[SkillName vX.Y.Z] 加载 skill-name 功能描述
```

## 为什么是 SOUL.md

| 通道 | 注入方式 | 跨设备 | 不侵入 | 可撤销 |
|------|---------|--------|--------|--------|
| SOUL.md | 一行追加 | ✅ (Obsidian/Git同步) | ✅ | ✅ (删掉即停) |
| Memory | write | ❌ (本地SQLite) | ❌ (2200字符限制) | ⚠️ |
| Cron | job | ❌ (换设备失效) | ✅ | ⚠️ |
| CLI -s | 启动参数 | ❌ (手动) | ✅ | ✅ |

## 实现

### 1. init 时询问

```
是否在 SOUL.md 中写入激活标记（一行），让 XX 在每次对话自动生效？

  [Y] 是 — 写入一行: [SkillName vX.Y.Z] 加载 skill-name 说明
  [N] 否 — 跳过，用 /skill 手动触发
```

### 2. 写入一行

在 SOUL.md 末尾追加，不修改已有内容：

```python
marker = "[SkillName v1.0.0] 加载 skill-name 功能描述\n"
with open(SOUL_PATH, "a") as f:
    f.write("\n" + marker)
```

### 3. 加载时检测

每次 Skill 加载时检查标记是否存在：

```python
content = SOUL_PATH.read_text()
match = re.search(r"\[SkillName v([\d.]+)\]", content)
if not match:
    print("SOUL.md 未找到激活标记，是否写入？[Y/N]")
elif match.group(1) != CURRENT_VERSION:
    print(f"版本过旧 (v{match.group(1)} → v{CURRENT_VERSION})，更新？[Y/N]")
```

### 4. 扫盘时检测丢失

如果用户手动删除了激活行，下次扫盘时提醒：

```
⚠️ SOUL.md 中未找到 XX 激活标记。护栏未自动生效。重新写入？[Y/N]
```

## 兼容性保证

- **一行纯文本**：任何编辑器可见可删，不污染文件结构
- **不声明区块**：不写 `<!-- START -->...<!-- END -->`，避免与其他 Skill 冲突
- **多 Skill 共存**：各自一行堆叠在末尾，互不干扰
- **版本可追踪**：标记含版本号，升级时自动检测

## 不适合本方案的场景

- 需要保存大量数据的 Skill（用独立存储）
- 纯工具类 Skill（用户手动触发即可）
- 需要持续后台进程的 Skill（用 gateway plugin）

## 实战参考

- CMG v5.2.1: 首次实现此模式
- 标记格式: `[CMG v5.2.1] 加载 canon-mnemonic-guard 护栏规则`
- init.py 完整实现: `canon-mnemonic-guard/scripts/init.py`
