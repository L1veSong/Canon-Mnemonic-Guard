# 子包自动检测安装模式

## 来源

CMG v5.4.0 发布（2026-05-25）。用户指出 CMG 外观层安装后不会自动装 guard/canon/mnemonic 三个子包，需要一键全家桶。

## 设计

在 `init.py` 的 Phase 0 增加子包检测步骤（先于目录创建），逻辑如下：

```
1. 检测 ~/.hermes/skills/software-development/<subpkg>/SKILL.md 是否存在
2. 三个全有 → 静默通过
3. 有缺失 → 显示勾选列表（默认全选），用户可输入逗号分隔的跳过名单
4. 对未跳过的子包 → os.system("npx skills add <pkg> --yes --global")
5. 安装后重新检测 → 报告结果
6. 跳过未装的 → 提示后续补装命令
```

## 关键代码模式

```python
def check_subpackages():
    """Check if sub-packages are installed. Returns {name: description} for missing."""
    sub_pkgs = {
        "guard": "Guard 护栏线 — 拦截执行 + 闭环重试",
        "canon": "Canon 典则线 — 规则生产 + 固化引擎",
        "mnemonic": "Mnemonic 忆存线 — 记忆存储 + 模式识别",
    }
    base = HERMES_HOME / "skills" / "software-development"
    missing = {}
    for pkg, desc in sub_pkgs.items():
        if not (base / pkg / "SKILL.md").exists():
            missing[pkg] = desc
    return missing

def install_subpackages(missing):
    """Prompt user to install missing sub-packages. Default: install all."""
    print(f"\n⚠️ 检测到 {len(missing)} 个子包未安装：")
    for pkg, desc in missing.items():
        print(f"  [✓] {pkg} — {desc}")
    print("\n默认全部安装。")
    print("输入要跳过的包名（逗号分隔），或直接回车全部安装：")
    skip_input = input("> ").strip()
    skip_list = [s.strip() for s in skip_input.split(",") if s.strip()] if skip_input else []
    
    for pkg in missing:
        if pkg in skip_list:
            print(f"  ⏭️ 跳过 {pkg}")
        else:
            ret = os.system(f"npx skills add {pkg} --yes --global 2>/dev/null")
            print(f"  {'✅' if ret == 0 else '❌'} {pkg}")
    
    # Re-check after install
    still_missing = check_subpackages()
    ...
```

## 设计原则

- **默认全部安装**——减少用户决策负担
- **可跳过**——不强制，灵活
- **后续自动检测**——补装后下次 init 自动感知
- **降级友好**——`2>/dev/null` + 错误提示 + 手动命令兜底
