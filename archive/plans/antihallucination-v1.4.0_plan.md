# sentinel v1.4.0 — 防幻觉增强计划（完整版）

> 创建: 2026-05-31 | 基线: sentinel v1.3.2 + CMG v5.6.0
> 来源: 豆包 6 方案 + DeepSeek 全景图 交叉分析
> 核心思想: 事后拦截 → 事前注入。给模型数据，不等它编完再抓。

---

## 一、问题定义

### 1.1 幻觉分类（豆包/DeepSeek 一致）

| 类型 | 特征 | sentinel 当前能力 |
|------|------|:--:|
| **假性幻觉（偷懒）** | 模型知道自己没查，故意编造 | ✅ post_llm_call evidence check + external-claims 能拦 |
| **真性幻觉（认知篡改）** | 模型真心以为自己查了，实际没查 | ❌ 事后拦不住——模型不觉得自己在撒谎 |

### 1.2 根因分析

LLM 推理时手中没数据 → 概率补全引擎自动脑补。不是"想撒谎"，是"不知道自己在编"。坑点 29 已确认架构边界：post_llm_call 拦得住说出来的假话，拦不住脑子里形成的假结论。

### 1.3 策略转变

**事后拦截 → 事前注入。** 模型张嘴之前，上下文已经有事实材料——不需要回忆，不需要脑补。两份外部来源（豆包 + DeepSeek）都指向 RAG/知识注入/验证层 这个方向。

---

## 二、方案设计

### 2.1 架构总览

```
用户消息
    │
    ▼
sentinel pre_llm_call 钩子 (现有增强)
    │
    ├── 1. _scan_blacklist(user_message)          [现有，不变]
    ├── 2. _scan_user_message(user_message)        [现有，sentinel]
    ├── 3. _check_task_recommendations(...)         [现有，不变]
    ├── 4. _check_step_completeness(...)            [现有，不变]
    │
    ├── 5. _inject_context_facts(user_message, session_id)  ★ 新增: 路1
    │   ├── _extract_entities(message) → List[str]
    │   ├── _query_rules(entity) → List[Fact]
    │   ├── _query_memory(entity) → List[Fact]
    │   ├── _query_soul(entity) → List[Fact]
    │   └── _format_facts(facts, session_dedup) → str
    │
    ├── 6. _prefetch_materials(user_message, session_id)    ★ 新增: 路2
    │   ├── _extract_urls(message) → List[str]
    │   ├── _detect_fact_query(message) → bool
    │   ├── _fetch_urls(urls) → List[FetchResult]
    │   ├── _fetch_search(query) → List[SearchResult]
    │   └── _format_prefetch(results) → str
    │
    └── return {"context": 合并所有注入文本}
            │
            ▼
        LLM 推理（上下文中已有事实 + 素材）
            │
            ▼
sentinel post_llm_call 钩子 (现有增强)
    │
    ├── 1. _scan_blacklist(response_text)          [现有，不变]
    ├── 2. _check_completion_evidence(response_text) [现有，不变]
    ├── 3. _check_external_claims(response_text)     [现有，不变]
    ├── 4. _append_cove_prompt(response_text)        ★ 新增: CoVe 薄层
    │   └── _detect_fact_claims(text) → bool
    │   └── 追加自检提示文本
    │
    └── return 拦截消息 或 None
```

### 2.2 路 1：上下文事实注入 (`_inject_context_facts`)

**目标：** 用户提到某实体时，自动从 rules/ + memory + SOUL.md 检索关联事实，注入 LLM 上下文。模型不需要回忆。

#### 2.2.1 实体提取 (`_extract_entities`)

```python
# 实体字典：关键词 → 标准化名称（用于检索 memory/rules）
_ENTITY_PATTERNS: Dict[str, re.Pattern] = {
    # 工具名
    "Tavily":     re.compile(r"tavily", re.IGNORECASE),
    "Firecrawl":  re.compile(r"firecrawl", re.IGNORECASE),
    "Obsidian":   re.compile(r"obsidian", re.IGNORECASE),
    "OpenWebUI":  re.compile(r"openwebui|open.webui", re.IGNORECASE),
    "Codex":      re.compile(r"codex\s*cli|openai\s*codex", re.IGNORECASE),
    "Claude Code":re.compile(r"claude\s*code", re.IGNORECASE),
    "OpenCode":   re.compile(r"opencode", re.IGNORECASE),
    "ralph-loop": re.compile(r"ralph[\s-]*loop", re.IGNORECASE),
    "Agent S":    re.compile(r"agent[\s-]*s", re.IGNORECASE),
    "豆包":       re.compile(r"豆包", re.IGNORECASE),
    "DeepSeek":   re.compile(r"deepseek", re.IGNORECASE),
    # CMG 组件
    "sentinel":  re.compile(r"cmg[\s-]*guard", re.IGNORECASE),
    "canon-mnemonic-guard": re.compile(r"canon[\s-]*mnemonic[\s-]*guard|CMG|三省引擎", re.IGNORECASE),
    # 偏好关键词
    "模型偏好":   re.compile(r"(模型|provider|用哪个|用什么模型|换.*模型)", re.IGNORECASE),
    "成本敏感":   re.compile(r"(token|成本|费用|省钱|免费|额度|收费)", re.IGNORECASE),
    "TDD":        re.compile(r"\btdd\b|测试驱动", re.IGNORECASE),
    "VBC":        re.compile(r"verification.before.completion|VBC|验证.*完成", re.IGNORECASE),
    # CMG 规则相关
    "skill-authoring": re.compile(r"skill.authoring|skill.*编写|skill.*发布|上传.*skill", re.IGNORECASE),
    "幻觉":       re.compile(r"幻觉|编造|脑补|瞎编|虚构", re.IGNORECASE),
}

def _extract_entities(message: str) -> List[str]:
    """Extract known entity names from user message. 
    Returns deduplicated list of standardized entity names."""
    found = []
    for entity_name, pattern in _ENTITY_PATTERNS.items():
        if pattern.search(message):
            found.append(entity_name)
    # Dedup + preserve order
    seen = set()
    return [e for e in found if not (e in seen or seen.add(e))]
```

