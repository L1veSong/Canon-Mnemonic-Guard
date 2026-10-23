# GitHub API 上传：git push 失败时的备选方案

## 触发条件

用户有 GitHub 仓库 + token，但本地 `git push` 因网络问题（TLS 握手失败、超时、代理拦截）不可用。

## 方法：Python + GitHub Contents API

```python
import base64, json, urllib.request

token = 'github_pat_...'  # GitHub Personal Access Token (classic, repo scope)
repo = 'user/repo'

def upload(path, msg):
    req = urllib.request.Request(f'https://api.github.com/repos/{repo}/contents/{path}')
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Accept', 'application/vnd.github+json')
    sha = None
    try:
        d = json.load(urllib.request.urlopen(req))
        sha = d.get('sha')
    except: pass

    with open(local_path, 'rb') as f:
        content = base64.b64encode(f.read()).decode()

    body = json.dumps({'message': msg, 'content': content, **( {'sha': sha} if sha else {})}).encode()
    req = urllib.request.Request(f'https://api.github.com/repos/{repo}/contents/{path}', data=body, method='PUT')
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Accept', 'application/vnd.github+json')
    resp = json.load(urllib.request.urlopen(req))
    print(f'{path}: OK' if 'content' in resp else f'{path}: {resp.get("message")}')
```

## 使用

```bash
python3 -c "
(贴上面的Python代码)
upload('index.html', '更新首页')
upload('yili/index.html', '伊犁行程更新')
"
```

## 注意事项

- Token 必须是 GitHub Personal Access Token (classic)，勾选 `repo` 权限
- Fine-grained token 可能权限不够
- `sha` 字段：首次上传不需要，更新已有文件必须带 sha
- 文件内容 base64 编码
- 此方法绕过本地网络限制，直接调用 GitHub REST API

## 实战记录

2026-06-19：用户 `vercel login` 和 `git push` 均 TLS 握手失败，但 `curl` API 调用成功。用此方法上传了 `index.html` 和 `yili/index.html` 到 `L1veSong/xinjiang-trip`。
