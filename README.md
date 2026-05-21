# Guard 护栏线 v4.0.0

> 自省引擎的规则执行器。从 Canon Mnemonic Guard v2.4.1 剥离独立。

Guard 是规范执行层——它不生产规则、不存储记忆、只执行拦截。运行时读取 Canon 规则库和 Mnemonic 状态，通过五层拦截器确保 AI 行为符合用户规范。

## 安装

```bash
npx skills add guard --yes --global
```

## 工作原理

```
用户请求 → Guard 五层拦截检查 → 放行/拦截 → 执行
                │
                ├── 命中 → 拦截 + 写入 intercept_log + 更新 Canon 评分
                └── 未命中 → 放行
```

## 五层拦截器

| 拦截器 | 功能 |
|--------|------|
| BanInterceptor | 精确关键词匹配，命中即拦截 |
| FabricationInterceptor | 识别幻觉声称，逐条核实 |
| StepCompletenessInterceptor | 拆解指令步骤，防止跳步 |
| SkillLoadInterceptor | 检测领域 Skill 是否加载 |
| ClarifyInterceptor | 多选项场景强制 clarify |

## 与 Canon / Mnemonic 联动

Canon 生产规则 → Guard 执行拦截 → Mnemonic 分析模式 → Canon 固化升级。

## License

MIT © L1veSong
