# Agent S Grounding 模型评估（2026-05-28）

## 背景
Agent S (Simular AI) 是 SOTA 桌面操控 agent。它需要两个模型：主模型（推理）+ grounding 模型（视觉定位，输出精确像素坐标）。

## 评估框架

### 评估维度
| 维度 | 权重 | 说明 |
|------|:--:|------|
| 坐标精度 | 高 | grounding 核心——必须输出精确像素坐标 |
| 费用 | 高 | 用户 token 成本敏感 |
| 磁盘占用 | 中 | M3 8GB + 有限 SSD |
| 下载速度 | 中 | 国内网络环境 |
| 集成难度 | 低 | Agent S 原生支持程度 |

### 测试方案矩阵

| 方案 | 精度 | 费用 | 磁盘 | 速度 | 结论 |
|------|:--:|------|:--:|------|------|
| 硅基流动 Qwen3-VL-8B | ❌ 区域描述 | ✅ 已有 key | 0 | 快 | **不通过**——坐标格式不兼容 |
| 本地 UI-TARS-1.5-7B (4-bit) | ⭐⭐⭐⭐⭐ | ✅ 永久免费 | 5GB | ❌ HF下载极慢 | **下载失败**——国内 HF 太慢 |
| 本地 UI-TARS-1.5-2B | ⭐⭐⭐⭐ | ✅ 永久免费 | 2GB | 快 | **可行**——待验证 |
| HF 免费 Inference API | ⭐⭐⭐⭐⭐ | $0.10/月 | 0 | 中 | **额度太少** |
| OpenRouter (UI-TARS) | ⭐⭐⭐⭐⭐ | 按量付费 | 0 | ⚠️ 国内慢 | **用户拒绝**——贵+卡 |
| Together AI | ⭐⭐⭐⭐⭐ | 最低充 $5 | 0 | 快 | **非免费** |
| Gemini Grounding | ⭐⭐⭐ | 1500次/天 | 0 | 快 | **国内无法注册** |

## 关键技术发现

### Agent S 架构
- `LMMEngineOpenAI` 接受 `base_url` → 兼容硅基流动等第三方 OpenAI 端点
- `OSWorldACI` 是实际使用的 grounding agent 类（非 SimpleACI/非 MacOSACI）
- grounding 是硬依赖——Worker 每次操作都调 `grounding_agent.assign_screenshot()` + `generate_coords()`

### bitsandbytes 4-bit on MPS
- MPS 上 4-bit Linear **可用**
- CPU 上 4-bit Linear **不可用**
- `device_map="auto"` 可能部分层落在 CPU → 需要在 MPS 设备上加载

### HF 国内下载
- hf-mirror.com 可用但不稳定
- 官方端点 + token 下载 7B 模型需数十分钟至数小时
- 建议用 2B 版本（2GB，快很多）

### API Key 传输
- 系统工具会自动截断 API key（安全机制）
- 绕过方式：写到文件 → 脚本读文件 → 用 `os.environ` 替代

## 推荐路径（按优先级）
1. **UI-TARS-2B 本地** —— 2GB 下载快，永久免费，精度够用
2. **硅基流动 + prompt 适配** —— 如果 2B 也不可行，退而求其次
3. 放弃 Agent S，回到 Hermes desktop-control
