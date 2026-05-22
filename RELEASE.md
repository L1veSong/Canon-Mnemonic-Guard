# 三省引擎 CMG v5.3.0 发布公告

> Canon-Mnemonic-Guard · 典忆卫 · 从拦截器到监工

---

## v5.3.0: 典忆卫・闭环校验器

**这是质变。Guard 不再只是一个红灯。**

之前的版本，Guard 能拦住 Agent 说「不许过」，但拦住了之后呢？Agent 可能僵在那里，也可能换句话继续糊弄。用户只知道「被拦了」，不知道「怎么过」。

v5.3.0 的闭环校验器解决了这个问题：

```
Agent 跳过步骤想交差
        │
        ▼
Guard StepCompleteness 拦截
        │
        ├── 剩余 1 步 → 提醒即可
        │
        └── 剩余 ≥ 2 步 → 启动典忆卫・闭环校验器
                │
                ▼
        逐步骤催办:
        [1/3] xxx → Agent执行 → 验证 → ✅
        [2/3] xxx → Agent执行 → 验证 → ✅
        [3/3] xxx → Agent执行 → 验证 → ✅
                │
                ▼
        全部闭环。放行。
```

### 设计原则

- **零外部依赖** — 不用 ralph-loop、不写文件、不委派子 Agent。纯典忆卫原生实现。
- **典忆卫语言体系** — 用规则编号、拦截器框架、对话上下文分析，没有引入任何外部概念。
- **ralph-loop 保留为进阶扩展** — 闭环校验器管单会话步骤遗漏，ralph-loop 管跨会话大项目。互补不重叠。

---

## 四包版本

| 包 | 版本 | 变更 |
|----|------|------|
| canon-mnemonic-guard | v5.3.0 | 闭环校验器外观索引 |
| guard | v4.6.0 | +典忆卫・闭环校验器 |
| canon | v2.5.2 | 无变更 |
| mnemonic | v3.3.0 | 无变更 |

---

## 已验证能力

- Guard 五层拦截全部实测通过（Ban ×4 / Fabrication ×2 / StepCompleteness ×6 含 escalation / SkillLoad ×1）
- 闭环校验器端到端通过（3 步任务截断 → 逐步骤催办 → 全部闭环）
- 5 项推荐联动全部验证通过

---

## 快速开始

```bash
npx skills add canon-mnemonic-guard --yes --global
python3 init.py
# 选 Y → SOUL 激活 → 完事
```

---

## 链接

- GitHub: https://github.com/L1veSong/Canon-Mnemonic-Guard
- License: MIT
