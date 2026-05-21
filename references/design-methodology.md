# 设计方法论 — 三省引擎 (CMG)

从 v1.0.0 到 v5.0.0 迭代中沉淀的 9 条核心设计原则。

---

## 1. 彻底解耦 · 物理拆分 · 单向依赖

四个模块（Canon/Guard/Mnemonic/Engine）严格独立，各自一份 SKILL.md。通过标准化接口（rules/*.md / errors.jsonl / state.json / intercept_log.jsonl）联动，不互相寄生。

```
典则 Canon = 规则生产库 → 不碰拦截、不碰记忆、不做校验
护栏 Guard = 规则执行器 → 不生产规则、不存记忆
忆存 Mnemonic = 状态记忆层 → 不生产规则、不执行拦截
```

---

## 2. 外观模式：封装即协同

统一引擎对外声明单一角色 `role: guard, stage: pre_action`，内部三线子角色（producer/memory/guard）保留。外部 Skill 不需要知道内部有几条线。

否决多角色声明——`roles: [producer, memory, guard]` 会把内部架构泄露成外部契约。

---

## 3. 角色声明制：废除数字优先级

Skill 之间不通过 `priority: 110` 竞争执行顺序，而是声明 `role + stage`：

```
Canon:   role: producer, stage: system_anchor
Mnemonic: role: memory,   stage: background
Guard:   role: guard,     stage: pre_action
```

新 Skill 加入只需声明 role+stage，自动归入对应阶段。

---

## 4. 添加式集成：只读不写不修改

CMG 只消费第三方工具的产出，绝不修改第三方工具的行为或配置。用户选「是」则单向读取，选「否」则完全无视。双向都不发生 CMG 向第三方的写入。

---

## 5. 白名单扫描：绝不全盘扫描

可配置扫描源（config.json 的 `scan_sources`），只扫用户明确指定的路径。内置源默认开启，自定义源用户不配就不扫。

---

## 6. 版本体系独立：禁止交叉引用外部版本号

CMG 的三线架构（Canon 2.x / Mnemonic 3.x / Guard 4.x）有独立版本体系。绝不引用 Idea Foundry 的 v8/v9 或其他外部 Skill 的内部版本号。

---

## 7. 坑点驱动迭代：每个错误写入文档

SKILL.md 的「常见坑点」章节来自实际维护中的反复修正。当前收录 10 条，每条包含错误示例 + 正确做法。

---

## 8. 闭环验证优先设计实施

真实数据流验证（Guard 拦截→Mnemonic 模式识别→Canon 固化）优先于功能堆砌。13 条未来优化方向在闭环未通之前全部暂缓。

---

## 9. 命名一致性：正式名 + 昵称分工

- 三省引擎 — 正式中文名，取自「吾日三省吾身」
- 典忆卫 — 昵称/简称，三字各对应一条线
- CMG — 英文简写（Canon-Mnemonic-Guard）
- 三线：典则线 / 护栏线 / 忆存线
