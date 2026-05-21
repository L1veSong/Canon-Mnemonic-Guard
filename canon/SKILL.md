---
name: canon
description: 三省引擎(CMG)典则线 (Canon) — 规则生产库。负责规则来源、固化、存储、效果评分。纯静态规则层，不执行拦截、不存记忆。
version: 2.5.2
role: producer
stage: system_anchor
dependencies: []
min_hermes_version: any
platforms: [linux, macos, windows]
author: L1veSong
license: MIT
metadata:
  hermes:
    tags: [cmg, canon, rules, self-reflection]
    related_skills: [guard, mnemonic, canon-mnemonic-guard]
---

# Canon 典则线 v2.5.2 — 规则生产库

> **角色**: producer (规则生产锚点) | **阶段**: system_anchor (系统锚点层)
>
> 三省引擎(CMG)典则线。从 CMG v5.0.2 物理拆分独立。不执行拦截、不存记忆——只生产规则。

---

## 文件结构

```
~/.hermes/self-reflection/
├── errors.jsonl              # 原始错误记录 (永久追加)
├── patterns.json             # 匹配模式库 (去重压缩)
├── state.json                # 跨会话状态
├── rules/                    # Obsidian 结构化规则目录
│   ├── _index.md             # 自动索引 + wikilinks 表格
│   ├── ban/                  # 禁止项
│   ├── gap/                  # 缺失项
│   └── lazy/                 # 偷懒项
├── config.json               # 用户配置
└── checklists/               # 防偷懒清单
```

---

## 版本变更

| 版本 | 变更 |
|------|------|
| v2.5.2 | +SOUL 激活机制: init时询问是否写一行激活标记到SOUL.md，扫盘时检测标记状态 |
| v2.5.1 | +推荐列表自动扫描: config.json recommendations + !scan-recommendations + plugins 扫描源 |
| v2.5.0 | +C1 定时扫盘: 加载时检查距上次扫盘天数，超阈值自动触发 |
| v2.4.1 | 护栏逻辑剥离至 guard-spec.md，CMG v5.1.0 四包制分装 |
| v2.4.0 | +规则效果评分 +角色声明制 +简化触发词 +导入导出 |
| v2.3.1 | +规则冲突检测与自动裁决 |
| v2.3.0 | +依赖解耦(RuleReader接口+7适配器) +可配置扫描源 +模式切换 |
| v2.2.9 | +首次真实扫盘提取+固化执行 |
| v2.2.3 | +角色声明制(废除数字优先级) |
| v2.2.0 | +扫盘提取 |
| v2.0.0 | Obsidian 结构化 rules/ 目录 |

---

## 启动时

### 1. 加载配置

读取 `~/.hermes/self-reflection/config.json`。如不存在，使用默认值（含 `auto_scan_interval_days: 7`）。

### 2. 加载规则库

优先加载 `rules/` 目录（结构化规则），降级加载 `rules.permanent.md`（v1 兼容）。

### 3. 加载跨会话状态

读取 `~/.hermes/self-reflection/state.json`，核心字段：

```json
{
  "last_solidify_at": "ISO8601",
  "last_scan_at": "ISO8601",
  "errors_since_solidify": 5,
  "sessions_since_start": 12,
  "last_activation": "ISO8601"
}
```

`last_scan_at` 记录上次扫盘时间（v2.5.0 新增）。

### 4. 检查固化阈值

比较 `errors_since_solidify` 与 `auto_solidify_threshold`。

### 5. 定时扫盘检查（C1 · v2.5.0）

**触发条件：** 每次 Canon 加载时自动执行。

**执行步骤：**

```
1. 读取 state.json → 获取 last_scan_at
2. 计算距上次扫盘的天数
3. 读取 config.json → auto_scan_interval_days（默认 7）
4. 如果 距上次扫盘 ≥ auto_scan_interval_days → 触发扫盘
   - 执行「扫盘提取」章节的完整流程（扫描 SOUL.md / Obsidian / Memory / Skill）
   - 更新 state.json: last_scan_at = now()
   - 输出: "定时扫盘完成。距上次 {N} 天。发现 {M} 条准则 → 待用户确认导入。"
5. 如果未到阈值 → 跳过
   - 输出: "距上次扫盘 {N} 天（阈值 {D} 天），跳过定时扫盘。"
```

**降级：** state.json 缺失或 `last_scan_at` 不存在 → 视同上一次从未扫盘，首次加载时自动触发。

### 5.5 SOUL 激活检测 + 推荐扫描（v2.5.2）

**触发条件：** 每次 Canon 加载时自动执行（在 C1 扫盘之后）。

**执行步骤：**