**设计决策：** 用静态字典而不是调 LLM 提取——零延迟、零 token 消耗。字典随版本迭代手动扩充（新发现的偏好/实体加入字典）。

#### 2.2.2 规则库检索 (`_query_rules`)

```python
def _query_rules(entity: str) -> List[str]:
    """Search CMG rules/ directory for rules mentioning this entity.
    
    Scans frontmatter keywords + description fields across:
      rules/ban/*.md, rules/gap/*.md, rules/lazy/*.md, rules/meta/*.md
    
    Returns list of rule descriptions (one-liners), max 3 per entity.
    """
    rules_dir = Path(os.path.expanduser("~/.hermes/self-reflection/rules"))
    if not rules_dir.is_dir():
        return []
    
    entity_lower = entity.lower()
    results = []
    
    for category in ("ban", "gap", "lazy", "meta"):
        cat_dir = rules_dir / category
        if not cat_dir.is_dir():
            continue
        for md_file in sorted(cat_dir.glob("*.md")):
            try:
                text = md_file.read_text(encoding="utf-8")
                # Check if entity appears anywhere in the file
                if entity_lower not in text.lower():
                    continue
                # Extract title (first # heading)
                title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
                title = title_match.group(1) if title_match else md_file.stem
                results.append(f"CMG {category}规则: {title}")
            except Exception:
                continue
            if len(results) >= 3:
                break
        if len(results) >= 3:
            break
    
    return results[:3]
```

**设计决策：** 不走 YAML frontmatter 解析（当前 `_load_ban_keywords` 已做），用全文搜索——因为规则描述可能不只在 keywords 字段里。3 条硬上限防止注入过量。

#### 2.2.3 Memory 检索 (`_query_memory`)

```python
def _query_memory(entity: str) -> List[str]:
    """Query Hermes memory store for entries containing this entity.
    
    Uses memory tool's search capability. Falls back gracefully if
    memory API is unavailable.
    """
    try:
        # Attempt to use Hermes memory API
        from hermes_cli.memory import search_memory
        results = search_memory(entity, limit=3)
        facts = []
        for r in results:
            content = r.get("content", "") or r.get("text", "") or str(r)
            if content and len(content) > 10:
                facts.append(content[:200])
        return facts[:3]
    except ImportError:
        # Fallback: read memory file directly
        logger.debug("[sentinel] memory API not available, trying file read")
        return _query_memory_file(entity)
    except Exception as e:
        logger.debug("[sentinel] memory query failed for '%s': %s", entity, str(e)[:80])
        return []

def _query_memory_file(entity: str) -> List[str]:
    """Fallback: grep memory storage file for entity mentions."""
    memory_paths = [
        os.path.expanduser("~/.hermes/memory/user.json"),
        os.path.expanduser("~/.hermes/memory/memory.json"),
    ]
    results = []
    entity_lower = entity.lower()
    for mp in memory_paths:
        if not os.path.exists(mp):
            continue
        try:
            with open(mp, encoding="utf-8") as f:
                data = json.load(f)
            # data is usually a list of {content, ...} or dict with entries
            items = data if isinstance(data, list) else data.get("entries", [])
            for item in items:
                content = item.get("content", "") if isinstance(item, dict) else str(item)
                if entity_lower in content.lower():
                    results.append(content[:200])
                if len(results) >= 3:
                    break
        except Exception:
            continue
        if results:
            break
    return results[:3]
```

**设计决策：** 两阶段降级——优先用 Hermes memory API（如果暴露），降级到直接读 JSON 文件。Hermes memory 的 Python API 路径需要验证（当前代码只用到 `hermes_cli.config` 和 `hermes_cli.session`）。如果两个路径都不可用，返回空列表不报错。

**待验证：** `hermes_cli.memory.search_memory` 是否真实存在。如果不存在，直接用文件读取路径。首次实现后通过 `grep -r "search_memory\|memory.*search\|def.*memory" ~/.hermes/` 确认 API 签名。

#### 2.2.4 SOUL.md 检索 (`_query_soul`)

```python
def _query_soul(entity: str) -> List[str]:
    """Search SOUL.md for paragraphs mentioning this entity.
    
    SOUL.md is the user's permanent system prompt rules.
    Returns relevant paragraphs (not full SOUL.md).
    """
    soul_paths = [
        os.path.expanduser("~/.hermes/SOUL.md"),
        os.path.expanduser("~/.hermes/profiles/default/SOUL.md"),
    ]
    entity_lower = entity.lower()
    for sp in soul_paths:
        if not os.path.exists(sp):
            continue
        try:
            text = Path(sp).read_text(encoding="utf-8")
            # Split into paragraphs (double newline)
            paragraphs = re.split(r"\n\s*\n", text)
            matches = []
            for para in paragraphs:
                if entity_lower in para.lower() and len(para.strip()) > 10:
                    matches.append(para.strip()[:300])
                if len(matches) >= 2:
                    break
            return matches
        except Exception:
            continue
    return []
```

**设计决策：** 只返回匹配段落，不返回全量 SOUL.md——SOUL 通常很大（~200 行），全注入浪费 token。最多 2 段、每段截断 300 字符。

#### 2.2.5 事实组装与注入 (`_format_facts` + `_inject_context_facts`)

