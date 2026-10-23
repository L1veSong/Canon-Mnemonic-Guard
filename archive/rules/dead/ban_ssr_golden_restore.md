---type: ban
id: ban_ssr_golden_restore
date: 2026-07-24
keywords:
- a_rules.json
- golden
- 恢复
- 覆盖
- 替换
- cp.*a_rules
- write_file.*a_rules
- SSR.*restore
- golden.*backup
tags:
- ssr
- data-safety
superseded: rule_ban_no_delete_a_rules
superseded_date: '2026-09-07'
---

# 禁止覆盖 a_rules.json

禁止用 backup 文件覆盖 `a_rules.json`。

- 禁止 `cp <backup> a_rules.json`
- 禁止 `write_file(path='...a_rules.json')` 写入备份内容
- 禁止 execute_code 中 `os.system("cp ... a_rules.json")`

修改 a_rules.json 必须走增量路径（python dict update），不能全量替换。

备份文件可以保留作为参考，但只能人工手动恢复，AI 不得执行。
