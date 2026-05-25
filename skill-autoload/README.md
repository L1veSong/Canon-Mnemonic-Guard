# skill-autoload

> Hermes 插件：会话首轮自动加载指定 Skill。零手动操作。

## 解决什么

Hermes 不支持"每次会话自动加载某个 Skill"。CMG 这样的护栏类 Skill 需要每次生效，但 SOUL.md 注入不可靠——AI 可能跳过。

`skill-autoload` 通过 `pre_llm_call` 钩子，在首轮 LLM 调用前注入强制加载指令到用户消息上下文。

## 版本历史

| 版本 | Hermes 兼容 | Hook | 说明 |
|------|------------|------|------|
| v1.0.0 | ≤ v0.13.x | `pre_system_prompt` | 原始版本 |
| v1.0.1 | ≥ v0.14.0 | `pre_llm_call` | 适配 Hermes v0.14.0（pre_system_prompt 已移除） |

## 安装

```bash
# 复制到 Hermes 插件目录
cp -r skill-autoload ~/.hermes/plugins/
```

然后在 `~/.hermes/config.yaml` 中启用：

```yaml
plugins:
  enabled:
    - skill-autoload
```

## 配置

```yaml
skill_autoload:
  skills:
    - canon-mnemonic-guard
    - karpathy-coding-guidelines
  per_platform:
    cli: [canon-mnemonic-guard]
    feishu: []
    weixin: []
```

- `skills`: 默认列表，所有平台生效
- `per_platform.<platform>`: 按平台覆盖。空列表 `[]` 表示该平台不自动加载

## 工作原理（v1.0.1）

1. 每次 LLM 调用前触发 `pre_llm_call` 钩子
2. 仅首轮（`is_first_turn=True`）且该会话未注入过时，注入 `[MUST-LOAD]` 上下文
3. 上下文注入到用户消息中（非 system prompt，保护 prompt 缓存）
4. AI 看到指令后自动加载配置的 Skill

## 验证

重启 Hermes，新会话首轮用户消息前应出现：

```
[MUST-LOAD] 以下技能已配置为自动加载...
  必须加载: canon-mnemonic-guard
```

日志应显示：

```
[skill-autoload] plugin registered (default skills: ['canon-mnemonic-guard'])
```

不应出现 `unknown hook 'pre_system_prompt'` 警告。

## License

MIT © 2026 L1veSong
