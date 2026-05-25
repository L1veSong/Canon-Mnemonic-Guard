# cmg-guard

> Hermes 插件：CMG 规则硬拦截。AI 的输出不经检查到不了用户眼睛。

## 解决什么

CMG 的 ban 规则在 Skill 层靠 AI 自觉遵守——可以被跳过。

`cmg-guard` 在 Plugin 层注册 `transform_llm_output` 钩子，每次 AI 生成回复后扫描输出文本，命中违规关键词直接替换。AI 绕不过去。

## 三层闭环

```
skill-autoload (Plugin) → 保证 CMG 被加载
        ↓
CMG Skill               → AI 读规则，微型调度
        ↓
cmg-guard (Plugin)       → 输出前硬拦截，违规就替换
```

## 安装

```bash
cp -r cmg-guard ~/.hermes/plugins/
```

```yaml
# ~/.hermes/config.yaml
plugins:
  enabled:
    - cmg-guard
```

## 原理

- 读取 `~/.hermes/self-reflection/rules/ban/*.md` 的关键词
- AI 每次回复 → `transform_llm_output` 扫描全文
- 命中 → 替换为 `[CMG 拦截] 请遵守规则重新回答`
- AI 下一轮看到提示 → 自动修正

## 依赖

- Hermes Agent（`transform_llm_output` 钩子）
- CMG Skill（提供 ban 规则库）

## License

MIT © 2026 L1veSong