```python
# Per-session dedup: prevent same fact from being injected twice
_FACTS_INJECTED: Dict[str, Set[str]] = {}

def _inject_context_facts(user_message: str, session_id: str) -> Optional[str]:
    """Main entry for context fact injection.
    
    1. Extract entities from user message
    2. Query rules + memory + soul for each entity
    3. Dedup against session history
    4. Format and return injection text
    """
    entities = _extract_entities(user_message)
    if not entities:
        return None
    
    session_dedup = _FACTS_INJECTED.setdefault(session_id, set())
    
    all_facts = []
    for entity in entities:
        # Query all three sources
        rules_facts = _query_rules(entity)
        memory_facts = _query_memory(entity)
        soul_facts = _query_soul(entity)
        
        for fact in rules_facts + memory_facts + soul_facts:
            # Dedup key: first 80 chars of fact content
            key = fact[:80]
            if key not in session_dedup:
                session_dedup.add(key)
                all_facts.append(fact)
    
    if not all_facts:
        return None
    
    # Cap total facts per injection
    max_facts = _load_context_facts_config().get("max_facts_per_injection", 5)
    all_facts = all_facts[:max_facts]
    
    # Format injection
    lines = ["[CMG 上下文事实] 以下为与该话题相关的已记录事实，请据此回答："]
    for i, fact in enumerate(all_facts, 1):
        lines.append(f"  {i}. {fact}")
    
    return "\n".join(lines)
```

**注入示例：**
```
[CMG 上下文事实] 以下为与该话题相关的已记录事实，请据此回答：
  1. CMG ban规则: 禁止对SKILL.md直接patch而不先加载hermes-agent-skill-authoring
  2. 用户偏好 Tavily 而非 Firecrawl（每月1000次免费搜索 vs 固定500次）
  3. 用户对token成本敏感，能省的绝不浪费
```

### 2.3 路 2：素材自动预拉取 (`_prefetch_materials`)

**目标：** 用户消息含 URL → 自动 web_extract。事实性提问 → 自动 web_search。模型推理前素材已就位。

#### 2.3.1 URL 提取 (`_extract_urls`)

```python
_URL_PATTERN = re.compile(r"https?://[^\s<>\"']+")

def _extract_urls(message: str) -> List[str]:
    """Extract unique URLs from user message. Max 3."""
    urls = list(dict.fromkeys(_URL_PATTERN.findall(message)))  # ordered dedup
    max_urls = _load_prefetch_config().get("max_urls", 3)
    return urls[:max_urls]
```

#### 2.3.2 事实性提问检测 (`_detect_fact_query`)

```python
# Positive signals: user is asking a factual question
_FACT_QUERY_PATTERNS = [
    re.compile(r"(是什么|什么是|怎么|如何|为什么|哪个|哪些|多少|什么时候)"),
    re.compile(r"(最新|最近|现在|当前|目前|刚刚)"),
    re.compile(r"(文档|API|参数|版本|发布|更新|changelog|release)"),
    re.compile(r"(解决|修复|处理|排查|debug|fix)"),
    re.compile(r"(真的吗|确定吗|对吗|是不是|有没有)"),
    re.compile(r"\?|？"),  # question mark
]

# Negative signals: casual chat, not fact-seeking
_NOT_FACT_QUERY_PATTERNS = [
    re.compile(r"^(hi|hey|hello|你好|嗨|在吗|早|晚安|谢谢|再见|拜拜)"),
    re.compile(r"^(好|ok|嗯|哦|行|对|是的|没错|可以|来吧|去吧)"),
    re.compile(r"^(哈哈|嘻嘻|嘿嘿|emm|emmm|...)"),
]

def _detect_fact_query(message: str) -> bool:
    """Heuristic: does this message look like a factual question?"""
    msg = message.strip()
    if len(msg) < 5:
        return False
    
    # Negative check first: casual chat
    for pat in _NOT_FACT_QUERY_PATTERNS:
        if pat.search(msg):
            return False
    
    # Positive check: at least one fact-seeking signal
    for pat in _FACT_QUERY_PATTERNS:
        if pat.search(msg):
            return True
    
    return False
```

**设计决策：** 纯启发式，不调 LLM。宁可漏判（少搜一次）不可误判（浪费搜索额度）。偏向保守——用户说"好"、"去吧"、"嗯"不触发搜索。

#### 2.3.3 URL 内容拉取 (`_fetch_urls`)

```python
# Per-session URL cache: don't re-fetch same URL in same session
_URL_FETCH_CACHE: Dict[str, Dict[str, FetchResult]] = {}

class FetchResult:
    def __init__(self, url: str, success: bool, content: str = "", error: str = ""):
        self.url = url
        self.success = success
        self.content = content
        self.error = error

def _fetch_urls(urls: List[str], session_id: str) -> List[FetchResult]:
    """Fetch URL content via Hermes web_extract, with session cache.
    
    NOTE: This function's implementation depends on whether the Hermes
    plugin environment exposes tool-calling APIs. Three fallback paths:
    
    Path A (preferred): Call Hermes internal web_extract function
    Path B: Use Python requests + html2text
    Path C: Shell out to curl + readability CLI
    """
    if not urls:
        return []
    
    cache = _URL_FETCH_CACHE.setdefault(session_id, {})
    results = []
    urls_to_fetch = []
    
    for url in urls:
        if url in cache:
            results.append(cache[url])
        else:
            urls_to_fetch.append(url)
    
    if not urls_to_fetch:
        return results
    
    config = _load_prefetch_config()
    timeout = config.get("timeout", 10)
    token_budget = config.get("token_budget", 2000)
    
    # Attempt Path A: Hermes internal web_extract
    fetched = _fetch_urls_hermes(urls_to_fetch, timeout)
    if fetched is None:
        # Path B: direct HTTP
        fetched = _fetch_urls_direct(urls_to_fetch, timeout)
    if fetched is None:
        # Path C: all failed, return error markers
        fetched = [FetchResult(u, False, error="无法访问（所有路径均失败）") for u in urls_to_fetch]
    
    for fr in fetched:
        # Truncate to token budget (distributed evenly)
        per_url_budget = token_budget // max(len(fetched), 1)
        if len(fr.content) > per_url_budget:
            fr.content = fr.content[:per_url_budget] + "…"
        cache[fr.url] = fr
        results.append(fr)
    
    return results

def _fetch_urls_hermes(urls: List[str], timeout: int) -> Optional[List[FetchResult]]:
    """Path A: Use Hermes web_extract tool if available."""
    try:
        # This import needs verification — Hermes may or may not expose this
        from hermes_cli.tools.web import extract_urls
        raw_results = extract_urls(urls, timeout=timeout)
        return [
            FetchResult(
                url=r.get("url", u),
                success=not r.get("error"),
                content=r.get("content", "") or r.get("text", ""),
                error=r.get("error", "")
            )
            for u, r in zip(urls, raw_results)
        ]
    except ImportError:
        logger.debug("[sentinel] hermes_cli.tools.web not available")
        return None
    except Exception as e:
        logger.debug("[sentinel] web_extract failed: %s", str(e)[:80])
        return None

def _fetch_urls_direct(urls: List[str], timeout: int) -> Optional[List[FetchResult]]:
    """Path B: Use requests + html2text directly."""
    try:
        import requests
    except ImportError:
        return None
    
    results = []
    for url in urls:
        try:
            resp = requests.get(url, timeout=timeout, headers={
                "User-Agent": "Hermes-sentinel/1.4.0"
            })
            if resp.status_code == 200:
                # Simple text extraction: strip HTML tags
                text = re.sub(r"<[^>]+>", " ", resp.text)
                text = re.sub(r"\s+", " ", text).strip()
                results.append(FetchResult(url, True, content=text[:2000]))
            else:
                results.append(FetchResult(url, False, error=f"HTTP {resp.status_code}"))
        except Exception as e:
            results.append(FetchResult(url, False, error=str(e)[:100]))
    return results
```

