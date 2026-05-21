# Mnemonic 忆存线 v3.0.0

> 自省引擎的状态记忆层。读取 Guard 拦截日志，自动识别高频错误模式。

不生产规则、不执行拦截——只分析、只推送。

## 安装

```bash
npx skills add mnemonic --yes --global
```

## 工作原理

Guard 拦截 → 写入日志 → Mnemonic 分析 → 发现高频模式 → 推送 Canon 固化。

## CLI

- `hermes reflect status` — 查看规则库状态
- `hermes reflect patterns` — 查看高频错误模式

## 三线联动

Canon（规则生产）→ Guard（拦截执行）→ Mnemonic（模式识别）→ Canon（固化升级）

## License

MIT © L1veSong
