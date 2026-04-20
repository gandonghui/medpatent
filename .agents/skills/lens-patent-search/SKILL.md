---
name: lens-patent-search
description: >
  Lens.org API 专利检索、元数据分析与全文下载 skill。
  覆盖完整三步工作流：① 多字段检索（关键词/CPC/申请人/日期/管辖区）
  → ② 结构化分析摘要（申请人分布、CPC热力、年份趋势、权利要求统计）
  → ③ 全文下载为标准 Markdown（自动存入 downloaded_patents/ 按管辖区分目录）。
  当用户需要"用 Lens.org 搜专利"、"检索先前技术"、"下载专利全文"、
  "分析专利申请人分布"、"批量下载专利"、"做专利景观分析"等任务时，
  立即使用此 skill。也适用于从已有检索结果 JSON 批量下载或分析的场景。
tools: Bash, Read, Write
model: sonnet
---

# Lens.org Patent Search Skill

Lens.org 是覆盖全球 1.2 亿+ 专利的开放平台，提供完整专利元数据、
权利要求全文和专利族信息。本 skill 封装了三个核心脚本，
遵循 `search_playbook.md` 的可追溯性与防幻觉要求。

> **前置检查**（每次使用前）:
> 1. 查阅 `../.harness/FAULT_DIARY.md` 了解已知问题
> 2. 确认 `.env` 中已配置 `LENS_API_KEY`（见下方 Setup）
> 3. 确认当前角色为 **Patent Researcher（专利检索专家）**

---

## ⚙️ Setup：API Key 配置

将以下内容添加到项目根目录的 `.env` 文件：

```
LENS_API_KEY=your_token_here
```

API Token 申请地址（免费学术账号）:
https://www.lens.org/lens/user/subscriptions

配置后，三个脚本均可自动读取，无需手动传参。

---

## 🔄 三步工作流

```
① 检索  →  ② 分析摘要  →  ③ 全文下载
```

**路径约定**（相对于 `medpatent/` 根目录）:
- 检索结果 JSON → `.agents/harness/data/search_results/lens_YYYYMMDD_HHMMSS.json`
- 下载的专利全文 → `downloaded_patents/{JUR}/JUR_NUMBER_KIND.md`
- 分析报告 → 由用户指定，或打印到终端

---

## 步骤一：检索 `lens_search.py`

### 基本用法

```bash
cd medpatent/

# 关键词检索（支持 AND/OR/NOT 布尔操作符）
python .agents/skills/lens-patent-search/scripts/lens_search.py \
  "surgical robot AND haptic feedback" \
  --limit 30

# 限定管辖区 + CPC 代码
python .agents/skills/lens-patent-search/scripts/lens_search.py \
  "endoscope imaging" \
  --cpc A61B1/00 A61B34/30 \
  --jurisdiction US EP \
  --limit 50

# 日期范围 + 申请人
python .agents/skills/lens-patent-search/scripts/lens_search.py \
  "robotic surgery" \
  --assignee "Intuitive Surgical" \
  --date-from 2018-01-01 --date-to 2024-12-31 \
  --limit 20

# 只输出 lens_id 列表（用于后续批量下载）
python .agents/skills/lens-patent-search/scripts/lens_search.py \
  "da vinci robot endoscope" --limit 20 --ids-only
```

### 高级：自定义 DSL 查询体

当需要复杂嵌套查询时，将 Lens.org Boolean DSL 写入 JSON 文件：

```json
{
  "query": {
    "bool": {
      "must": [
        {"query_string": {"query": "laparoscopic OR endoscopic", "fields": ["title","abstract"]}},
        {"terms": {"jurisdiction": ["US","EP"]}}
      ],
      "filter": [
        {"range": {"date_published": {"gte": "2020-01-01"}}}
      ]
    }
  }
}
```

```bash
python .agents/skills/lens-patent-search/scripts/lens_search.py \
  --query-file my_query.json --limit 100
```

### 检索结果格式

