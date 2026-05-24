# CMG 三省引擎 v5.5.0

> AI 的错题本 + 免疫系统 + 监工。取自「吾日三省吾身」。
> 你只需指出一次错误，它从此记住。53 条规则，全部从你的实际使用中生长出来。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-5.5.0-blue)]()

---

## 解决什么问题

和 AI 协作时，你会反复纠正同样的错误——"别编造""加载 skill 再干活""发布前检查版本号"。CMG 让你只需纠正一次：它记住规则、下次自动拦截、甚至从拦截日志中发现新模式推给你确认。

不是"建议"，是"拦截"。不是静态规则表，是会学习的免疫系统。

## 怎么工作

```
你犯了错 → 说「记住，禁止xxx」
    ↓
Canon 写入 rules/ 目录（一条 .md 规则，含修正模板）
    ↓
Guard 每次行动前检查五层拦截器 → 命中就拦
    ↓
拦截事件写入 intercept_log.jsonl
    ↓
Mnemonic 分析日志 → 同会话第2次命中 → 自动推规则草稿
    ↓
你确认 → Canon 固化 → 规则库 +1
    ↓
Guard 下一轮用新规则拦截 + 微型调度器推荐配套 skill
```

规则存在 `~/.hermes/self-reflection/rules/` 下——纯 Markdown，Obsidian 原生可浏览，Dataview 可查询。

## 四层架构

CMG 是四包制外观引擎，内部三条独立线路 + 外观索引层：

### Canon 典则线 v2.7.1 — 规则生产库

你说「记住」→ 写入规则 → 去重固化 → 冲突检测 → 效果评分。

- 规则分级 hard/soft/monitor，含 correction_template（告诉 AI 怎么改）
- 误报自动降级：连续否决 ≥3 次 → 自动降为 soft
- 规则有效期：`!remember --expires 7d "临时规则"`，到期自动归档
- 扫盘提取：自动扫描 SOUL.md / Obsidian / Memory 中的准则类内容
- 定时扫盘：每 7 天自动触发，新安装 skill 的准则自动纳入

### Guard 护栏线 v4.8.1 — 规则执行器

每次 AI 行动前执行五层拦截，任一命中就拦：

| 层级 | 拦截器 | 检查什么 |
|------|--------|---------|
| 1 | BanInterceptor | 精确关键词匹配（"虚构""跳过验证"） |
| 2 | FabricationInterceptor | 防幻觉声称（"已经创建了""确认无误"） |
| 3 | StepCompletenessInterceptor | 用户指令的步骤是否全部完成 |
| 4 | SkillLoadInterceptor | 当前任务是否加载了对应 skill |
| 5 | ClarifyInterceptor | 多选项时是否调用了 clarify 确认 |

- 同会话第 2 次命中直接 block（原 3 次），24h 半衰期防误升级
- 你说「记住」「别再犯」→ 规则自动提升（monitor→soft→hard）
- 闭环重试引擎：拦截后注入修正方向 → AI 重生成 → 再检 → 合格放行
- 风险分级：不可逆操作（删除/覆盖）暂停确认，可自动修复自动重试
- 拦截日志写入 `intercept_log.jsonl`，Mnemonic 消费

### Mnemonic 忆存线 v3.5.2 — 模式识别

消费 Guard 拦截日志，自动发现重复犯错模式：

- 同会话同一规则第 2 次命中 → 立即推草稿（原需 7 天 3 次）
- 跨会话 7 天内累计 2 次 → 推草稿
- 你确认后推送给 Canon 固化
- `!patterns` 查看当前识别的模式（本会话命中 / 7 天 / 置信度 / 推荐操作）
- `!datasource` 查看数据源状态（guard_intercept / canon_errors / none）
- 命中上下文保留：每次拦截记录触发场景，解决 unknown 规则无法还原

### CMG 外观层 v5.5.0 — 微型调度 + 四包索引

- `init.py` 一键初始化：创建 rules/ 目录 + config.json + SOUL 激活标记
- `!diagnose` 五阶段深度诊断（文件完整性 → 规则有效性 → 跨模块引用 → 数据源 → 版本一致性）
- `!log` 三线协调日志统一视图
- **微型调度器（v5.5.0）：Guard 拦截时自动匹配配套 skill，提示加载**

## 微型调度器

Guard 拦截 → 场景匹配 → 提示加载。推荐列表不再只是手册。

**拦截触发型：**

| 拦截场景 | 自动推荐 |
|---------|---------|
| 过设计/复杂化 | karpathy-coding-guidelines |
| 跳步骤/未闭环 | ralph-loop |
| 声称完成未验证 | verification-before-completion |
| 同规则连续命中 ≥3 次 | diagnose |

**被动/基础设施型（标注状态即可）：** rtk-rewrite（Gateway 自动运行）、plur（扫盘时读取）、obsidian（直接浏览 rules/）、hermes-agent-skill-authoring（发布时加载）、gstack/careful + guard（Hermes hook 限制，参考模式）。

## 命令

| 命令 | 做什么 | 示例 |
|------|--------|------|
| `!remember 禁止xxx` | 记录规则 | `!remember --hard "禁止跳过验证"` |
| `!remember --expires 7d` | 临时规则 | `!remember --expires 7d "论文格式检查"` |
| `!scan` | 手动扫盘 | 扫描 SOUL/Obsidian/Memory 中准则 |
| `!patterns` | 查看识别模式 | 表格：规则/本会话/7天/置信度/推荐 |
| `!datasource` | 数据源状态 | 当前源/健康/切换历史/降级链 |
| `!solidify` | 手动固化 | errors.jsonl → 去重 → 写入 rules/ |
| `!log` | 协调日志 | Canon/Guard/Mnemonic 三线汇总 |
| `!diagnose` | 一键诊断 | 五阶段：文件→规则→引用→数据源→版本 |
| `!export` | 导出规则 | 打包 rules/ 为 ZIP |
| `!import <path>` | 导入规则 | 解压 ZIP → 冲突检测 → 逐条确认 |

