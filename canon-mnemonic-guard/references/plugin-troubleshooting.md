# Plugin 存活验证诊断流程

> 创建: 2026-06-23 | 触发: 用户问"XX是不是没用"、插件列表声称已启用但无效果

## 背景

Hermes 插件有多种安装路径（`~/.hermes/plugins/` 原生 vs pip site-packages vs entry points），
且插件内部有自我降级逻辑（如 rtk-rewrite 的 `_check_rtk()` 找不到二进制就不注册 hook）。
仅凭 config.yaml 里有名字 ≠ 插件在工作。

## 诊断四步

### Step 1: 确认配置声明

```bash
grep -A 5 'plugins:' ~/.hermes/config.yaml
```

只需确认插件名在 `enabled` 列表中。

### Step 2: 确认代码存在

原生插件（~/.hermes/plugins/）：
```bash
ls ~/.hermes/plugins/<plugin-name>/src/*/__init__.py
```

pip 安装的插件：
```bash
pip3 show <package-name>
python3 -c "import <module>; print(<module>.__file__)"
```

### Step 3: 确认插件注册日志

**这是最关键的一步。** 搜 agent.log 中该插件的注册消息：
```bash
grep -i '<plugin-keyword>.*reg\|\[<plugin-tag\]' ~/.hermes/logs/agent.log | tail -5
```

三种判定：

| 日志状态 | 含义 | 动作 |
|---------|------|------|
| 有 `[xxx] registered` | ✅ 插件已注册 | 继续 Step 4 |
| 有 `[xxx] xxx not found` 等 warning | ⚠️ 注册了但降级 | 按日志提示修复前置条件 |
| **零日志** | ❌ register() 从未被调用 | 插件未被 Hermes 发现 |

### Step 4: 确认实际效果

对于 hook 类插件（pre_tool_call / transform_llm_output 等），检查是否有拦截/改写记录：
```bash
grep '\[<plugin-tag\]' ~/.hermes/logs/agent.log | wc -l
```

零条 = 插件装了但一次都没生效过。

## 实战案例：rtk-rewrite

```
Step 1: config.yaml 有 rtk-rewrite            ✅
Step 2: pip3 show rtk-hermes → 1.2.3          ✅
         which rtk → ~/.local/bin/rtk 0.42.4   ✅
Step 3: grep '[rtk]' agent.log → 零条          ❌
Step 4: grep '[rtk]' agent.log | wc -l → 0     ❌
结论: 插件从未被 Hermes 发现/调用。register()未执行。
根因推测: pip site-packages 的 entry point 不被 Hermes 扫描。
```

## 对比参照

同一会话中正常注册的插件日志格式：
```
INFO hermes_plugins.sentinel: [sentinel] v2.0.2 registered
INFO hermes_plugins.skill_autoload: [skill-autoload] plugin registered
INFO hermes_plugins.ssr: [ssr] 插件注册完成
```

这些是 Hermes 原生路径（`~/.hermes/plugins/`）的插件。pip 安装的插件没有 `hermes_plugins.` 前缀的 logger。

## 修复方向

如果 Step 3 零日志：
1. 检查 entry_points.txt 格式是否正确（`[hermes_agent.plugins]\nplugin-name = module`）
2. 检查 Hermes 的 Python 环境是否与 pip install 目标一致
3. 尝试将插件复制到 `~/.hermes/plugins/` 路径（原生格式）
4. 如无法修复 → 从 config.yaml 移除，避免占位误导