**设计决策：**
- 三路径降级：Hermes API → requests → 全失败报告。确保至少有一个路径能跑。
- URL 会话级缓存：同一会话同一 URL 不重复拉取。
- **关键待验证：** `hermes_cli.tools.web.extract_urls` 是否存在。首次实现时需 `grep -r "def extract\|def web_extract" ~/.hermes/` 确认。

#### 2.3.4 搜索拉取 (`_fetch_search`)

```python
_SEARCH_CACHE: Dict[str, Dict[str, List[str]]] = {}

def _fetch_search(query: str, session_id: str) -> List[str]:
    """Perform web search and return result summaries.
    
    Three paths, same fallback pattern as URL fetching.
    """
    cache = _SEARCH_CACHE.setdefault(session_id, {})
    if query in cache:
        return cache[query]
    
    config = _load_prefetch_config()
    max_results = config.get("max_search_results", 3)
    
    results = _fetch_search_hermes(query, max_results)
    if results is None:
        results = _fetch_search_direct(query, max_results)
    if results is None:
        results = [f"搜索 '{query[:50]}' 暂时不可用（搜索服务未就绪）"]
    
    cache[query] = results
    return results

def _fetch_search_hermes(query: str, max_results: int) -> Optional[List[str]]:
    """Path A: Hermes internal web_search."""
    try:
        from hermes_cli.tools.web import search
        raw = search(query, limit=max_results)
        summaries = []
        for r in raw:
            title = r.get("title", "") or ""
            desc = r.get("description", "") or r.get("snippet", "") or ""
            url = r.get("url", "") or ""
            if title or desc:
                summaries.append(f"{title}: {desc[:150]}")
                if url:
                    summaries[-1] += f" ({url})"
        return summaries if summaries else None
    except ImportError:
        return None
    except Exception as e:
        logger.debug("[sentinel] web_search failed: %s", str(e)[:80])
        return None

def _fetch_search_direct(query: str, max_results: int) -> Optional[List[str]]:
    """Path B: direct HTTP to a search API."""
    try:
        import requests
        # Use Tavily as default (user preference from memory)
        api_key = os.environ.get("TAVILY_API_KEY", "")
        if not api_key:
            return None  # No API key, can't search directly
        
        resp = requests.post(
            "https://api.tavily.com/search",
            json={"query": query, "max_results": max_results, "api_key": api_key},
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            results = []
            for r in data.get("results", [])[:max_results]:
                results.append(f"{r.get('title', '')}: {r.get('content', '')[:150]}")
            return results if results else None
    except Exception:
        pass
    return None
```

#### 2.3.5 预拉取组装 (`_format_prefetch` + `_prefetch_materials`)

```python
def _prefetch_materials(user_message: str, session_id: str) -> Optional[str]:
    """Main entry for material prefetch.
    
    1. Extract URLs → fetch
    2. Detect fact query → search
    3. Format results into injection text
    """
    urls = _extract_urls(user_message)
    is_fact = _detect_fact_query(user_message)
    
    if not urls and not is_fact:
        return None
    
    parts = []
    
    # URL results
    if urls:
        fetch_results = _fetch_urls(urls, session_id)
        for fr in fetch_results:
            if fr.success:
                parts.append(f"📎 {fr.url}\n   内容摘要: {fr.content[:300]}")
            else:
                parts.append(f"📎 {fr.url}\n   ⚠️ 无法访问: {fr.error}")
    
    # Search results
    if is_fact:
        query = user_message[:200]  # Use message itself as search query
        search_results = _fetch_search(query, session_id)
        if search_results:
            parts.append(f"🔍 搜索 \"{query[:80]}...\" 的结果:")
            for i, sr in enumerate(search_results, 1):
                parts.append(f"   {i}. {sr}")
    
    if not parts:
        return None
    
    return "[CMG 素材预拉取]\n" + "\n".join(parts)
```

**注入示例（URL 成功）：**
```
[CMG 素材预拉取]
📎 https://www.doubao.com/thread/w78ccdaa6336eb5f5
   内容摘要: Hermes 幻觉的解决办法 - 豆包。2026年5月31日。完全听懂你全部痛点...
```

**注入示例（URL 失败）：**
```
[CMG 素材预拉取]
📎 https://chat.deepseek.com/share/54cg7oyxm7d3b6qybx
   ⚠️ 无法访问: cookie 墙阻挡，需手动打开
```