```
1. 读取 SOUL.md → 搜索 [CMG v{x}.{y}.{z}] 标记
2. 检测结果：
   ✅ 标记存在 + 版本匹配 → 静默通过
   ⚠️ 标记存在 + 版本过旧 → 输出: "CMG 已升级到 v{x}，SOUL.md 激活标记仍为 v{old}。更新？[Y/N]"
   ❌ 标记不存在 → 输出: "SOUL.md 未找到激活标记，护栏未自动生效。重新写入？[Y/N]"
3. 如果 C1 扫盘触发（距上次扫盘超阈值）：
   - 扫盘流程自动包含推荐列表扫描
   - 检查 config.json → recommendations.items[] 逐项
   - 新检测到的已安装推荐 → 提示启用
4. 如果 C1 扫盘未触发（未到阈值）：
   - 跳过推荐扫描（避免每次对话都扫）
   - 用户可用 !scan-recommendations 手动触发
```

**推荐扫描输出格式（扫盘时自动包含）：**

```
📋 推荐列表（自动扫描）:
  ✅ 8 个已就绪
  ⚠️ 1 个待配置: plur（已安装但未启用 → 输入 !scan-recommendations 配置）
  ❌ 0 个未安装
```

**激活标记丢失的恢复流程：**

```
⚠️ SOUL.md 中未找到 CMG 激活标记。
   护栏规则当前未自动生效。

   原因可能：
   1. 你手动删除了 SOUL.md 中的 [CMG v...] 行
   2. SOUL.md 被其他工具覆盖
   3. 这是首次在新设备上使用 CMG

   是否重新写入激活标记？
     [Y] 恢复 — 重新写入 [CMG v5.2.1] 加载 canon-mnemonic-guard 护栏规则
     [N] 跳过 — 护栏保持停用，下次扫盘再提醒

   选择 [Y/n]:
```

**注意：** 激活标记丢失≠CMG 损坏。规则库、配置、推荐列表全部在 `~/.hermes/self-reflection/` 中完整保留。丢失的只是 SOUL.md 中的一行触发器。

**首次安装：** 安装时执行初始扫盘 → 写入 `last_scan_at`。后续按阈值周期触发。

### 6. 加载防偷懒清单

读取 `checklists/` 下 `config.json` 中启用的 YAML 文件。

### 7. 输出激活状态

**必须输出**: "Canon v2.5.2 已激活。{N} 条规则（{ban}/{gap}/{lazy}）。距上次扫盘 {D} 天。定时扫盘: {on/off}（间隔 {X} 天）。"

---

## 用户指出错误时（「记住」触发）

任何表达「记录错误行为 + 希望未来避免」的语句触发。三步走：生成规则 → 写入 rules/ → 更新 patterns.json。

---

## 冲突检测

新规则写入前扫描同类型规则。跨类型检测（ban↔gap↔lazy）已启用。冲突时 clarify 四选一裁决。

---

## 规则效果评分

命中率/误报率/最后命中/创建日期四指标。误报率>30%标记待调整，180天未命中提示过期。

---

## 动态固化阈值

adaptive 模式根据用户纠正频率动态调整（高频→5，正常→10，低频→20），可切换为 fixed。

---

## 规则导入/导出

`!export` → rules/ + state.json + patterns.json → ZIP。`!import <path>` → 逐条冲突检测 → 确认导入。

---

## 扫盘提取

扫描 SOUL.md / Obsidian 铁则库 / Memory / 其他 Skill 中的准则类内容。过滤规则：含「禁止/必须/规则/铁则/HARD-GATE」的准则类提取，纯偏好/闲聊/日志跳过。

### 定时扫盘（C1 · v2.5.0）

扫盘不再是一次性的。每次 Canon 加载时检查 `last_scan_at`，超过 `auto_scan_interval_days`（config.json 中 `auto_scan_interval_days`，默认 7 天）自动触发扫盘。新增规则源（如新安装的 Skill、Obsidian 新增的铁则）会自动纳入。

**扫盘中自动执行推荐检测（v2.5.1 新增）：** 扫盘流程自动包含推荐列表扫描——检查 config.json 的 `recommendations.items[]`，对每个推荐项验证是否已安装、是否已配置。未配置的已安装项 → 提示用户启用。

### 手动扫盘

用户说「扫盘」/「扫描规则」/「提取准则」→ 立即执行扫盘，不受阈值限制。执行后更新 `last_scan_at`。

### 推荐列表扫描（v2.5.1 新增）

**触发词**: `!scan-recommendations` 或「扫描推荐」/「检查推荐列表」

独立于规则扫盘。只扫描 config.json 的 `recommendations.items[]`，不扫规则源。

**执行流程：**

```
1. 读取 config.json → recommendations.items[]
2. 逐项检测安装状态:
   - type=skill: 检查 detection_path 文件是否存在
   - type=plugin: 检查 pip entry points (detection_group + detection_name)
   - type=mcp_server: 检查 detection_path 文件是否存在
3. 逐项检测配置状态:
   - skill: 检查 skill 是否在 Hermes 已安装列表中
   - plugin: 检查 config.yaml plugins.enabled 是否包含
   - mcp_server: 检查 ~/.hermes/config.yaml 是否有对应 provider
4. 分类输出:
   - ✅ 已安装+已配置: N 个（正常）
   - ⚠️ 已安装+未配置: N 个 → 逐一询问用户是否启用
   - ❌ 未安装: N 个
5. 用户确认启用 → 自动配置（skill: 无需操作已可用; plugin: 写入 config.yaml; mcp: 写入 custom scan source）
6. 更新 recommendations.items[].configured = true
7. 更新 recommendations.last_scan
```

