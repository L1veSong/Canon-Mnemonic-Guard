# 地图渲染教训 (2026-06-15)

## 背景
用户要求做新疆互动地图入口页。尝试了 5 种方案都失败：
- 3D Three.js 噪音地形 → "很丑"
- Canvas 2D 像素渲染 → 性能灾难
- Leaflet 瓦片地图 → "不要这么真实"
- SVG + 硬编码 GeoJSON → JS 解析失败
- SVG + fetch DataV API → **唯一正确**

## 核心教训
每改一次 HTML 都应该先打开浏览器确认渲染正常再继续。本条违反 ban_act_before_verify 至少 8 次。

## 模式
用真实数据别自己造：DataV API → GeoJSON → SVG path。禁止：嵌入 script 标签、邻接地州填充色、模拟地形。