### 2.4 CoVe 薄层自检 (`_append_cove_prompt`)

**目标：** 模型输出后在末尾追加自检提示，让模型自己逐条验证。不硬拦截，不中断输出。

#### 2.4.1 事实主张检测

```python
# Patterns indicating the output contains factual claims
_FACT_CLAIM_PATTERNS = [
    re.compile(r"\d{4}年"),                               # 年份
    re.compile(r"\d+[万亿千百]?\s*(元|次|条|个|人|%|美元)"),  # 数量+单位
    re.compile(r"(根据|按照|引用|来源|据|来自)"),             # 引用标记
    re.compile(r"(已|已经|刚|刚刚|成功|完成|实现)"),          # 完成/实现断言
    re.compile(r"(不存在|没有|不是|并非|从未)"),              # 否定断言
    re.compile(r"✅|✓|✔️"),                                  # 完成标记
]

def _detect_fact_claims(text: str) -> bool:
    """Does this response text appear to contain factual claims?"""
    if len(text) < 50:
        return False
    for pat in _FACT_CLAIM_PATTERNS:
        if pat.search(text):
            return True
    return False
```

#### 2.4.2 CoVe 提示注入

```python
_COVE_PROMPT = (
    "\n\n---\n"
    "[CMG CoVe 自检] 请逐条确认你上述内容：\n"
    "• 哪些陈述有可追溯的证据（链接、工具输出、文件内容）？\n"
    "• 哪些是推测或基于训练记忆的泛化？如有请标注「推测」。\n"
    "• 如有无法确认的内容，请明确说明。"
)

def _append_cove_prompt(response_text: str) -> Optional[str]:
    """If response contains factual claims, append CoVe self-check prompt.
    
    This is NOT an interception — it appends to the output rather than
    replacing it. The model sees the prompt and generates additional
    verification text.
    
    Returns the CoVe prompt string to append, or None if not applicable.
    """
    config = _load_cmg_config()
    cove_enabled = config.get("hooks", {}).get("post_llm_call_cove", True)
    if not cove_enabled:
        return None
    
    if _detect_fact_claims(response_text):
        return _COVE_PROMPT
    
    return None
```

**设计决策：** CoVe 不中断输出——它追加到末尾，模型看到后会生成额外的验证段落。这和 post_llm_call 的拦截模式（evidence check 替换输出）不同。Hermes post_llm_call 返回 str 时是**替换**输出而非追加。因此实际实现时需要确认 Hermes 是否支持"追加"模式，或者改为在 replace 文本中包含原输出 + CoVe 提示。

**待验证：** Hermes post_llm_call hook 的返回语义——返回 `str` 是完全替换还是追加？需要查看 Hermes 文档或通过实验确认。如果只支持替换，则实现为：
```python
return response_text + _COVE_PROMPT  # 保留原输出 + 追加 CoVe
```

### 2.5 主函数修改

#### 2.5.1 `_pre_llm_call` 增强

```python
def _pre_llm_call(user_message: str = "", session_id: str = "", **kwargs) -> Optional[dict]:
    if not _hook_enabled("pre_llm_call"):
        return None
    
    context_parts = []
    
    # [现有] 1. Blacklist scan
    bl_msg = _scan_blacklist(user_message)
    if bl_msg:
        logger.info("[sentinel] blacklist intercept")
        return {"context": f"[CMG-BLACKLIST-BLOCK] {bl_msg}"}
    
    # [现有] 2. Sentinel scan
    if _sentinel_enabled():
        flag = _scan_user_message(user_message)
        if flag:
            logger.info("[sentinel] sentinel: flagged suspected correction")
            context_parts.append(flag)
    
    # [现有] 3. Task recommendations
    if _task_recommendations_enabled():
        rec_msg = _check_task_recommendations(user_message, session_id)
        if rec_msg:
            context_parts.append(rec_msg)
    
    # [现有] 4. Step completeness
    step_fail = _check_step_completeness(user_message, **kwargs)
    if step_fail:
        logger.info("[sentinel] step check: blocking LLM call")
        context_parts.append(step_fail)
    
    # ★ 新增 5. Context facts injection (路1)
    if _context_facts_enabled():
        facts_msg = _inject_context_facts(user_message, session_id)
        if facts_msg:
            context_parts.append(facts_msg)
    
    # ★ 新增 6. Material prefetch (路2)
    if _material_prefetch_enabled():
        prefetch_msg = _prefetch_materials(user_message, session_id)
        if prefetch_msg:
            context_parts.append(prefetch_msg)
    
    if not context_parts:
        return None
    
    return {"context": "\n\n".join(context_parts)}
```

**注入顺序设计：** blacklist/sentinel 最前（拦截优先），step check 次之（阻断），事实注入和预拉取最后（增强型，不阻断）。同一个 `context` 字段合并返回——Hermes 会将所有 context 注入 LLM 系统提示。

#### 2.5.2 `_post_llm_call` 增强

```python
def _post_llm_call(response_text: str = "", **kwargs) -> Optional[str]:
    if not _hook_enabled("post_llm_call"):
        return None
    
    # [现有] 1. Blacklist scan
    bl_msg = _scan_blacklist(response_text)
    if bl_msg:
        return bl_msg
    
    # [现有] 2. Completion evidence check
    evidence_fail = _check_completion_evidence(response_text)
    if evidence_fail:
        return evidence_fail
    
    # [现有] 3. External claims check
    external_fail = _check_external_claims(response_text)
    if external_fail:
        return external_fail
    
    # ★ 新增 4. CoVe self-check prompt (append mode)
    cove_prompt = _append_cove_prompt(response_text)
    if cove_prompt:
        # Preserve original output + append CoVe prompt
        # Assumes Hermes post_llm_call return replaces output
        return response_text + cove_prompt
    
    return None
```

### 2.6 配置开关函数

