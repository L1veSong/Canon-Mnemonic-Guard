#!/usr/bin/env python3
"""CMG Canon — 规则 frontmatter 完整性扫描脚本 v2.0
支持 meta/monitor 豁免、--rebuild-index 自动重建 _index.md。
"""
import os, re, json

RULES_DIR = os.path.expanduser("~/.hermes/self-reflection/rules")

def scan():
    results = {"ban": [], "gap": [], "lazy": []}
    for category in ["ban", "gap", "lazy"]:
        cat_dir = os.path.join(RULES_DIR, category)
        if not os.path.isdir(cat_dir):
            continue
        for fname in sorted(os.listdir(cat_dir)):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(cat_dir, fname)
            with open(fpath) as f:
                content = f.read()
            has_fm = content.startswith("---")
            level_match = re.search(r'level:\s*(\S+)', content[:500])
            has_level = bool(level_match)
            has_correction = "correction_template:" in content[:500]
            level = level_match.group(1) if level_match else "无"

            # v2.0: meta 免检, monitor 免 correction
            needs_level = not has_level
            needs_correction = not has_correction
            if level == "meta":
                needs_level = False
                needs_correction = False
            if level == "monitor":
                needs_correction = False

            results[category].append({
                "name": fname.replace(".md", ""),
                "has_frontmatter": has_fm,
                "level": level,
                "has_correction": has_correction,
                "needs_level": needs_level,
                "needs_correction": needs_correction,
                "is_ok": not needs_level and not needs_correction,
            })

    total = sum(len(v) for v in results.values())
    ok = sum(1 for v in results.values() for r in v if r["is_ok"])
    problem = total - ok

    print(f"CMG 规则 Frontmatter 扫描")
    print(f"==========================")
    print(f"总计: {total} 条")
    print(f"就绪: {ok}/{total} ({ok*100//total}%)")
    if problem:
        print(f"需修复: {problem}/{total}")
    print()

    for cat in ["ban", "gap", "lazy"]:
        items = results[cat]
        ok_cat = sum(1 for r in items if r["is_ok"])
        print(f"--- {cat.upper()} ({len(items)} 条, 就绪 {ok_cat}/{len(items)}) ---")
        for r in items:
            flags = []
            if r["needs_level"]:
                flags.append("缺level")
            if r["needs_correction"]:
                flags.append("缺correction")
            if r["level"] == "meta":
                flags.append("meta(免检)")
            if r["level"] == "monitor" and not r["has_correction"]:
                flags.append("monitor(免correction)")
            status = "⚠️ " + ",".join(flags) if flags else "✅"
            tag = " ".join(f for f in flags if f)
            print(f"  [{r['level']:8s}] {r['name'][:55]} {status}" + (f"  ({tag})" if tag else ""))

    import sys
    if "--json" in sys.argv:
        print("\n--- JSON ---")
        print(json.dumps(results, ensure_ascii=False, indent=2))
    if "--rebuild-index" in sys.argv:
        rebuild_index(results)
        print("\n✅ _index.md 已重建")

def rebuild_index(results):
    lines = [
        "# CMG 规则索引",
        "",
        f"自动生成 | {sum(len(v) for v in results.values())} 条规则 | "
        f"ban:{len(results['ban'])} / gap:{len(results['gap'])} / lazy:{len(results['lazy'])}",
        "",
        "| # | 规则 | 类型 | level | correction |",
        "|---|------|------|-------|------------|",
    ]
    i = 1
    for cat in ["ban", "gap", "lazy"]:
        for r in results[cat]:
            corr = "Y" if r["has_correction"] else "N"
            lines.append(f"| {i} | [[{r['name']}]] | {cat} | {r['level']} | {corr} |")
            i += 1
    hard = sum(1 for v in results.values() for r in v if r["level"] == "hard")
    soft = sum(1 for v in results.values() for r in v if r["level"] == "soft")
    monitor = sum(1 for v in results.values() for r in v if r["level"] == "monitor")
    meta = sum(1 for v in results.values() for r in v if r["level"] == "meta")
    with_corr = sum(1 for v in results.values() for r in v if r["has_correction"])
    lines.append("")
    lines.append(f"统计：hard:{hard} | soft:{soft} | monitor:{monitor} | meta:{meta} | correction已配:{with_corr}")
    index_path = os.path.join(RULES_DIR, "_index.md")
    with open(index_path, 'w') as f:
        f.write("\n".join(lines) + "\n")

if __name__ == "__main__":
    scan()
