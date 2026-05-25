# CMG 生态系统更新日志

## v5.5.1 (2026-05-25) — 自动加载推荐

### canon-mnemonic-guard v5.5.1
- README 新增 skill-autoload 插件推荐，取代 SOUL 手动激活
- 配套生态加入 skill-autoload

### skill-autoload v1.0.0（新增）
- 首次发布：通过 pre_system_prompt 钩子自动加载指定 Skill
- 支持 config.yaml 配置，按平台控制加载列表

### 四包合集
- 首次以 ecosystem 形式发布，包含全部四包 + 自动加载插件

---

## v5.5.0 (2026-05-25) — 微型调度器

### canon-mnemonic-guard v5.5.0
- 微型调度器：Guard 拦截自动匹配配套 skill
- P1-P4 全部完成，17 项待优化全部清零

### canon v2.7.1 / guard v4.8.1 / mnemonic v3.5.2
- 四包当前版本，功能稳定

---

完整历史见各子包 CHANGELOG.md。