```python
def _context_facts_enabled() -> bool:
    """Check if context facts injection is enabled."""
    cfg = _load_cmg_config()
    return cfg.get("hooks", {}).get("pre_llm_call_context_facts", True)

def _material_prefetch_enabled() -> bool:
    """Check if material prefetch is enabled."""
    cfg = _load_cmg_config()
    return cfg.get("hooks", {}).get("pre_llm_call_material_prefetch", True)

def _load_context_facts_config() -> dict:
    """Load context facts sub-config with defaults."""
    cfg = _load_cmg_config()
    defaults = {
        "max_facts_per_injection": 5,
        "sources": ["rules", "memory", "soul"],
    }
    user_cfg = cfg.get("context_facts", {})
    return {**defaults, **user_cfg}

def _load_prefetch_config() -> dict:
    """Load material prefetch sub-config with defaults."""
    cfg = _load_cmg_config()
    defaults = {
        "max_urls": 3,
        "max_search_results": 3,
        "token_budget": 2000,
        "timeout": 10,
    }
    user_cfg = cfg.get("material_prefetch", {})
    return {**defaults, **user_cfg}
```

---

## 三、version 与文件变更清单

### 3.1 版本号

| 组件 | 当前 | 目标 | 说明 |
|------|------|------|------|
| sentinel `__init__.py` | v1.3.2 | **v1.4.0** | 插件文件头部 docstring + logger 消息 |
| sentinel CHANGELOG | v1.3.2 | 追加 v1.4.0 | 新增条目 |
| CMG 四包 | v5.6.0 | v5.6.0（不变） | 插件独立升级，不影响 CMG 核心 |
| CMG SKILL.md | v5.6.0 | v5.6.0（不变） | 可选追加坑点 35（防幻觉增强记录） |

### 3.2 文件变更

| 文件 | 操作 | 行数变化 | 内容 |
|------|:--:|:--:|------|
| `~/.hermes/plugins/sentinel/__init__.py` | 修改 | +~300 行 | 新增路1+路2+CoVe 全部函数，修改 _pre_llm_call 和 _post_llm_call |
| `~/.hermes/config.yaml` | 手动追加 | +11 行 | 新增配置项（用户粘贴） |
| `~/.hermes/plugins/sentinel/CHANGELOG.md` | 修改 | +~20 行 | v1.4.0 条目 |
| `~/.hermes/skills/.../canon-mnemonic-guard/SKILL.md` | 可选修改 | +~10 行 | 坑点 35：防幻觉增强 |
| 桌面包 ZIP | 更新 | — | 6 组件重新打包 |
| GitHub | 推送 | — | 覆盖 v5.5.5 tag |

---

## 四、config.yaml 新增配置（用户粘贴块）

```yaml
# === sentinel v1.4.0 新增 ===
sentinel:
  hooks:
    pre_llm_call: true                       # [现有] 不变
    pre_llm_call_context_facts: true         # [新增] 上下文事实注入
    pre_llm_call_material_prefetch: true     # [新增] 素材自动预拉取
    post_llm_call: true                      # [现有] 不变
    post_llm_call_cove: true                 # [新增] CoVe 自检追加
    pre_tool_call: true                      # [现有] 不变
    transform_llm_output: true               # [现有] 不变
  context_facts:
    max_facts_per_injection: 5               # 单次最多注入几条事实
    sources:                                 # 检索源
      - rules
      - memory
      - soul
  material_prefetch:
    max_urls: 3                              # 单次最多预拉取几个 URL
    max_search_results: 3                    # web_search 最多几条
    token_budget: 2000                       # 预拉取总字符上限
    timeout: 10                              # web_extract 超时秒数
```

---

## 五、实现步骤与估时

### Phase 1: 路 1 — 上下文事实注入

| # | 步骤 | 内容 | 估时 |
|:--:|------|------|:--:|
| 1.1 | 实体字典 | 在 `__init__.py` 中加入 `_ENTITY_PATTERNS` 字典 + `_extract_entities()` | 10min |
| 1.2 | 规则检索 | 实现 `_query_rules()`，扫描 rules/ 四个子目录 | 15min |
| 1.3 | Memory 检索 | 实现 `_query_memory()` + `_query_memory_file()` 降级路径。需先 `find ~/.hermes -name "*.py" | xargs grep -l "def.*memory\|class.*Memory"` 确认 memory API 签名 | 20min |
| 1.4 | SOUL 检索 | 实现 `_query_soul()`，段落拆分匹配 | 10min |
| 1.5 | 组装注入 | 实现 `_format_facts()` + `_inject_context_facts()` + session dedup | 15min |
| 1.6 | 配置开关 | 实现 `_context_facts_enabled()` + `_load_context_facts_config()` | 5min |
| 1.7 | 集成 | 修改 `_pre_llm_call`，在第 4 步后插入事实注入调用 | 5min |
| | **Phase 1 合计** | | **~80min** |

### Phase 2: 路 2 — 素材自动预拉取

| # | 步骤 | 内容 | 估时 |
|:--:|------|------|:--:|
| 2.1 | URL 提取 | 实现 `_extract_urls()` + `_URL_PATTERN` | 5min |
| 2.2 | 事实检测 | 实现 `_detect_fact_query()` + 正负模式字典 | 10min |
| 2.3 | URL 拉取 | 实现 `_fetch_urls()` + `_fetch_urls_hermes()` + `_fetch_urls_direct()` 三路径降级 | 25min |
| 2.4 | 搜索拉取 | 实现 `_fetch_search()` + `_fetch_search_hermes()` + `_fetch_search_direct()` 三路径降级 | 25min |
| 2.5 | 组装注入 | 实现 `_format_prefetch()` + `_prefetch_materials()` + 会话缓存 | 15min |
| 2.6 | 配置开关 | 实现 `_material_prefetch_enabled()` + `_load_prefetch_config()` | 5min |
| 2.7 | 集成 | 修改 `_pre_llm_call`，在第 5 步后插入预拉取调用 | 5min |
| | **Phase 2 合计** | | **~90min** |

