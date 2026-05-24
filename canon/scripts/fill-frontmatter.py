#!/usr/bin/env python3
"""Batch-fill missing level + correction_template in CMG rule frontmatter.

Three-step workflow (from 2026-05-25 session):
  1. Classify: scan all rules, separate 'real rules' from 'meta configs'
  2. Fill: add level + correction_template in batches (5-8 per batch)
  3. Rebuild: regenerate _index.md

Usage:
  python3 fill-frontmatter.py --dry-run          # Preview changes
  python3 fill-frontmatter.py --all              # Fill all at once
  python3 fill-frontmatter.py --rebuild-index    # Rebuild _index.md only

Level inference rules (edit these if your convention changes):
  hard:  coordinate errors, file corruption, data loss, version skew, fabrication
  soft:  style preferences, heuristic suggestions
  monitor: auto-detected patterns, unknown triggers
  meta:  user preferences, system flow configs (skip these entirely)
"""

import os, sys, re
from pathlib import Path

RULES_DIR = Path.home() / ".hermes/self-reflection/rules"

LEVEL_RULES = [
    (["坐标", "除2", "retina", "pyautogui", "hotkey", "行号污染",
      "ZIP不验证", "不查全包", "全量审计", "RED失败", "打包遗漏",
      "版本号变更", "全文件同步", "幻觉", "瞎编", "编造", "虚构",
      "铁则库", "自动归档", "联网搜索", "金融子Agent", "纠错必须固化",
      "不加载.*skill", "不用专业skill", "Darwin过度精简", "write_file清空",
      "cmg-declaration", "extra-click", "single-click", "window-position",
      "ocr-wechat", "incomplete-readme", "changelog.*gaps", "version.*skip"],
     "hard"),
    (["企业化套路", "废话开头", "女娲.*审查", "灵感来源.*依赖",
      "iMessage.*手机号", "不走TDD", "不跑checklist", "跳步骤偷懒摆烂"],
     "soft"),
    (["自动识别", "关键词匹配", "unknown"],
     "monitor"),
    (["热记忆", "记忆查询", "完全自动化", "智能技能调度", "思考模式"],
     "meta"),
]

DEFAULT_CORRECTIONS = {
    "hard": "你的回答违反了规则。请根据规则内容修正后重新生成。",
}


def infer_level(filename: str, content: str) -> str:
    text = filename + " " + content[:500]
    for keywords, level in LEVEL_RULES:
        for kw in keywords:
            if re.search(kw, text, re.IGNORECASE):
                return level
    return "soft"


def fill_frontmatter(fpath: Path, level: str, correction: str, dry_run: bool = False) -> bool:
    content = fpath.read_text()
    if not content.startswith("---"):
        return False
    fm_close = content.find("\n---", 4)
    if fm_close == -1:
        return False
    if "level:" in content[:fm_close]:
        return False  # already has level
    
    before = content[:fm_close]
    after = content[fm_close:]
    lines = [f"level: {level}"]
    if correction and level != "monitor" and level != "meta":
        lines.append(f'correction_template: "{correction}"')
    new_content = before + "\n" + "\n".join(lines) + after
    
    if dry_run:
        print(f"  DRY-RUN: {fpath.name} → level={level}")
        return True
    fpath.write_text(new_content)
    print(f"  ✅ {fpath.name} → level={level}")
    return True


def rebuild_index():
    entries = []
    for category in ["ban", "gap", "lazy"]:
        cat_dir = RULES_DIR / category
        if not cat_dir.is_dir():
            continue
        for fpath in sorted(cat_dir.glob("*.md")):
            content = fpath.read_text()
            level = "待定"; correction = "N"
            if content.startswith("---"):
                fm_end = content.find("\n---\n", 3)
                if fm_end > 0:
                    fm = content[3:fm_end]
                    lm = re.search(r'level:\s*(\S+)', fm)
                    if lm: level = lm.group(1)
                    if 'correction_template:' in fm: correction = "Y"
            entries.append({"category": category, "name": fpath.stem, "level": level, "correction": correction})
    
    lines = ["# CMG 规则索引\n"]
    total = len(entries)
    lines.append(f"自动生成 | {total} 条规则\n")
    lines.append("| # | 规则 | 类型 | level | correction |")
    lines.append("|---|------|------|-------|------------|")
    for i, e in enumerate(entries, 1):
        lines.append(f"| {i} | [[{e['name']}]] | {e['category']} | {e['level']} | {e['correction']} |")
    
    hard = sum(1 for e in entries if e['level'] == 'hard')
    soft = sum(1 for e in entries if e['level'] == 'soft')
    monitor = sum(1 for e in entries if e['level'] == 'monitor')
    meta = sum(1 for e in entries if e['level'] == 'meta')
    pending = sum(1 for e in entries if e['level'] == '待定')
    with_c = sum(1 for e in entries if e['correction'] == 'Y')
    lines.append(f"\n统计：hard:{hard} | soft:{soft} | monitor:{monitor} | meta:{meta} | 待定:{pending} | correction已配:{with_c}")
    
    (RULES_DIR / "_index.md").write_text("\n".join(lines))
    print(f"✅ _index.md rebuilt: {total} rules")


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--rebuild-index", action="store_true")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()
    
    if args.rebuild_index:
        rebuild_index()
        return
    
    if not RULES_DIR.is_dir():
        print(f"ERROR: {RULES_DIR} not found")
        sys.exit(1)
    
    filled = 0
    for category in ["ban", "gap", "lazy"]:
        cat_dir = RULES_DIR / category
        if not cat_dir.is_dir():
            continue
        for fpath in sorted(cat_dir.glob("*.md")):
            content = fpath.read_text()
            level = infer_level(fpath.name, content)
            if level == "meta":
                print(f"  SKIP {fpath.name} (meta)")
                continue
            correction = DEFAULT_CORRECTIONS.get(level, "")
            if fill_frontmatter(fpath, level, correction, dry_run=args.dry_run):
                filled += 1
    
    if filled > 0 and not args.dry_run:
        print(f"\n✅ Filled {filled} rules. Run --rebuild-index next.")
    elif args.dry_run:
        print(f"\n📋 Would fill {filled} rules.")
    else:
        print("\n✅ All rules already have level.")


if __name__ == "__main__":
    sys.exit(main() or 0)