## 安装

### 一键安装（推荐）

```bash
npx skills add canon-mnemonic-guard --yes --global
npx canon-mnemonic-guard init
```

init 流程：
1. 创建 `~/.hermes/self-reflection/rules/` 目录结构
2. 生成 `config.json` / `state.json` / `patterns.json`
3. 询问是否在 SOUL.md 写入激活标记
4. 选 Y → 每次对话自动生效。选 N → 手动 `/skill canon-mnemonic-guard`

### 分别安装子包

```bash
npx skills add guard --yes --global
npx skills add canon --yes --global
npx skills add mnemonic --yes --global
```

### 手动安装

```bash
mkdir -p ~/.hermes/skills/software-development
# 解压 CMG-v5.5.0-full.zip 中的四个目录到上述路径
# 运行 canon-mnemonic-guard/scripts/init.py
```

## 配套生态

8 个验证通过的配套 skill，按三线归属：

**护栏线（拦截执行 · 验证闭环）：**

| 推荐 | 增强点 |
|------|--------|
| ralph-loop | Guard 拦截跳步骤 → 自动触发闭环验证 |
| verification-before-completion | Guard 拦截「声称完成」→ 要求证据 |
| diagnose | 同规则连续命中 → !diagnose 诊断根因 |
| karpathy-coding-guidelines | 进攻型行为准则，防守+进攻互补（已双向认可） |

**典则线（规则扩展 · 可视化）：**

| 推荐 | 增强点 |
|------|--------|
| plur | 扩展规则来源，扫盘读取 ~/.plur/engrams.yaml |
| obsidian | rules/*.md 可视化 + Dataview 查询 + 图谱链接 |

**跨线共享（基础设施）：**

| 推荐 | 增强点 |
|------|--------|
| rtk-rewrite | 压缩终端输出 60-90% token（Gateway 插件） |
| hermes-agent-skill-authoring | 13 项发布自检清单 + 版本号 grep 验证 |

**参考模式：** gstack/careful、gstack/guard（命令层安全，Hermes hook 限制下作为参考模式）。

所有配套满足**添加式集成**标准：CMG 只消费第三方产出，绝不修改第三方行为。装不装推荐，第三方本身功能完全不受影响。

## 文件结构

```
~/.hermes/self-reflection/
├── errors.jsonl              # 原始错误记录（永久追加）
├── patterns.json             # 匹配模式库（去重压缩）
├── state.json                # 跨会话状态
├── mnemonic_state.json       # Mnemonic 持久化状态
├── intercept_log.jsonl       # Guard 拦截日志
├── config.json               # 用户配置
├── rules/                    # 规则库（Obsidian .md 格式）
│   ├── _index.md             # 自动索引
│   ├── ban/                  # 禁止项（36 条）
│   ├── gap/                  # 缺失项（8 条）
│   └── lazy/                 # 偷懒项（9 条）
└── checklists/               # 防偷懒清单
```

## 版本路线

| 版本 | 里程碑 |
|------|--------|
| v5.0.0 | 三线合一外观模式 |
| v5.1.0 | 四包制分装 |
| v5.2.0 | 定时扫盘 + 协调日志 + 一键诊断 |
| v5.3.0 | Guard 风险分级 |
| v5.4.0 | P1+P3+P4 + Mnemonic 上下文保留 |
| v5.4.1 | P2 补全（Mnemonic 加速 + session 追踪） |
| v5.4.2 | M3 清零（!patterns + !datasource） |
| **v5.5.0** | **微型调度器 + 三线归属恢复** |
| 未来 | 完整中央调度器（独立项目） |

## P 系列全貌

| # | 功能 | 版本 |
|---|------|:--:|
| P1 | 同会话第 2 次拦截 + 24h 半衰期衰减 | v5.4.0 |
| P2 | Mnemonic 加速模式识别（2 次推草稿 + session 追踪） | v5.4.1 |
| P3 | 用户纠正自动提升（monitor→soft→hard） | v5.4.0 |
| P4 | 误报自动降级 + 规则有效期 | v5.4.0 |

## FAQ

**Q: 规则库会被打包到 ZIP 里吗？**
不会。`rules/` 是你的本地数据，在 `~/.hermes/self-reflection/` 下，不在发布的 ZIP 中。别人安装 CMG 后从零开始积累自己的规则。

**Q: 和其他 skill 会冲突吗？**
不会。CMG 采用 stage 声明制（system_anchor → pre_action → dispatch），所有 skill 按声明位置排队。CMG 是 pre_action 护栏，在所有 skill 执行前检查。

**Q: 能自动调用配套 skill 吗？**
v5.5.0 微型调度器会在 Guard 拦截时提示加载配套 skill。完整的自动调度在 roadmap 中规划为独立项目。

**Q: 规则太多会不会拖慢响应？**
53 条规则 + 五层拦截器，在规则数 > 20 时自动切换轻量模式（只跑第一层精确匹配），避免上下文膨胀。

## License

MIT © [L1veSong](https://github.com/L1veSong)
