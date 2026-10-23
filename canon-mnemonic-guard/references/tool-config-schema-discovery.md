# 工具 Config Schema 发现指南

> 写任何工具的配置文件前，必须先验证其实际 schema。禁止猜测。

## 核心原则

遇到"帮我配置 X 工具"时，先问：我知道 X 的 config 格式吗？
不知道 → 先查，再写。绝不凭经验编造 JSON 结构。

## 按工具类型查 schema

### 1. npm 全局包（最常见）

```bash
# 确认安装位置
which <tool>           # → /Users/xxx/.local/bin/<tool>
ls -l $(which <tool>)  # → 找到实际安装目录

# 找 TypeScript 类型定义（最可靠）
grep 'interface.*Config' <pkg>/dist/index.d.ts
# 例：grep -A 50 'interface ReasonixConfig' .../reasonix/dist/index.d.ts
# → 得到完整字段定义：apiKey?, lang?, theme?, mcpServers?, ...

# 找子类型
grep 'interface McpServerConfig' <pkg>/dist/index.d.ts
# → command?, args?, env?, transport?, url?, headers?, disabled?
```

**实战案例：** 用户要求写 Reasonix config.json。第一次凭猜测写了错误结构（`"apiKey"` 放在顶层但缺少 `mcpServers` 正确嵌套）。被纠正后，读 `~/.local/lib/node_modules/reasonix/dist/index.d.ts` 找到 `ReasonixConfig` 接口 → 确认了 `apiKey`, `lang`, `theme`, `mcpServers`, `reasoningEffort` 等字段的准确名称和类型。

### 2. Python 包

```bash
pip3 show <pkg>        # → Location: /path/to/site-packages
grep -r 'config' <path>/<pkg>/  # 搜索 config 相关代码
# 或直接看源码中 Config 类/dataclass
```

### 3. CLI 工具（无包管理器）

```bash
<tool> --help           # 查看是否有 config 子命令
<tool> config --help    # 如 reasonix setup（交互式向导）
<tool> config show      # 查看当前配置（如有）
```

### 4. 已有配置文件（最可靠）

```bash
cat ~/.<tool>/config.json   # 看已有字段名和结构
# 从已有配置推断 schema，增量添加
```

## 反模式

| ❌ 错误 | ✅ 正确 |
|--------|--------|
| 看到 `apiKey` 就写 `"apiKey": "sk-xxx"` | 先查接口定义确认字段名是 `apiKey` 还是 `api_key` 还是 `key` |
| MCP 服务器写 `{name: {command, args}}` | 查 `McpServerConfig` 确认是 `command` + `args`，不是 `cmd` + `argv` |
| 凭感觉写 JSON 结构 | 从 `.d.ts` / 源码 / 已有配置 三选一验证 |
| 改了再说，错了再改 | 先读 schema，一次写对 |

## 本会话教训

Reasonix config.json：第一次按通用格式猜测 → 结构错（CMG ban_act_before_verify 的典型违规）。正确做法：读 `index.d.ts` → 找到 `ReasonixConfig` + `McpServerConfig` → 按真实 schema 重写。

关联 CMG 规则：`ban_act_before_verify`（验证先于动作）、坑点 24（验证先于结论）。
