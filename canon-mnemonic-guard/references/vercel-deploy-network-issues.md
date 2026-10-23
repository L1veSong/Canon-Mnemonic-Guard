# Vercel 部署网络受限环境应对

> 来源：新疆行程部署实战（2026-06-19）

## 问题
`vercel login` 报 TLS 握手失败（`Client network socket disconnected before secure TLS connection was established`），`git push` 超时。

## 根因
本地网络（公司防火墙/代理）拦截了到 `vercel.com` 和 `github.com` 的 CLI 直连。

## 绕过方案

### Vercel 部署
```bash
# 方案 A：用 token 直连（跳过 login）
vercel --token <vc_pat_token> --yes

# 方案 B：手动创建 token
# 浏览器打开 https://vercel.com/account/tokens → Create Token
# 然后 vercel --token <token> --yes
```

### GitHub 上传（CLI 不通时）
```bash
# 用 Python API 上传文件
python3 -c "
import base64, json, urllib.request
token = 'github_pat_...'
repo = 'user/repo'

def upload(path, msg):
    req = urllib.request.Request(f'https://api.github.com/repos/{repo}/contents/{path}')
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Accept', 'application/vnd.github+json')
    # GET sha if exists, PUT with base64 content
    ...
    print(f'{path}: OK' if 'content' in resp else f'{path}: {resp.get(\"message\")}')

upload('index.html', 'commit message')
"
```

### GitHub Token 要求
- Fine-grained PAT 需要 "Contents: Read and write" 权限
- 需要授权到**具体仓库**（在 token 设置里选 `Only select repositories` → 勾 L1veSong/xinjiang-trip）
- 如报 401：检查 token 是否过期/仓库是否授权

### 检查清单
- [ ] Vercel PAT (`vcp_xxx`) 可读
- [ ] GitHub PAT (`github_pat_xxx`) 可读写 Contents
- [ ] GitHub PAT 授权了目标仓库
- [ ] `curl https://api.github.com/repos/<user>/<repo> -H "Authorization: Bearer <token>"` 返回 200