结果自动保存为 `.agents/harness/data/search_results/lens_YYYYMMDD_HHMMSS.json`，
包含原始 API 响应和检索元数据（时间戳、查询词、过滤条件）——满足
`search_playbook.md Rule 1（查询可追溯性）`。

---

## 步骤二：分析摘要 `lens_analyze.py`

### 从检索结果 JSON 分析

```bash
python .agents/skills/lens-patent-search/scripts/lens_analyze.py \
  --from-results .agents/harness/data/search_results/lens_20260419_103000.json \
  --output-report doc/analysis/lens_report.md \
  --output-csv doc/analysis/lens_claims.csv
```

### 从已下载 Markdown 目录分析

```bash
python .agents/skills/lens-patent-search/scripts/lens_analyze.py \
  --from-dir downloaded_patents/ \
  --output-report doc/analysis/landscape_report.md
```

### 分析报告内容

报告包含：
- 申请人分布 TOP 15（横向条形图，ASCII 渲染）
- CPC 主分组热力分布 TOP 15
- 年份趋势
- 管辖区分布
- 权利要求平均数 & 独立项统计
- 专利明细表（前 50 条）

输出的 `--output-csv` 兼容 `patent-claims-analyzer` skill，
可直接作为其输入进行深度权利要求解析。

---

## 步骤三：全文下载 `lens_download.py`

### 下载单个或多个专利

```bash
# 下载单个（lens_id 格式）
python .agents/skills/lens-patent-search/scripts/lens_download.py \
  031-720-013-543-533

# 批量下载（多个 lens_id）
python .agents/skills/lens-patent-search/scripts/lens_download.py \
  031-720-013-543-533 086-163-927-682-451 191-452-827-316-092
```

### 从检索结果批量下载

```bash
# 从上一步的 JSON 结果取前 20 条下载全文
python .agents/skills/lens-patent-search/scripts/lens_download.py \
  --from-results .agents/harness/data/search_results/lens_20260419_103000.json \
  --top 20
```

### 输出文件规范

文件按管辖区分子目录存放，命名与项目现有规范一致：

```
downloaded_patents/
├── US/
│   └── US_10123456_B2.md
├── EP/
│   └── EP_2470089_A1.md
├── CN/
│   └── CN_102596062_B.md
└── WO/
    └── WO_2021_054321_A1.md
```

每个 Markdown 文件包含：基本信息表、申请人、CPC/IPC 代码、
摘要（中英文）、**完整权利要求**、说明书全文（如 Lens.org 有收录）。

---

## 🔗 与其他 Skills 的衔接

| 下一步操作 | 使用的 Skill |
|-----------|-------------|
| 解析权利要求为独立/从属分类 | `patent-claims-analyzer` |
| 35 USC 合规审查 | `patent-examiner` |
| 撰写新专利申请 | `patent-application-creator` |
| 中国专利申请表格 | `patent-architect` |

**数据流**:

```
lens_search.py ──JSON──▶ lens_analyze.py ──CSV──▶ patent-claims-analyzer
                │
                └──lens_ids──▶ lens_download.py ──MD──▶ patent-examiner
```

---

## 🚩 防幻觉 & 可追溯性规则

遵循 `search_playbook.md` 的以下规则（对 Lens.org 来说同样适用）：

1. **Rule 1（可追溯性）**: 每次检索的 JSON 结果文件即为查询证据，
   引用专利时必须附带文件名和 lens_id。
2. **Rule 2（防幻觉）**: 所有专利编号来自 API 实际返回，禁止推测或合成。
3. **Rule 2（零结果处理）**: 如果检索返回 0 条，如实报告"未找到结果"，
   调整关键词后重试，不得凭空捏造专利。
4. **Rule 3（相关性校验）**: 分析报告中的 CPC 代码需与检索目标领域一致，
   发现明显偏差时须标注并提示重新校准查询。

---

## 📂 参考文档

详细 API 字段说明和高级查询示例见：

→ `references/lens_api_reference.md`（含完整字段列表、响应结构、
  错误码说明、配额限制）
