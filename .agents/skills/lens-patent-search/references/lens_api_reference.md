# Lens.org Patent API 参考文档

> 此文档供 `lens_search.py` 高级用法参考，以及当脚本无法满足需求时直接构造查询体使用。

## 端点

| 操作 | Endpoint | 方法 |
|------|----------|------|
| 专利检索 | `https://api.lens.org/patent/search` | POST |
| 学术文献检索 | `https://api.lens.org/scholarly/search` | POST |
| 按 lens_id 获取 | `https://api.lens.org/patent/{lens_id}` | GET |

## 认证

```
Authorization: Bearer {LENS_API_KEY}
Content-Type: application/json
```

---

## 请求体结构

```json
{
  "query":   { /* Elasticsearch-like DSL */ },
  "size":    20,           // 每页条数，最大 100
  "from":    0,            // 分页偏移
  "sort":    [{"year_published": {"order": "desc"}}],
  "include": ["lens_id", "title", ...],   // 字段白名单
  "exclude": ["description"],             // 字段黑名单（节省带宽）
  "scroll":  "1m"          // 滚动翻页（大批量 > 100 条时使用）
}
```

---

## 常用查询模式

### 1. 关键词全文检索

```json
{
  "query": {
    "query_string": {
      "query": "robotic surgery AND (haptic OR force feedback)",
      "fields": ["title", "abstract", "claims.text", "description.text"],
      "default_operator": "AND"
    }
  }
}
```

### 2. CPC 代码精确匹配

```json
{"query": {"term": {"classifications.cpc.symbol": "A61B34/30"}}}
```

### 3. CPC 代码前缀匹配（整个子类）

```json
{"query": {"prefix": {"classifications.cpc.symbol": "A61B34"}}}
```

### 4. 申请人模糊匹配

```json
{"query": {"match": {"applicants.name": "Intuitive Surgical"}}}
```

### 5. 管辖区过滤

```json
{"query": {"terms": {"jurisdiction": ["US", "EP", "CN", "WO"]}}}
```

### 6. 日期范围

```json
{
  "query": {
    "range": {
      "date_published": {
        "gte": "2020-01-01",
        "lte": "2024-12-31",
        "format": "yyyy-MM-dd"
      }
    }
  }
}
```

### 7. 复合 Bool 查询

```json
{
  "query": {
    "bool": {
      "must": [
        {"query_string": {"query": "endoscope imaging", "fields": ["title","abstract"]}},
        {"terms": {"jurisdiction": ["US","EP"]}}
      ],
      "should": [
        {"prefix": {"classifications.cpc.symbol": "A61B1"}},
        {"prefix": {"classifications.cpc.symbol": "A61B34"}}
      ],
      "filter": [
        {"range": {"date_published": {"gte": "2018-01-01"}}}
      ],
      "must_not": [
        {"term": {"publication_type": "DESIGN"}}
      ]
    }
  }
}
```

### 8. 专利族检索（Patent Family）

```json
{"query": {"term": {"families.family_id": "67890123"}}}
```

---

## include 字段完整列表

| 字段 | 说明 |
|------|------|
| `lens_id` | Lens.org 全局唯一ID |
| `title` | 标题（多语言列表） |
| `abstract` | 摘要（多语言列表） |
| `claims` | 权利要求（含 claim_sequence、claim_text、claim_type、claim_refs） |
| `description` | 说明书全文（部分专利支持） |
| `date_published` | 公开日（YYYY-MM-DD） |
| `year_published` | 公开年份 |
| `priority_date` | 最早优先权日 |
| `filing_key` | 申请号 |
| `pub_key` | 公开号（如 US_10123456_B2） |
| `jurisdiction` | 管辖区（US/EP/CN/WO 等） |
| `publication_type` | 类型（GRANTED_PATENT / PATENT_APPLICATION / DESIGN 等） |
| `applicants` | 申请人列表（含 name、country_code、type） |
| `inventors` | 发明人列表（含 name、country_code） |
| `classifications.cpc` | CPC 分类（含 symbol、version） |
| `classifications.ipc` | IPC 分类 |
| `families.family_id` | 专利族ID |
| `families.size` | 专利族规模 |
| `legal_status` | 法律状态（ALIVE/DEAD，含 patent_status） |
| `cited_by_patent_count` | 被引用次数 |
| `references_cited` | 引用的专利列表 |
| `biblio` | 完整书目信息 |

---

## 响应结构

```json
{
  "total":  {"value": 1247, "relation": "eq"},
  "data": [
    {
      "lens_id": "031-720-013-543-533",
      "pub_key": "US_10123456_B2",
      "jurisdiction": "US",
      "title": [{"lang": "en", "text": "Surgical robot system..."}],
      "abstract": [{"lang": "en", "text": "A system for..."}],
      "date_published": "2021-06-15",
      "applicants": [{"name": "Intuitive Surgical Operations", "country_code": "US"}],
      "classifications": {
        "cpc": [{"symbol": "A61B34/30", "version": "20130101"}]
      },
      "claims": [
        {
          "lang": "en",
          "claims": [
            {
              "claim_sequence": 1,
              "claim_text": "A surgical system comprising...",
              "claim_type": "independent",
              "claim_refs": []
            },
            {
              "claim_sequence": 2,
              "claim_text": "The system of claim 1, wherein...",
              "claim_type": "dependent",
              "claim_refs": [1]
            }
          ]
        }
      ],
      "legal_status": {"patent_status": "ALIVE"}
    }
  ]
}
```

---

## 错误码

| HTTP 状态 | 含义 | 处理建议 |
|-----------|------|---------|
| 400 | 查询体格式错误 | 检查 DSL 语法 |
| 401 | API Key 无效或过期 | 重新申请/检查 .env |
| 403 | 超出配额或权限不足 | 检查订阅级别 |
| 429 | 速率限制（Rate Limit） | 降低请求频率，增加延迟 |
| 500 | Lens.org 服务器错误 | 稍后重试 |

---

## 配额与限制

| 账户类型 | 每日请求数 | 每请求最大条数 | 全文访问 |
|---------|-----------|------------|---------|
| 免费学术账号 | 500 | 100 | 部分支持 |
| 高级订阅 | 无限制 | 500（scroll） | 全支持 |

> **Scroll API（>100 条批量拉取）**:
> 在请求体中加入 `"scroll": "1m"`，响应中会返回 `scroll_id`，
> 后续请求发送 `{"scroll_id": "xxx", "scroll": "1m"}` 到相同端点继续翻页。

---

## 常用 CPC 代码（医疗器械方向）

| 代码 | 描述 |
|------|------|
| `A61B34/00` | 计算机辅助手术 / 机器人手术 |
| `A61B34/30` | 外科机器人 |
| `A61B34/35` | 微创机器人 |
| `A61B1/00` | 内窥镜 |
| `A61B1/045` | 机器人内窥镜 |
| `A61B17/00` | 外科器械 |
| `A61B5/00` | 诊断设备 |
| `A61M25/00` | 导管 |
| `G06T7/00` | 图像分析（医学影像） |
| `G16H30/00` | 医疗影像 ICT |
| `G16H40/63` | 手术机器人管理系统 |
