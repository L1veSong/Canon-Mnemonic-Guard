#!/usr/bin/env python3
"""sentinel 契约回归测试 — 每次 Hermes 升级后运行。

背景: 2026-09-15 审计发现 pre_tool_call 返回值契约在 Hermes 升级后静默失配
(旧 {"block": True} 被核心忽略)，"改文件防线"从未生效。此测试锁住契约与关键行为。

运行: python3 ~/.hermes/plugins/sentinel/tests/test_contract.py
"""
import importlib.util, os, sys

SENTINEL = os.path.expanduser("~/.hermes/plugins/sentinel/__init__.py")


def load():
    spec = importlib.util.spec_from_file_location("sentinel_contract", SENTINEL)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    # 掐掉一切写盘副作用
    m._log_intercept = lambda *a, **k: None
    m._record_correction = lambda p: 1
    m._maybe_add_to_blacklist = lambda *a: None
    return m


def main():
    m = load()
    fails = []

    def check(name, cond):
        print(("PASS " if cond else "FAIL ") + name)
        if not cond:
            fails.append(name)

    # 1) pre_tool_call 契约（用内核 v0.21 真实载荷形态：tool_name=/args=/全字段）
    def core_call(tool, targs):
        return m._pre_tool_call(tool_name=tool, args=targs, task_id="t1", session_id="s1",
                                tool_call_id="c1", turn_id="r1", api_request_id="a1", middleware_trace=[])
    r = core_call("write_file", {"path": os.path.expanduser("~/.hermes/skills/x/SKILL.md")})
    check("skill 写入门(内核载荷): action=block + message", isinstance(r, dict) and r.get("action") == "block" and r.get("message"))
    check("skill 写入门: 无旧 block 键", not (isinstance(r, dict) and "block" in r))
    check("非 skill 路径放行", core_call("write_file", {"path": "/tmp/not_a_skill_path.txt"}) is None)
    r = core_call("terminal", {"command": "echo x >> ~/.hermes/skills/a/b.md"})
    check("terminal 写 skill 拦截", isinstance(r, dict) and r.get("action") == "block")
    r = core_call("write_file", {"path": os.path.expanduser("~/Desktop/x.txt")})
    check("Desktop path_guard 拦截", isinstance(r, dict) and r.get("action") == "block")
    g = m._behavior_path_guard("terminal", {"command": "ls ~/Desktop/x 2>&1 | head"})
    check("path_guard 不误伤 2>&1 只读命令", g is None)
    g = m._behavior_path_guard("terminal", {"command": "echo x > ~/Desktop/a.txt"})
    check("path_guard 拦桌面写入命令", isinstance(g, dict) and g.get("action") == "block")
    check("旧位置参数形态兼容", m._pre_tool_call("write_file", {"path": "/tmp/legacy.txt"}) is None)

    # 2) 纠错检测器
    check("IMPORTANT 系统消息豁免", m._scan_user_message('[IMPORTANT: The user has invoked the "x" skill]') is None)
    check("普通提问不触发", m._scan_user_message("我觉得意义不大吧，你测一下") is None)
    check("真纠错仍触发", m._scan_user_message("你又偷懒了") is not None)

    # 3) 词表基准（历史误伤语料放行 + 真违规命中）
    for t in ["我不会瞎编数据的。", "规则库的结构怎么设计？", "明文条款写清楚。", "restore 命令怎么用？",
              "版本号和 CHANGELOG 核对一下。", "隐私政策更新了。", "那边说今天下午有雨。"]:
        check("放行: " + t, m._scan_text(t) is None)
    for t in ["请使用 skill_manage(action='patch') 操作 skill。", "文档自动归档到备份区是常见做法。", "建议不要再犯类似问题。", "备份文件后重试。"]:
        check("放行(正常语料): " + t, m._scan_text(t) is None)
    for t in ["我瞎编了一个安装结果。", "记进规则库。", "密钥是 abcdef", "changelog没更新就发了。"]:
        check("命中: " + t, m._scan_text(t) is not None)

    print()
    if fails:
        print(f"FAIL {len(fails)} 项 — 契约可能再次漂移，检查 Hermes 版本与插件返回值格式")
        sys.exit(1)
    print("全部通过 — 契约正常")


if __name__ == "__main__":
    main()
