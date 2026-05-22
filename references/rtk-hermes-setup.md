# rtk-hermes 安装与配置

> CMG 成本优化推荐配套。压缩终端输出 60-90% token。被动受益——不影响 CMG 功能范围。

## 组件

| 组件 | 说明 | 安装方式 |
|------|------|---------|
| `rtk` 二进制 | 实际执行命令重写的 Rust 二进制 | GitHub Releases 直链下载（brew 可能卡队列） |
| `rtk-hermes` pip 包 | Hermes 插件桥接层 | pip install 到 Hermes venv |

## 安装流程

### 1. 安装 rtk 二进制

```bash
# M1/M2/M3 Mac (aarch64):
curl -sL "https://github.com/rtk-ai/rtk/releases/latest/download/rtk-aarch64-apple-darwin.tar.gz" -o /tmp/rtk.tar.gz
tar xzf /tmp/rtk.tar.gz -C /tmp
cp /tmp/rtk ~/.local/bin/rtk
chmod +x ~/.local/bin/rtk

# 验证:
rtk --version
```

**坑：** `brew install rtk` 在 TUNA 镜像下可能排队长达数百位，超时失败。直链下载 2 秒完成。

### 2. 安装 rtk-hermes pip 包

```bash
# Hermes venv 的 pip 可能缺失——先 ensurepip:
~/.hermes/hermes-agent/venv/bin/python -m ensurepip

# 安装（从 GitHub 或本地克隆）:
~/.hermes/hermes-agent/venv/bin/python -m pip install rtk-hermes
```

### 3. 配置 Hermes

```yaml
# ~/.hermes/config.yaml
plugins:
- name: rtk-rewrite    # ⚠️ 是 rtk-rewrite，不是 rtk-hermes！
  enabled: true
```

**坑：** pip 包名是 `rtk-hermes`，但 Hermes entry point 名是 `rtk-rewrite`。config.yaml 必须用 entry point 名，否则 Hermes 找不到插件。当前会话安装后需重启 gateway 才能在新会话生效。

### 4. 重启

```bash
hermes gateway restart
```

**注意：** 插件在当前会话不生效（会话启动时加载）。下个新聊天自动启用。

## 验证

```bash
# rtk 功能:
rtk rewrite "git status"     # 应输出: rtk git status
rtk rewrite "ls -la"          # 应输出: rtk ls -la

# 插件状态（新会话中）:
/rtk status
```

## 环境变量（可选）

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `RTK_HERMES_MODE` | `rewrite` | `rewrite` / `suggest` / `off` |
| `RTK_HERMES_TIMEOUT_MS` | `2000` | 重写超时（毫秒） |
| `RTK_HERMES_BACKENDS` | `local` | 启用的终端后端，逗号分隔；`all` 全部启用 |

## 坑点汇总

1. **Config 名称不匹配：** pip 包名 `rtk-hermes` ≠ entry point 名 `rtk-rewrite`。config 必须用后者。
2. **brew 卡队列：** TUNA 镜像下 `brew install rtk` 可能超时。直接 GitHub Releases 下载二进制。
3. **Hermes venv 无 pip：** 需要 `python -m ensurepip` 先装 pip。
4. **会话级加载：** 安装后必须重启 gateway + 新会话才生效。当前会话看不到。
5. **`hermes plugins list` 不显示：** 该命令只列出 repo-managed 插件。pip entry-point 插件通过 `hermes_agent.plugins` 自动发现，不在列表中。
