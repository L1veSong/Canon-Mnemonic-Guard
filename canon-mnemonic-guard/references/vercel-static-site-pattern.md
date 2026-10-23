# Vercel 静态站 + GitHub + 自定义域名

## 完整流程

1. **本地建项目目录** → `mkdir project && cp index.html project/`
2. **Vercel CLI 部署**（先拿一个临时域名）→ `vercel --token <token> --yes`
3. **GitHub 建私有仓库** → 上传文件
4. **Vercel 连 GitHub** → Settings → Git → Connect `user/repo`
5. **绑自定义域名** → Settings → Domains → 输入域名 → DNS 加 CNAME 指向 `cname.vercel-dns.com`
6. **之后改文件** → 本地改 → `git push` → Vercel 自动部署

## 多页面静态站结构

```
repo/
  index.html      ← 入口页（链接到各子目录）
  yili/
    index.html    ← 伊犁行程
  altay/
    index.html    ← 阿勒泰（预留）
```

Vercel 自动路由：`domain.com/yili/` → `yili/index.html`

## 公开版脱敏规则

单 HTML 旅行攻略脱敏：
- 酒店名 → 通用名（"朗丽兹" → "大兴机场附近酒店"）
- 价格 → 隐藏
- 航班号 → 隐藏（MU5173 → "上午航班"）
- 预算页 → 替换为"适中预算"概览
- 租车品牌 → 通用（"理想L8" → "SUV"）

保留：行程、景点、路线、动画、CSS。

## Token 区分

- Vercel token：`vcp_...` — 用于 `vercel --token` 或 API
- GitHub token：`ghp_...` (classic) 或 `github_pat_...` (fine-grained) — 用于 git push 或 API 上传
- 两者不可互换

## 实战：xinjiang-trip

- 仓库：`L1veSong/xinjiang-trip`（私有）
- 域名：`xinjiang-trip-chi.vercel.app` + 用户 .icu 域名
- 结构：入口页 + `yili/` 子目录
