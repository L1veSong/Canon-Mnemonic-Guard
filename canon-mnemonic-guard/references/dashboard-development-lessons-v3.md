# Dashboard v5.6.0 — 开发教训与自适应性改进

> 日期: 2026-06-14 | 基线: Dashboard v1.0.0 → v5.6.0

## 七条 Bug 与修复

| # | Bug | 根因 | 修复 |
|---|-----|------|------|
| 1 | 配置读写用旧 key `cmg_guard` | sentinel 改名未同步 | read/write_config → SENTINEL_KEY 自动检测 |
| 2 | 版本号显示 v5.5.5 | 硬编码在 HTML 模板 | 从 SKILL.md frontmatter 动态读取 |
| 3 | "近30天无拦截记录"硬编码 | 无数据驱动 | items.length ? '' : i18n 消息 |
| 4 | 趋势图空白 | 时区不匹配(naive vs UTC-aware datetime 相减抛 TypeError→被 except 吞) | dt.tzinfo=None 时补 UTC + fallback 到 'ts' 字段 |
| 5 | 趋势图模糊 | Retina 屏 Canvas 未做 DPR 缩放 | canvas.width/height × dpr + ctx.scale(dpr) |
| 6 | 英文残留中文(导出/批量/主题按钮) | 两套按钮 HTML 未加 data-i18n + JS textContent 直接覆写 | 全部改用 t() + data-i18n 属性 |
| 7 | 统计卡片换行 | "Prohibited 60 · Missing 4 · Lazy 3" 超宽 | white-space:nowrap + overflow:hidden + text-overflow:ellipsis |

## 自适应性改进

### 版本号
```python
def _cmg_version():
    with open(CMG_SKILL_PATH) as f:
        for line in f:
            if line.startswith('version:'):
                return line.split(':',1)[1].strip()
    return '?.?.?'
CMG_VERSION = _cmg_version()
```

### 配置 Key
```python
def _sentinel_config_key():
    py = os.path.expanduser('~/.hermes/plugins/sentinel/plugin.yaml')
    if os.path.exists(py):
        d = yaml.safe_load(open(py)) or {}
        return d.get('name', 'sentinel')
    return 'sentinel'
SENTINEL_KEY = _sentinel_config_key()
```

### i18n CJK 审计
切英文后自动扫描页面，发现汉字元素→红框标记 `⚠ Untranslated`：

```javascript
function auditI18n() {
  document.querySelectorAll('[data-i18n]').forEach(function(el){
    if (el.dataset.i18nAudited) return;
    var txt = el.textContent.trim();
    if (txt && /[\u4e00-\u9fff]/.test(txt) && currentLang === 'en') {
      el.style.outline = '2px dashed #f85149';
      el.title = '⚠ Untranslated: ' + el.getAttribute('data-i18n');
      el.dataset.i18nAudited = '1';
    }
  });
}
```

调用时机：`switchLang()` → `applyLang()` → `setTimeout(auditI18n, 500)`

## 备份铁律

**修改 `server.py` 前必须备份：**
```bash
cp ~/.hermes/dashboard/server.py ~/.hermes/dashboard/server.py.bak.$(date +%Y%m%d_%H%M%S)
```

本会话实战教训：execute_code 多次调用互踩，文件被清空为 0 字节。幸好有 `server.py.bak5` 备份可恢复。

备份文件位于 `~/.hermes/dashboard/server.py.bak*`。