### Phase 3: CoVe 薄层

| # | 步骤 | 内容 | 估时 |
|:--:|------|------|:--:|
| 3.1 | 事实检测 | 实现 `_detect_fact_claims()` + 模式字典 | 10min |
| 3.2 | CoVe 追加 | 实现 `_append_cove_prompt()` | 10min |
| 3.3 | 集成 | 修改 `_post_llm_call`，在第 3 步后追加 CoVe 调用 | 5min |
| 3.4 | 验证语义 | 确认 Hermes post_llm_call 返回 str 是替换还是追加——通过 grep Hermes 源码确认 | 10min |
| | **Phase 3 合计** | | **~35min** |

### Phase 4: 测试 & 文档

| # | 步骤 | 内容 | 估时 |
|:--:|------|------|:--:|
| 4.1 | API 验证 | `grep -r "def extract\|def web_extract\|def search\|search_memory" ~/.hermes/` 确认内部 API 存在性和签名 | 15min |
| 4.2 | 功能测试 | 重启 Hermes → 逐项验证 7 个场景（见下方验收标准） | 30min |
| 4.3 | 性能测试 | 确认 pre_llm_call 增量 < 2s（web_extract 有时延） | 10min |
| 4.4 | config 更新 | 用户粘贴 config 块到 config.yaml | 5min |
| 4.5 | CHANGELOG | sentinel CHANGELOG 追加 v1.4.0 | 5min |
| 4.6 | 坑点追加 | CMG SKILL.md 追加坑点 35：防幻觉增强（可选） | 10min |
| 4.7 | 桌面包 | 6 组件重新打包 ZIP | 5min |
| 4.8 | GitHub | 推送 | 5min |
| | **Phase 4 合计** | | **~85min** |

**总估时：~290min（约 5 小时）**

---

## 六、验收标准（7 项）

| # | 测试场景 | 预期结果 | 验证方法 |
|:--:|------|------|------|
| 1 | 用户说"用 Tavily 搜一下" | LLM 上下文出现"用户偏好 Tavily 而非 Firecrawl" | 查 Hermes 日志或 LLM 实际收到的上下文 |
| 2 | 用户消息含 URL | web_extract 被调用，内容注入；失败则标注"无法访问" | terminal log 确认 |
| 3 | 用户问"Python 3.13 有什么新特性" | web_search 被触发 | terminal log 确认 |
| 4 | 用户说"去吧" | 不触发任何搜索/拉取（闲聊放行） | 确认无 web_search 调用日志 |
| 5 | LLM 输出含事实主张（数字、日期、断言） | 末尾追加 CoVe 自检提示 | 实际对话中看到 CoVe 追加文本 |
| 6 | 同一会话第二次提到"Tavily" | 不重复注入相同事实（dedup 生效） | 上下文只出现一次事实注入 |
| 7 | 关闭 `pre_llm_call_material_prefetch: false` 后重启 | 不再做 URL 预拉取和搜索 | 确认无 web_extract/web_search 调用 |

---

## 七、延期事项（现在不做 ≠ 永远不做）

以下每一项的"不做"仅针对 v1.4.0——原因、前置条件、后续版本规划全部列清。

### 7.1 strict 模式（无日志直接丢弃输出）

**当前不做原因：** 检测覆盖面不够。post_llm_call 的证据校验只做模式匹配，不做语义真假判断。覆盖面不够时 strict 会误杀正确答案——比漏拦更糟。

**前置条件：**
- 路 1（事实注入）+ 路 2（素材预拉取）跑稳 ≥ 2 周
- false_positive_rate < 10%（evidence check + external-claims 合计误报率）
- 至少 50+ 次真实拦截记录（样本量够大才有统计意义）

**后续方向：**
- 满足前置条件后，加 strict 开关（`post_llm_call_strict: true`）
- strict 开启后：evidence check 失败 → 丢弃输出 + 返回 "[CMG-STRICT] 无行为日志，输出已丢弃"
- 与现有 soft 模式并行（用户可选）

**目标版本：** sentinel v1.5.0 或 v1.6.0

---

### 7.2 独立 RAG 知识库

**当前不做原因：** 需要新存储引擎（embedding + 向量索引 + 检索管线），工程量≈ Phase 1-4 总和。v1.4.0 先用现有 infrastructure（rules/ 目录 + memory JSON + SOUL.md 段落匹配）。

**前置条件：**
- 路 1 事实注入的 memory/rules/SOUL 三源检索已经跑稳，证明了"上下文注入能降低幻觉"这个假设
- 用户反馈现有 memory 检索命中率不够（噪声多、漏检多）
- 确认 Hermes 环境有可用的 embedding 服务（本地 Ollama embedding 或 API）

**后续方向：**
- 新增 `memory_index/` 目录，存储 embedding + faiss/chromadb 索引
- 语义检索替代关键词匹配（"用户不喜欢花钱" → 能匹配到"对 token 成本敏感，能省的绝不浪费"）
- CMG rules/ 目录也入索引（规则语义检索）

**目标版本：** sentinel v2.0

---

### 7.3 多 Agent 验证（生成-验证分离）

**当前不做原因：** token 翻倍。用户 memory 明确记录"对 token 成本敏感，能省的绝不浪费"。个人用户场景下，翻倍 token = 翻倍费用，不是小数目。

**前置条件：**
- Hermes 支持用本地免费模型（Ollama qwen2.5:3b）做验证 Agent，不消耗云端 token
- 或者用户主动说"可以接受 token 翻倍"
- delegate_task 子 Agent 支持只返回验证结果（通过/不通过 + 理由），不返回全量上下文

**后续方向：**
- post_llm_call 检测到事实性输出 → 自动 spawn 验证子 Agent
- 子 Agent 逐条核对：原文摘录是否真实？数据是否可追溯？逻辑是否自洽？
- 验证不通过 → 主 Agent 重生成（只重试一次，不循环）

