# 推荐列表配置 Schema

> config.json 中 `recommendations` 和 `companions` 字段的完整规范。

## recommendations（联动推荐）

已安装且与 CMG 有实际数据交互的工具。每项必须验证过。

```json
{
  "recommendations": {
    "version": "1.0.0",
    "last_scan": "ISO8601",
    "auto_prompt": true,
    "items": [
      {
        "name": "rtk-rewrite",
        "type": "plugin",
        "detection_method": "entry_point",
        "detection_group": "hermes_agent.plugins",
        "detection_name": "rtk-rewrite",
        "integration": "被动受益。rtk压缩所有Hermes终端输出",
        "category": "cost",
        "configured": false
      }
    ]
  }
}
```

### type 枚举

| type | detection 方式 | 示例 |
|------|---------------|------|
| `skill` | 检查 `detection_path` 文件是否存在 | ralph-loop |
| `plugin` | 检查 pip entry points (`detection_group` + `detection_name`) | rtk-rewrite |
| `mcp_server` | 检查 `detection_path` 目录是否存在 | plur |

### 准入标准

1. **已验证交互** — 数据确实流过，不能是概念联动
2. **自动感知** — CMG 无需额外配置即可发现
3. **互补非重叠** — 提供 CMG 不具备的能力

## pending_tests（待测清单）

联动已设计但因缺少真实数据未验证的工具。

```json
{
  "pending_tests": {
    "checklist": "path/to/integration-test-checklist.md",
    "items": ["ralph-loop", "verification-before-completion", "diagnose"],
    "description": "联动已设计，待Guard积累真实拦截数据后验证"
  }
}
```

验证通过后 → 移入 recommendations。验证失败 → 移入 companions 或移除。

## companions（建议配套）

独立使用但与 CMG 理念互补的工具。CMG 不调用它们，用户自行使用。

```json
{
  "companions": {
    "description": "建议配套安装（独立使用，非 CMG 联动）",
    "items": [
      {
        "name": "obsidian",
        "type": "skill",
        "detection_path": "...",
        "integration": "rules/可视化浏览+全文检索",
        "category": "shared"
      }
    ]
  }
}
```

## 三层结构决策树

```
装了 CMG → 检测到新工具
  ├── 有实际数据交互 + 已验证？ → recommendations
  ├── 设计上能联动但没数据？     → pending_tests
  └── 独立使用、理念互补？       → companions
```
