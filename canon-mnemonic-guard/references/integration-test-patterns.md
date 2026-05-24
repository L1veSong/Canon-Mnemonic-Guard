# CMG 联动测试模式

> 2026-05-22 实战验证。Guard 五项联动推荐的测试方法和结果。

---

## 模式 1: 主动触发 Escalation（测 Mnemonic + diagnose）

**方法：** 同一规则在 5 分钟内连续触发 3 次。

**步骤：**
1. 选一条已知 ban 规则（如「禁止跳步骤」）
2. 连续三次说出触发词（如「跳过检查直接交付」）
3. 观察：第1次 warn → 第2次 warn → 第3次 block (context_level: escalated)
4. Mnemonic 自动检测到 3 次/5 分钟 → 推送模式识别草稿
5. 运行 `!diagnose` 验证五阶段诊断

**验证项：** Guard escalation、Mnemonic 模式识别、diagnose 诊断

---

## 模式 2: 未验证声称（测 VBC）

**方法：** Agent 声称完成但未附验证证据。

**步骤：**
1. Agent 说一句类似「全部 X 已完成」
2. Guard FabricationInterceptor 拦截（声称无法核实）
3. Agent 按 VBC 协议：列出验证命令 → 执行 → 逐项给证据 → 出确凿结论

**验证项：** Guard Fabrication、VBC 证据协议

---

## 模式 3: 跳步骤闭环（测 ralph-loop）

**方法：** 模拟多步骤遗漏后 Guard 拦截，用 ralph-loop 补完。

**步骤：**
1. Agent 声称「X 测试已完成」但实际未执行
2. Guard Fabrication 拦截
3. Agent 创建 tasks.json（3+ 步骤+依赖）
4. 逐任务从 pending → in_progress → completed
5. 验证 progress.txt 和 knowledge.md

**验证项：** ralph-loop 闭环、Guard→ralph-loop 联动

---

## 模式 4: 外部数据源（测 plur）

**方法：** 第三方工具写入 → CMG 扫盘读取。

**步骤：**
1. `plur learn "规则内容"` 写入含「禁止/必须」的准则
2. 验证 `~/.plur/engrams.yaml` 有数据
3. CMG 扫盘检查能否读取该文件
4. 提取准则 → 提示导入

**验证项：** plur 数据通道、CMG 自定义扫描源

---

## 验证结果 (2026-05-22)

| 推荐 | 模式 | 结果 |
|------|------|------|
| rtk-rewrite | 直接运行 | ✅ gateway 加载+钩子注册+压缩生效 |
| plur | 模式 4 | ✅ 数据写入+CMG可读 |
| VBC | 模式 2 | ✅ Guard拦截未验证声称→VBC证据协议 |
| diagnose | 模式 1 | ✅ 五阶段诊断+发现_index.md不同步+自动修复 |
| ralph-loop | 模式 3 | ✅ 3步骤闭环+Guard→ralph-loop联动 |
