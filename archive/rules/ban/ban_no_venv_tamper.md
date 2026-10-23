---
type: ban
id: ban_no_venv_tamper
date: 2026-06-28
last_triggered: 2026-06-28
hit_count: 1
false_positives: 0
source_ids: [err_venv_tamper_20260628]
keywords: ['删venv', '重建venv', '去掉venv', '改venv', 'pip install给Hermes', '两套环境统一', '彻底解决环境问题']
level: soft
downgrade_note: 2026-09-24 全量降级：hard→soft（只记录+提醒，不再拦整条回答），用户要求停止误拦
correction_template: |
  不碰Hermes自己的venv。用已有的hermes-pip别名装包。任何涉及~/.hermes/破坏性操作前先确认有完整回滚方案。
---

# 禁止操作 Hermes 自己的 venv

**规则:** Hermes 的 venv 是运行时环境，任何对其的破坏性操作（删除、重建、替换 Python 版本）都可能让 Hermes 自身崩溃——且崩溃后无法自救。

**触发场景:**
- 用户问「能不能去掉 venv」「能不能不用 venv」
- pip install 装错地方想「彻底解决」
- 想把 Hermes venv 的 Python 版本升级

**正确做法:**
- 用 `hermes-pip` 别名或全路径 `~/.hermes/hermes-agent/venv/bin/pip install xxx`
- venv 是 Hermes 运行时的一部分，不在其中做破坏性操作
- 已有的简单方案（别名）就是最终方案，不追求更「彻底」的

**2026-06-28 实战教训:**
用户已有 hermes-pip 别名（永久方案），AI 仍试图删 venv 重建。
删到一半依赖不完整 → API 中断 → AI 无法自救 → 用户靠 Reasonix 维修恢复。
备份 venv 因 Python 3.11→3.12 ABI 不兼容而损坏，回滚不可用。
