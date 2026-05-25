# skill-autoload

> Hermes 插件：会话开始时自动加载指定 Skill。零手动操作。

## 解决什么

Hermes 不支持"每次会话自动加载某个 Skill"。CMG 这样的护栏类 Skill 需要每次生效，但 SOUL.md 注入不可靠——AI 可能跳过。

`skill-autoload` 通过 `pre_system_prompt` 钩子，在系统提示词构建后、发送给 LLM 前，注入强制加载指令。

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

## 依赖

- Hermes Agent 需包含 `pre_system_prompt` 钩子（PR: https://github.com/NousResearch/hermes-agent/pulls）
- 钩子未合入前，可本地应用 patch（见下文）

## 本地 patch（PR 合入前）

```bash
cd ~/.hermes/hermes-agent
git remote add L1veSong https://github.com/L1veSong/hermes-agent.git
git fetch L1veSong
git cherry-pick <commit-hash>   # pre_system_prompt 钩子的 commit
```

## 验证

重启 Hermes，新会话的系统提示词末尾应出现：

```
[MUST-LOAD] 以下技能已配置为自动加载...
  必须加载: canon-mnemonic-guard
```

AI 会在每个会话开始时自动加载列表中所有 Skill。

## License

MIT © 2026 L1veSong
