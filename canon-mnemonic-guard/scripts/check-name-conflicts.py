#!/usr/bin/env python3
"""
CMG Name Conflict Checker v1.0.0
Scans all installed skills for name collisions with CMG's four core skills.
Usage: python3 check-name-conflicts.py [--fix] [--quiet]
"""
import os, re, sys, glob
from pathlib import Path

HERMES_HOME = Path(os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes")))
AGENTS_HOME = Path(os.path.expanduser("~/.agents"))

CMG_NAMES = {"canon", "guard", "mnemonic", "canon-mnemonic-guard"}
CMG_BASE = HERMES_HOME / "skills" / "software-development"


def parse_skill(filepath):
    """Parse name: from SKILL.md frontmatter."""
    try:
        with open(filepath) as f:
            content = f.read()
        m = re.search(r'^name:\s*(.+)$', content, re.MULTILINE)
        return m.group(1).strip() if m else None
    except Exception:
        return None


def scan_all_skills():
    """Scan all SKILL.md files, return {name: [paths]}."""
    name_map = {}
    for base in [HERMES_HOME / "skills", AGENTS_HOME / "skills"]:
        if not base.exists():
            continue
        for f in glob.glob(f"{base}/**/SKILL.md", recursive=True):
            name = parse_skill(f)
            if name:
                name_map.setdefault(name, []).append(f)
    return name_map


def find_conflicts(name_map):
    """Find CMG name conflicts. Returns list of (cmg_name, cmg_path, other_paths)."""
    conflicts = []
    for name in CMG_NAMES:
        paths = name_map.get(name, [])
        cmg_paths = [p for p in paths if str(CMG_BASE / name) in p]
        other_paths = [p for p in paths if p not in cmg_paths]
        if cmg_paths and other_paths:
            conflicts.append((name, cmg_paths[0], other_paths))
    return conflicts


def rename_skill(filepath, new_name):
    """Change name: field in SKILL.md."""
    with open(filepath) as f:
        content = f.read()
    content = re.sub(r'^name:\s*.+$', f'name: {new_name}', content, count=1, flags=re.MULTILINE)
    with open(filepath, "w") as f:
        f.write(content)
    return True


def update_cmg_refs(old_name, new_name):
    """Update related_skills references in all four CMG packs."""
    packs = ["canon", "guard", "mnemonic", "canon-mnemonic-guard"]
    for pkg in packs:
        skill_file = CMG_BASE / pkg / "SKILL.md"
        if not skill_file.exists():
            # Try without software-development prefix
            skill_file = HERMES_HOME / "skills" / pkg / "SKILL.md"
            if not skill_file.exists():
                continue
        with open(skill_file) as f:
            content = f.read()
        content = content.replace(f"related_skills: [{old_name},", f"related_skills: [{new_name},")
        content = content.replace(f"related_skills: [canon, {old_name},", f"related_skills: [canon, {new_name},")
        content = content.replace(f", {old_name},", f", {new_name},")
        content = content.replace(f", {old_name}]", f", {new_name}]")
        with open(skill_file, "w") as f:
            f.write(content)
        print(f"    已更新引用: {skill_file}")


def resolve_conflict_interactive(name, cmg_path, other_paths):
    """Interactive conflict resolution."""
    print(f"\n{'='*60}")
    print(f"⚠️ 检测到 skill 名称冲突: {name}")
    print(f"{'='*60}")
    print(f"\n  CMG/{name}  → {cmg_path}")
    print(f"  第三方       →")
    for p in other_paths:
        print(f"    {p}")
    
    source = "gstack" if "gstack" in str(other_paths[0]) else "第三方"
    new_other_name = f"{source}-{name}" if source != "第三方" else f"external-{name}"
    new_cmg_name = f"cmg-{name}"
    
    print(f"\n原因: 同名 skill 会导致 Hermes 加载歧义，任选一个改名即可解决。\n")
    print(f"A) 将 {source} 改名为 {new_other_name}（推荐，不影响功能）")
    print(f"B) 将 CMG/{name} 改名为 {new_cmg_name}（需同步更新四包引用）")
    print(f"C) 两者都改")
    print(f"D) 跳过，手动处理")
    print()
    
    choice = input("选择 [A]: ").strip().upper() or "A"
    
    if choice == "A":
        for p in other_paths:
            rename_skill(p, new_other_name)
            print(f"  ✅ {os.path.basename(os.path.dirname(p))} → {new_other_name}")
        return True
    elif choice == "B":
        rename_skill(cmg_path, new_cmg_name)
        print(f"  ✅ CMG/{name} → {new_cmg_name}")
        update_cmg_refs(name, new_cmg_name)
        return True
    elif choice == "C":
        for p in other_paths:
            rename_skill(p, new_other_name)
        rename_skill(cmg_path, new_cmg_name)
        update_cmg_refs(name, new_cmg_name)
        print(f"  ✅ 双方已改名")
        return True
    elif choice == "D":
        print(f"  ⏭️ 已跳过。后续可手动处理或重跑 init.py。")
        return False
    else:
        print(f"  无效选项，跳过。")
        return False


def auto_report(name_map):
    """Non-interactive: just report conflicts."""
    conflicts = find_conflicts(name_map)
    if not conflicts:
        print("✅ CMG 四名无冲突")
        return True, []
    print(f"⚠️ 发现 {len(conflicts)} 个冲突:")
    for name, cmg_path, other_paths in conflicts:
        print(f"  {name}: CMG ←→ {[os.path.basename(os.path.dirname(p)) for p in other_paths]}")
    return False, conflicts


def main():
    args = sys.argv[1:]
    interactive = "--fix" in args
    quiet = "--quiet" in args
    
    name_map = scan_all_skills()
    conflicts = find_conflicts(name_map)
    
    if not conflicts:
        if not quiet:
            print("✅ CMG 四名无冲突 (canon/guard/mnemonic/canon-mnemonic-guard)")
        return True
    
    if not interactive:
        if not quiet:
            print(f"⚠️ 发现 {len(conflicts)} 个冲突:")
            for name, cmg_path, other_paths in conflicts:
                print(f"  {name}:")
                print(f"    CMG → {cmg_path}")
                for p in other_paths:
                    print(f"    冲突 → {p}")
            print(f"\n运行 python3 {__file__} --fix 进入交互式修复。")
        return False
    
    for name, cmg_path, other_paths in conflicts:
        resolve_conflict_interactive(name, cmg_path, other_paths)
    
    # Re-scan
    name_map = scan_all_skills()
    conflicts = find_conflicts(name_map)
    if not conflicts:
        print("\n✅ 全部冲突已解决。")
        return True
    else:
        print(f"\n⚠️ 仍有 {len(conflicts)} 个冲突未解决。")
        return False


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
