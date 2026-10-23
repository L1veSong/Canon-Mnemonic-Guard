# GitHub + Vercel 部署工作流

## 架构

```
~/Desktop/新疆/         ← 本地编辑（源码）
  index.html
  yili/index.html, style.css, script.js
  altay/, turpan/, ...   ← 预留目录

GitHub: L1veSong/xinjiang-trip (private)
  ↓ 自动同步
Vercel: xinjiang-trip-chi.vercel.app
```

## Token 管理

### Classic vs Fine-grained
- **Classic token (ghp_*)**: 勾 `repo` 即可，所有仓库通吃。推荐。
- **Fine-grained token (github_pat_*)**: 需逐仓库授权 + `Contents: Read and write`。曾经可用但后续全 401，切换为 Classic。

### Shell 传 token 的陷阱
token 在命令中会被安全扫描替换为 `***`。Python `-c` 字符串中的 `'ghp_00...uOiJ'` ——三个点是**字面量字符**，不是占位符。

**✅ 正确做法：写文件再读**
```bash
echo "ghp_完整token" > /tmp/gh_token
python3 << 'PYEOF'
with open('/tmp/gh_token') as f:
    token = f.read().strip()
# ... 使用 token ...
PYEOF
rm -f /tmp/gh_token
```

### Token 持久化
token 存两份：
1. `~/obsidian/🔒 HERMES-全局铁则库/GitHub Token.md`
2. Hermes memory

下次推送：从 memory/obsidian 取 token → `echo > /tmp/gh_token` → Python 读文件 → API 上传

## 上传脚本

```python
import base64, json, urllib.request

with open('/tmp/gh_token') as f:
    token = f.read().strip()

REPO = 'L1veSong/xinjiang-trip'

def upload(path, local_path, msg):
    # GET SHA
    r = urllib.request.Request(f'https://api.github.com/repos/{REPO}/contents/{path}')
    r.add_header('Authorization', f'Bearer {token}')
    r.add_header('Accept', 'application/vnd.github+json')
    sha = json.load(urllib.request.urlopen(r))['sha']
    
    # PUT
    with open(local_path, 'rb') as f:
        content = base64.b64encode(f.read()).decode()
    body = json.dumps({'message': msg, 'content': content, 'sha': sha}).encode()
    r = urllib.request.Request(f'https://api.github.com/repos/{REPO}/contents/{path}',
                               data=body, method='PUT')
    r.add_header('Authorization', f'Bearer {token}')
    r.add_header('Accept', 'application/vnd.github+json')
    return json.load(urllib.request.urlopen(r))

# 使用
upload('yili/index.html', '/Users/holiday_home/Desktop/新疆/yili/index.html', 'update')
```

## Vercel 配置

- 项目: ljylivesong-1392s-projects/xinjiang-trip
- Git 已连接: L1veSong/xinjiang-trip (main branch)
- 主域名: xinjiang-trip-chi.vercel.app
- .icu 自定义域名: 待绑（CNAME → cname.vercel-dns.com）
- 推送自动部署，无需手动 redeploy

## 本地结构 vs GitHub 结构

```
本地 ~/Desktop/新疆/     →  GitHub xinjiang-trip/
  index.html                       index.html
  yili/index.html                  yili/index.html
  yili/style.css                   yili/style.css
  yili/script.js                   yili/script.js
  altay/ (空)                      altay/ (空目录不上传)
```

空目录（altay/turpan/pamir/kashgar）不上传 GitHub。有内容时再推。

## 修改流程

1. 改本地文件
2. **先对比本地 vs GitHub**（见下方"三方对比"章节）
3. 确认差异后再推
4. 跑上传脚本
5. Vercel 自动部署（~30秒）
6. `web_extract` 或浏览器验证 Vercel 页面内容

## 三方对比流程（本地 → GitHub → Vercel）

部署前必须对比，避免推送无变更的文件。

```python
# 1. 获取 GitHub 文件大小和 SHA
url = f'https://api.github.com/repos/{REPO}/contents/{path}'
d = json.load(urllib.request.urlopen(req))
gh_size = d['size']
gh_sha = d['sha']

# 2. 对比本地文件
local_size = os.path.getsize(local_path)
diff = local_size - gh_size

# 3. 关键指标对比
gh_content = base64.b64decode(d['content']).decode()
local = open(local_path).read()
# - 行数差异
# - 特定标记（如"66家"→"78家"）
# - 新增标签页/章节
# - 高德链接数量
```

### 对比输出示例

```
                 GitHub        本地          差异
yili/index.html   81,984字      114,334字     +32,350 (+39%)
  美食条目        68条          78条          +10条
  景点标签页      ❌ 无         ✅ 新增       本地新增
index.html        4,825字       4,825字       完全相同 → 无需推送
```

### 铁则
- 完全相同的文件不要推
- 推送前展示差异摘要给用户确认
- 推完验证 Vercel 页面（web_extract 或 browser_snapshot 看底部导航栏数量）