**自动询问格式：**

```
⚠️ 发现已安装但未配置的推荐工具：

  1. verify-before-completion (护栏增强)
     → Guard 拦截「声称完成但未验证」后自动调用
     启用？ [Y] 是 [N] 跳过

  2. rtk-rewrite (成本优化)
     → 压缩终端输出 60-90% token
     启用？ [Y] 是 [N] 跳过
```

用户确认后自动写入对应配置，无需手动编辑 config.yaml。

---

## 固化引擎

errors.jsonl → 去重合并 → rules/ 目录独立 .md → _index.md 自动索引 → patterns.json 更新。

---

## 健康检查

启动时检测 rules/ state.json patterns.json intercept_log.jsonl mnemonic_state.json 五文件完整性。

---

## config.json 参考

```json
{
  "auto_solidify_threshold": 10,
  "solidify_threshold_mode": "adaptive",
  "auto_scan_interval_days": 7,
  "conflict_detection": {"cross_type": true},
  "scoring": {"false_positive_threshold": 0.3, "expiry_days": 180},
  "health_check": {"enabled": true},
  "scan_sources": {
    "builtin": {"soul": true, "memory": true, "skills": true},
    "obsidian": {"enabled": true, "vault_path": "~/obsidian", "rule_dirs": ["🔒 HERMES-全局铁则库"]},
    "custom": []
  }
}
```

---

## 参考文件

- [SOUL 激活模式](references/soul-activation-pattern.md) — 技能自激活的通用方案
- [推荐列表配置 schema](references/recommendations-config-schema.md) — config.json recommendations 字段完整 schema
- [CHANGELOG.md](CHANGELOG.md) — 完整版本变更记录
- [README.md](README.md) — 快速上手指南

## 安装与激活

```bash
npx skills add canon --yes --global
npx skills add guard --yes --global
npx skills add mnemonic --yes --global
npx skills add canon-mnemonic-guard --yes --global
```

安装完成后运行初始化：

```bash
npx canon-mnemonic-guard init
```

### init 流程（v2.5.2）

```
✅ rules/ 目录已创建（ban/gap/lazy）
✅ config.json 已生成
✅ state.json / patterns.json 已初始化

📋 扫描推荐列表中……

═══════════════════════════════════════
⚡ 护栏自动激活
═══════════════════════════════════════

是否在 SOUL.md 中写入激活标记（一行），让护栏规则在每次对话中自动生效？

  [Y] 是 — 写入一行: [CMG v5.2.1] 加载 canon-mnemonic-guard 护栏规则
  [N] 否 — 跳过，用 !scan 手动触发

选择 [Y/n]: 
```

**选 Y：** 在 SOUL.md 末尾追加一行激活标记。Hermes 读取 SOUL.md 时看到这行 → 自动加载 CMG 技能 → Guard 护栏在每次对话中生效。

**选 N：** 规则仅在 rules/ 目录中。用户手动 `/skill canon-mnemonic-guard` 或 `/skill guard` 触发。

### 激活标记格式

```
[CMG v5.2.1] 加载 canon-mnemonic-guard 护栏规则
```

这是 SOUL.md 中普通的一行文本。你可以随时手动删除——删掉后护栏不再自动生效。下一次扫盘时会检测到缺失并提醒。

### 扫盘时自动检测激活标记（v2.5.2）

每次扫盘（C1 定时或 `!scan` 手动）都会检查 SOUL.md 中是否存在 `[CMG v` 开头的激活行：

| 检测结果 | 行为 |
|---------|------|
| ✅ 标记存在且版本匹配 | 正常，静默通过 |
| ⚠️ 标记存在但版本过旧 | 提示升级：「CMG 已升级到 v{x}，SOUL.md 中激活标记仍为 v{old}。更新？[Y/N]」 |
| ❌ 标记不存在 | 提示缺失：「SOUL.md 中未找到 CMG 激活标记，护栏规则未自动生效。重新注入？[Y/N]」 |

用户选 Y → 自动更新/写入标记。选 N → 保持当前状态。

### 激活标记的兼容性

- **格式极简：** 一行纯文本，任何文本编辑器可见可删
- **不干扰其他内容：** 追加到 SOUL.md 末尾，不修改已有内容
- **版本可追踪：** 标记含版本号，升级时检测更新
- **可撤销：** 删除这行即可停用护栏，CMG 只在下一次扫盘时提醒一次
- **跨设备：** 如果你的 SOUL.md 通过 Obsidian/Git 同步，激活标记随文件迁移