**目标版本：** 条件满足后再规划，不设固定版本

---

### 7.4 双模型自动分流

**当前不做原因：** 模型选择是 Hermes router/provider 层的事，sentinel 是 plugin 层——插件管不到上游选哪个模型。

**前置条件：**
- Hermes 暴露模型路由 hook（类似 `pre_model_select` 或请求级 provider override）
- 或者 Hermes 支持 per-message model switching（用户消息层面切换）

**后续方向：**
- sentinel 检测到事实性问答 → 标记 `suggest_model: "claude-sonnet-4"` 或 `suggest_provider: "deepseek"`
- Hermes 读取标记自动切换低幻觉模型
- 闲聊/创意消息继续用便宜模型

**归属：** 这个功能的行为定义属于 sentinel（检测+标记），执行属于 Hermes 内核（模型切换）。如果 Hermes 不暴露接口，CMG 做不了。

---

### 7.5 思考链强制外化

**当前不做原因：** LLM 推理过程是黑盒（坑点 29 / 豆包方案 4）。Hermes 钩子全部在输出层和动作层——`pre_llm_call`（输入前）、`post_llm_call`（输出后）、`pre_tool_call`（动作前）——没有一个钩子能干预模型内部的概率推理。

**前置条件：**
- Hermes 内核支持 `thinking` 模式（类似 Claude 的 extended thinking 或 DeepSeek 的 deep think）
- 且该 thinking 内容对 hook 可见（可以注入、修改、验证）

**后续方向：**
- 如果 Hermes 支持 thinking hook → sentinel 可以在 thinking 阶段注入"请验证以下事实"的提示
- 但即使如此，也只是引导，不是强制——模型仍可能在 thinking 中自我欺骗
- DeepSeek/豆包 都确认：这是技术边界，不是设计缺陷

**归属：** 不是 CMG 能做主的事。Hermes 支持后再规划。

---

### 7.6 对话记忆轻量化 + 时序分段

**当前不做原因：** 这是 Hermes memory 系统的基础设施——如何存储、检索、分段、压缩历史对话。CMG 的角色是**消费** memory（读），不是**改造** memory（写/重构）。

**前置条件：**
- Hermes memory 系统支持分段标记（session 内 time labels）
- 或者 Hermes 提供 memory compaction hook（CMG 可介入压缩策略）

**后续方向：**
- 如果 Hermes 暴露 memory compaction hook → sentinel 可以定义"保留规则/偏好条目、丢弃纯闲聊"的压缩策略
- 不改造 memory 存储格式——那是 Hermes 的事

**归属：** Hermes 基础设施。CMG 可以提需求，但不能自己动手改。不是 CMG 范围。

---

## 八、风险与缓解

| # | 风险 | 概率 | 影响 | 缓解 |
|:--:|------|:--:|:--:|------|
| 1 | **hermes_cli.tools.web 不存在**，无法从插件调 web_extract | 中 | 路2 核心功能不可用 | 三路径降级（hermes→requests→失败报告）。至少能标注"无法访问" |
| 2 | **hermes_cli.memory API 不存在** | 中 | 路1 memory 检索不可用 | 两路径降级（API→直接读 JSON 文件） |
| 3 | web_extract 超时导致 pre_llm_call 整体延迟 > 5s | 低 | 用户感知响应变慢 | timeout=10s 硬上限；超时降级为错误标注不阻塞 |
| 4 | 事实性提问启发式误判，闲聊触发搜索 | 中 | 浪费搜索额度 | 否定模式优先（先排除闲聊），正向模式偏保守 |
| 5 | CoVe 提示在 post_llm_call 替换模式下吞掉原输出 | 低 | 用户看不到模型回答 | 实现时保留原输出+追加（`response_text + cove_prompt`） |
| 6 | 新代码引入 bug 影响现有 4 个 core hook | 低 | 黑名单/sentinel/step-check/completion-evidence 失效 | 每个新功能独立开关（`context_facts`/`material_prefetch`/`cove`），出问题单路关闭 |
| 7 | session dedup 内存泄漏（长会话累积大量事实 dedup key） | 极低 | 内存微量增长 | `_FACTS_INJECTED` dict 的 set 只存 80-char key，100 条才 8KB |

---

## 九、关键待确认项（Phase 4 第一步）

以下 4 项在开始编码前必须验证，否则可能写一堆调不通的代码：

| # | 待确认 | 验证命令 |
|:--:|------|------|
| 1 | Hermes 是否暴露 web_extract Python API | `grep -r "def extract\|def web_extract\|class.*WebExtract" ~/.hermes/` |
| 2 | Hermes 是否暴露 web_search Python API | `grep -r "def.*search\|def.*web_search\|class.*WebSearch" ~/.hermes/` |
| 3 | Hermes 是否暴露 memory search API | `grep -r "def.*memory.*search\|def.*search_memory\|class.*Memory" ~/.hermes/` |
| 4 | post_llm_call 返回 str 是替换还是追加 | 查 Hermes 文档或源码 hook 处理逻辑 |

如果 1-3 全部不可用，路 2 退化为纯 requests 路径（仍然可用，只是多一个外部依赖）。路 1 memory 退化为文件读取（仍然可用）。

---

## 十、版本发布流程

1. 实现 Phase 1-3 → 本地 `__init__.py` 修改完成
2. Phase 4 API 验证 → 确认降级路径有效
3. 功能测试 → 7 项验收全部通过
4. `__init__.py` 头部 docstring 更新为 `v1.4.0`
5. 用户粘贴 config 块到 `~/.hermes/config.yaml`
6. 重启 Hermes
7. 功能验证（验收标准 1-7 复测）
8. CHANGELOG 追加
9. CMG SKILL.md 可选追加坑点 35
10. 桌面包重建（6 组件 ZIP）
11. GitHub 推送
