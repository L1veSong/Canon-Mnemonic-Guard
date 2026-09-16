#!/usr/bin/env python3
"""三省引擎规则体检脚本 — 供 !review 使用：找出死规则/僵尸规则/高频规则。

用法:
    python3 review-rules.py            # 体检报告（stdout）
    python3 review-rules.py --json     # JSON 输出
    python3 review-rules.py --old 180  # 自定义「未触发」天数阈值（默认 180）

体检维度:
  1. hit_count == 0 或 last_triggered 为空        → 从未触发的规则（可能是需求不存在）
  2. last_triggered 距今 > 阈值                     → 死规则（可能过时）
  3. false_positives / hit_count > 30%              → 误报高的规则（建议降级 monitor）
  4. top hit_count                                 → 高频规则（最有效，值得保留）

2026-09-07 创建。与 rebuild-index.py 同目录。
"""
import os
import sys
import glob
import json
from datetime import datetime, date

RULES_DIR = os.path.expanduser('~/.hermes/self-reflection/rules')
CATS = ['ban', 'gap', 'lazy', 'meta']


def load_rules():
    rules = []
    for cat in CATS:
        for f in sorted(glob.glob(os.path.join(RULES_DIR, cat, '*.md'))):
            name = os.path.basename(f)[:-3]
            try:
                import yaml
                parts = open(f).read().split('---')
                fm = yaml.safe_load(parts[1]) if len(parts) >= 3 else {}
            except Exception as e:
                fm = {'parse_error': str(e)}
            kw_vals = fm.get('keywords') or []
            rules.append({
                'name': name, 'cat': cat,
                'date': str(fm.get('date', '')),
                'hit': int(fm.get('hit_count') or 0),
                'last': str(fm.get('last_triggered') or ''),
                'fp': int(fm.get('false_positives') or 0),
                'level': str(fm.get('level', '')),
                'kw': len(kw_vals),
                'kw_list': list(kw_vals),
            })
    return rules


def days_since(s):
    if not s:
        return None
    try:
        d = datetime.fromisoformat(s.replace('Z', '+00:00')).date()
    except Exception:
        try:
            d = datetime.strptime(s[:10], '%Y-%m-%d').date()
        except Exception:
            return None
    return (date.today() - d).days


def find_wide_keywords(rules):
    """检测可能误杀的宽泛关键词（纯英文裸词 / 二字中文词 / 高频通用词）。

    sentinel 关键词为子串/正则匹配，裸词（如 dashboard、开发、验证）会在
    正常对话中被误杀（2026-09-07 实测：讨论 Dashboard 状态命中 ban 规则）。
    此检测输出候选，由人工判断是否改为行为短语；不自动修改。
    """
    import re
    # 通用高频词（英文小写），出现在 keywords 中高度可疑
    GENERIC_EN = {
        'dashboard', 'dev', 'ui', 'css', 'html', 'ok', 'ai', 'use', 'open',
        'write', 'new', 'file', 'path', 'data', 'app', 'web', 'task', 'test',
        'api', 'key', 'click', 'word', 'view', 'run', 'code', 'msg',
    }
    GENERIC_ZH2 = {
        '验证', '假设', '开发', '迁移', '改名', '发布', '打包', '搜索', '测试',
        '检查', '修改', '删除', '复制', '替换', '重新', '部分', '全部', '版本',
        '历史', '上传', '下载', '完整', '使用', '期间', '应该', '可能', '大概',
    }
    out = []
    for r in rules:
        for k in r['kw_list']:
            ks = str(k)
            low = ks.lower()
            if re.fullmatch(r'[a-z0-9_\-]{1,8}', low) and low in GENERIC_EN:
                out.append((r['cat'], r['name'], ks, 'EN裸词'))
            elif re.fullmatch(r'[\u4e00-\u9fff]{2}', ks) and ks in GENERIC_ZH2:
                out.append((r['cat'], r['name'], ks, '2字宽词'))
    return out


def review(rules, old_threshold=180):
    never = [r for r in rules if r['hit'] == 0 and not r['last']]
    dead = []
    fp_high = []
    for r in rules:
        ds = days_since(r['last'])
        if ds is not None and ds > old_threshold:
            dead.append((ds, r))
        if r['hit'] > 0 and r['fp'] / r['hit'] > 0.3:
            fp_high.append(r)
    top = sorted(rules, key=lambda r: -r['hit'])[:8]
    return {'never': never, 'dead': dead, 'fp_high': fp_high, 'top': top}


def main():
    args = sys.argv[1:]
    old_threshold = 180
    if '--old' in args:
        try:
            old_threshold = int(args[args.index('--old') + 1])
        except Exception:
            pass
    rules = load_rules()
    rv = review(rules, old_threshold)
    wide = find_wide_keywords(rules)
    as_json = '--json' in args

    if as_json:
        def slim(items):
            return [{'name': x['name'], 'cat': x['cat'], 'hit': x['hit'], 'last': x['last'], 'fp': x['fp']} for x in items]
        out = {
            'total': len(rules), 'old_threshold': old_threshold,
            'never': slim(rv['never']),
            'dead': [{'name': x[1]['name'], 'cat': x[1]['cat'], 'days': x[0]} for x in rv['dead']],
            'fp_high': slim(rv['fp_high']),
            'top': slim(rv['top']),
            'wide_keywords': [{'cat': x[0], 'name': x[1], 'keyword': x[2], 'type': x[3]} for x in wide],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    print('=' * 50)
    print('三省引擎 · 规则体检报告  (%d 条)' % len(rules))
    print('=' * 50)
    print('\n[1] 从未触发 (%d 条):' % len(rv['never']))
    for r in rv['never']:
        print('  - %s/%s  (level=%s)' % (r['cat'], r['name'], r['level'] or '-'))
    print('\n[2] 超过 %d 天未触发 (%d 条):' % (old_threshold, len(rv['dead'])))
    for ds, r in sorted(rv['dead'], reverse=True):
        print('  - %4d 天  %s/%s' % (ds, r['cat'], r['name']))
    print('\n[3] 误报率 > 30%% (%d 条):' % len(rv['fp_high']))
    for r in rv['fp_high']:
        print('  - %s/%s  hit=%d fp=%d' % (r['cat'], r['name'], r['hit'], r['fp']))
    print('\n[4] TOP 高频规则 (最有价值):')
    for r in rv['top']:
        print('  - %-8s %s  hit=%d  last=%s' % (r['cat'], r['name'], r['hit'], r['last'] or '-'))
    print('\n[5] 宽泛关键词候选 (可能导致误杀, 建议改为行为短语):')
    if wide:
        for cat, name, kw, typ in wide:
            print('  - %s/%s  %s (%s)' % (cat, name, kw, typ))
    else:
        print('  - 无')
    print('\n建议: [3] 降级 monitor；[1][2] 需求消失则归档 dead/；[4] 保留；[5] 人工确认是否精确化。')
    print('归档操作: mv rules/<cat>/<name>.md rules/dead/\n')


if __name__ == '__main__':
    main()
