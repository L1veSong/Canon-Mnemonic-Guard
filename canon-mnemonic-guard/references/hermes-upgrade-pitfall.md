# Hermes Major Version Upgrade — CMG 适配

> 坑点 14，追加于 2026-05-26 Hermes v0.14.0 升级实战。

## 症状

Hermes 大版本升级后，CMG 三层闭环可能有层静默失效。skill-autoload 插件注册失败但不报错（只有 WARNING 级别日志），CMG skills 文件可能被升级流程清空。

## 根因

1. Hermes v0.14.0 移除了 `pre_system_prompt` hook，skill-autoload v1.0.0 依赖此 hook
2. Hermes 升级可能清空 `~/.hermes/skills/` 下的用户安装 skills

## 检测

```bash
grep -E "cmg|unknown hook" ~/.hermes/logs/agent.log | tail -5
```

若出现 `unknown hook 'pre_system_prompt'` → skill-autoload 失效。

## 修复

1. 恢复 CMG 四包：从 zip 备份或 GitHub (`L1veSong/Canon-Mnemonic-Guard`) 复制到 `~/.hermes/skills/`
2. 迁移 skill-autoload 到 `pre_llm_call`（见 `hermes-agent` skill 的 `references/skill-autoload-plugin.md`）
3. 添加 SOUL.md 激活行作为双保险
4. 重启 Hermes，验证 agent.log 无 `unknown hook` 警告

## 预防

每次 Hermes 大版本升级后，主动执行上述检测流程。不要等用户发现 CMG 不生效。
