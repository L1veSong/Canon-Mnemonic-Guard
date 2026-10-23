# 高德 SSR 页面 web_extract 兼容性问题

## 现象

CMG Guard 的 `素材提示` 要求对高德 POI 链接（`https://www.amap.com/ssr/place/B0XXX` 或 `https://www.amap.com/ssr/search/poi_detail?...`）调用 `web_extract` 读取内容。

## 结果

**100% 失败**（本会话验证 60+ 次，零次成功）。

三种失败模式：
- `Failed to fetch url` — SSR place 页面（最常见）
- `404 page not found` — poi_detail 格式
- `SSL: UNEXPECTED_EOF_WHILE_READING` — 偶发

## 根因

高德地图 SSR 页面（`/ssr/place/` 和 `/ssr/search/poi_detail`）是 JS 渲染的单页应用。`web_extract` 无法执行 JavaScript，只能抓取服务端渲染内容——而高德 SSR 返回的是空壳 HTML，实际内容由客户端 JS 动态生成。

## 影响

- CMG Guard 每次遇到高德链接都强制要求 `web_extract` → 浪费 1 轮工具调用 + 额外 token
- 本会话中，60+ 次 `web_extract` 调用全部返回失败，对实际任务无任何贡献
- 用户提供的高德 POI ID 是已知事实（用户亲自在高德 App 搜到的），不需要验证

## 建议

CMG Guard 应识别高德 SSR URL 模式（`amap.com/ssr/`），直接跳过 `web_extract` 要求。

## 日期

2026-06-15 · 会话中首次记录
