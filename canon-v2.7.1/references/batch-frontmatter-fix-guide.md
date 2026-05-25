# 批量补全 frontmatter 实战指南

> 2026-05-25 实战验证：52 条规则（35 ban + 8 gap + 9 lazy），13→52 条有 level，0→39 条有 correction_template。

## 触发条件

`_index.md` 过期（条目数 ≠ 实际文件数）且大量规则缺 `level` + `correction_template`。

## 三步走

### Step 1：分类（5 分钟）

扫描 ban/gap/lazy 三个目录，逐文件判断：

| 类型 | 判定标准 | 需 level? |
|------|---------|----------|
| 真规则 | 有明确禁止/必须/强制语义 | 是 |
| 元配置 | 偏好/开关/工作流约定（如"完全自动化模式""思考模式关闭"） | 标 meta |
| unknown 空壳 | 有 hit_count 但无规则内容 | 标 monitor |

**边缘案例：** "禁止跳步骤偷懒摆烂"在 lazy/ 目录但含规则性质 → 标 soft。

**关键操作：** 读每个文件前 2000 字符，检查 `# heading` 和正文内容判断分类。不可仅凭目录归属判断——gap/lazy 目录混了大量元配置。

### Step 2：重建 _index.md

生成完整索引，52 条全列出。level 列先标"待定"，让系统看到全貌。

**生成脚本逻辑：**
```python
for category in ["ban", "gap", "lazy"]:
    for fname in sorted list:
        extract level from frontmatter if exists
        generate [[wikilink]] row
```

### Step 3：分批补 frontmatter（每批 5-12 条）

**分批策略：**
- 第 1 批：ban 发布流程类（全 hard，8 条）
- 第 2 批：ban 核心行为类（全 hard，7 条）
- 第 3 批：混合（ban 风格类 + gap + lazy，混合 hard/soft/monitor，12 条）
- 尾批：unknown 空壳（标 monitor，6 条）+ meta 文件（标 meta，5 条）

**每批执行步骤：**
1. 读取文件 → 找到 frontmatter 闭合 `\n---`（偏移 4 之后第一个）
2. 在闭合前插入 `level: xxx` + `correction_template: "xxx"`
3. 写入文件
4. 立即验证：`read_file` 前 500 字符确认 `level:` 存在

**Python 插入模板：**
```python
fm_close = content.find("\n---", 4)  # 跳过开头的 ---
before = content[:fm_close]
new_fields = f"level: {level}\ncorrection_template: \"{text}\""
new_content = before + "\n" + new_fields + content[fm_close:]
```

## level 分配经验

| 规则性质 | level | 示例 |
|---------|-------|------|
| 数学/确定性错误 | hard | 坐标除2、行号strip |
| 不可逆操作 | hard | 删除文件、覆盖铁则库 |
| 发布流程跳过 | hard | ZIP不验证、不做审计 |
| 数据安全 | hard | 自动改写铁则库 |
| 风格/表达规范 | soft | 禁止废话、禁止套话 |
| 流程缺失 | soft | 不走TDD、不跑checklist |
| 自动检测类 | monitor | 自动识别虚构、跳步骤 |
| 占位/观察类 | monitor | unknown 空壳 |
| 非规则 | meta | 偏好、开关、工作流 |

## correction_template 编写原则

- **一句话，可执行指令**（不是原则描述）
- **给出替换方案**（不仅说不要什么，要说该做什么）
- **不超过 80 字**（避免上下文膨胀）
- **monitor/meta 不强制配**

## unknown 空壳处理原则

当 unknown 规则有 hit_count 但无规则内容时：

1. 先查 `errors.jsonl` → 搜索 rule_id 匹配记录
2. 再查 `patterns.json` → 搜索条目
3. **有数据** → 从触发上下文反推规则内容，填入
4. **无数据** → 标 monitor 保留，不编造。等 Mnemonic"2次推草稿"机制下次触发时自动填充

**禁止：** 根据文件名/猜测编造规则内容。违反铁则第 1 条（禁止虚构幻觉瞎编）。

## 完成后验证

```bash
# 统计验证
python3 -c "
import os, re
for cat in ['ban','gap','lazy']:
    for f in os.listdir(f'~/.hermes/self-reflection/rules/{cat}'):
        c = open(f'~/.hermes/self-reflection/rules/{cat}/{f}').read(500)
        lv = 'level:' in c
        ct = 'correction_template:' in c
        print(f'{cat}/{f}: level={lv}, correction={ct}')
"
```

最后重建 `_index.md` 确保 level 列反映最新状态。
