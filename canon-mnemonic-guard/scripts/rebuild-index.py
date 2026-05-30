#!/usr/bin/env python3
"""CMG _index.md 重建脚本 — 扫描 rules/ 目录，生成规则索引表格。

用法:
    python3 rebuild-index.py                     # 重建当前 _index.md
    python3 rebuild-index.py --dry-run           # 仅预览不写入
    python3 rebuild-index.py --check             # 仅检查一致性（退出码 0=一致, 1=漂移）

每次固化后建议运行此脚本，确保 _index.md 与实际文件数一致。
CMG v5.5.5+ diagnose Phase 2 会检测漂移。
"""

import os
import sys
import glob
from datetime import datetime

RULES_DIR = os.path.expanduser('~/.hermes/self-reflection/rules')


def collect_rules():
    """扫描 rules/ 目录，返回规则列表 [(cat, name, level, has_correction), ...]"""
    rules = []
    for cat in ['ban', 'gap', 'lazy']:
        pattern = os.path.join(RULES_DIR, cat, '*.md')
        for f in sorted(glob.glob(pattern)):
            name = os.path.splitext(os.path.basename(f))[0]
            level = '?'
            has_correction = 'N'
            try:
                import yaml
                with open(f) as fh:
                    content = fh.read()
                parts = content.split('---')
                if len(parts) >= 3:
                    fm = yaml.safe_load(parts[1])
                    if fm:
                        level = fm.get('level', '?')
                        has_correction = 'Y' if fm.get('correction_template') else 'N'
            except Exception as e:
                print(f'⚠️  {f}: YAML 解析失败 ({e})', file=sys.stderr)
            rules.append((cat, name, level, has_correction))
    return rules


def build_index(rules):
    """生成 _index.md 内容"""
    ban_count = sum(1 for r in rules if r[0] == 'ban')
    gap_count = sum(1 for r in rules if r[0] == 'gap')
    lazy_count = sum(1 for r in rules if r[0] == 'lazy')
    total = len(rules)

    lines = [
        '# CMG 规则索引',
        '',
        f'自动生成 | {total} 条规则 | ban:{ban_count} / gap:{gap_count} / lazy:{lazy_count}',
        '',
        '| # | 规则 | 类型 | level | correction |',
        '|---|------|------|-------|------------|',
    ]

    for i, (cat, name, level, corr) in enumerate(rules, 1):
        lines.append(f'| {i} | [[{name}]] | {cat} | {level} | {corr} |')

    lines.append('')
    return '\n'.join(lines)


def count_existing_table_rows(index_path):
    """统计已有 _index.md 的表格行数"""
    if not os.path.exists(index_path):
        return 0
    count = 0
    with open(index_path) as f:
        for line in f:
            if line.startswith('| ') and '[[' in line and ']]' in line:
                count += 1
    return count


def main():
    dry_run = '--dry-run' in sys.argv
    check_only = '--check' in sys.argv

    rules = collect_rules()
    if not rules:
        print('❌ 未找到任何规则文件', file=sys.stderr)
        sys.exit(1)

    content = build_index(rules)
    index_path = os.path.join(RULES_DIR, '_index.md')

    if check_only:
        existing_rows = count_existing_table_rows(index_path)
        if existing_rows == len(rules):
            print(f'✅ _index.md 一致: {len(rules)} 条规则')
            sys.exit(0)
        else:
            print(f'⚠️  漂移: _index.md 有 {existing_rows} 行, rules/ 有 {len(rules)} 条', file=sys.stderr)
            sys.exit(1)

    if dry_run:
        print(content)
        print(f'\n--- 预览: {len(rules)} 条规则 (ban:{sum(1 for r in rules if r[0]=="ban")} gap:{sum(1 for r in rules if r[0]=="gap")} lazy:{sum(1 for r in rules if r[0]=="lazy")}) ---')
    else:
        with open(index_path, 'w') as f:
            f.write(content)
        print(f'✅ _index.md 已写入: {index_path}')
        print(f'   {len(rules)} 条规则 (ban:{sum(1 for r in rules if r[0]=="ban")} gap:{sum(1 for r in rules if r[0]=="gap")} lazy:{sum(1 for r in rules if r[0]=="lazy")})')


if __name__ == '__main__':
    main()
