# skill-autoload 更新日志

## v1.0.0 (2026-05-25) — 首次发布

- 通过 `pre_system_prompt` 钩子自动加载指定 Skill
- 支持 `config.yaml` 配置（`skill_autoload.skills` + `per_platform`）
- 注入 `[MUST-LOAD]` 指令到系统提示词
- 支持按平台控制加载列表（如飞书不自动加载）
