# 🔍 medpatent: Search Playbook & Traceability

Standards for patent searching, prior art identification, and result logging.

## 🚩 Rule 1: Query Traceability
- **MANDATORY**: Log every search query, database, and date.
- **MANDATORY**: Use systematic Boolean search clusters (e.g., `(device OR robot) AND (force feedback OR haptic)`).

## 🚩 Rule 2: Anti-Hallucination
- **Never cite a patent number you haven't directly confirmed from a tool output.**
- **MANDATORY**: If no results are found, report "0 results". Do NOT synthesize.

## 🚩 Rule 3: Relevance Check
- Extract IPC/CPC codes (e.g., `A61B 34/30` for robotic surgery) to narrow searches.
- Compare candidates to the core technical problem defined in Step 1.

## 🚩 Rule 4: Data Hand-off & Tooling

### Lens.org API（主推，结构化检索 + 全文下载）
- **API Setup**: 在 `.env` 中配置 `LENS_API_KEY=your_token` 后，运行：
  ```bash
  python .agents/skills/lens-patent-search/scripts/lens_search.py "query" --limit 20
  ```
- **全文下载**: 检索后通过以下命令批量下载 Markdown 全文：
  ```bash
  python .agents/skills/lens-patent-search/scripts/lens_download.py \
    --from-results .agents/harness/data/search_results/lens_latest.json --top 20
  ```
- **分析摘要**: 生成申请人/CPC/年份分布报告，并输出 `patent-claims-analyzer` 兼容 CSV：
  ```bash
  python .agents/skills/lens-patent-search/scripts/lens_analyze.py \
    --from-results lens_xxx.json --output-report doc/analysis/report.md --output-csv claims.csv
  ```
- **Pre-Classification Delivery**: Markdown 文件自动存入 `downloaded_patents/{JUR}/` 子目录。

### Valyu API（备选，语义检索）
- **API Setup**: Ensure the Valyu API key is configured (`node search.mjs setup <key>`) prior to executing `patents-search`.
- **Results Extraction**: For Windows environments without `jq`, parse the JSON arrays using PowerShell: `Get-Content <file.json> | ConvertFrom-Json` to extract required `cpc_classifications` and `patent_number`.
- **Pre-Classification Delivery**: Automatically export the full patent content to individual Markdown files (e.g., `doc/downloaded_patents/[PatentID].md`) so that they can be digested systematically by the examiner skill.

## 📓 Search Log Template
```markdown
### 🕵️ Search Trace [Date: YYYY-MM-DD]
- **Tool**: `patents-search` (Valyu)
- **Query**: "Da Vinci 5 robotic surgery haptic feedback"
- **Hits**: 15
- **Top 3 Relevance**: [US123A](link), [EP456B](link), [WO789C](link)
```


# 🔍 medpatent：搜索指南与可追溯性
专利检索标准、现有技术识别标准以及结果记录标准。
## 🚩 规则 1：查询可追溯性
- **强制要求**：记录每一次搜索查询、所使用的数据库以及具体日期。
- **强制要求**：采用系统的布尔搜索组合方式（例如，“（设备 或 机器人）AND（力反馈 或 感觉）”）。
## 🚩 规则 2：防止幻觉
- **绝对禁止**：切勿引用您未直接从工具输出中确认的专利编号。
- **强制要求**：若未找到任何结果，请报告“0 个结果”。切勿进行合成操作。
## 🚩 规则 3：相关性检查
- 提取 IPC/CPC 编码（例如，机器人手术的编码为 `A61B 34/30`）以缩小搜索范围。
- 将候选选项与步骤 1 中定义的核心技术问题进行比较。
## 🚩 规则 4：数据交接与工具使用
- **API 配置**：在执行 `patents-search` 前，请先配置 Valyu API 密钥（使用命令 `node search.mjs setup <key>`）。
- **结果提取**：对于没有 `jq` 的 Windows 环境，可以使用 PowerShell 来解析 JSON 数组：`Get-Content <file.json> | ConvertFrom-Json` 以提取所需的 `cpc_classifications` 和 `patent_number`。
- **预分类交付**：自动将完整的专利内容导出到单独的 Markdown 文件中（例如，`doc/downloaded_patents/[PatentID].md`），以便考官能够系统地对其进行理解。
## 📚 搜索日志模板
```markdown
### 🌟 搜索记录 [日期：YYYY-MM-DD]
- **工具**：`patents-search`（Valyu）
- **查询**：“达芬奇 5 机器人手术触觉反馈”
- **匹配结果**：15 个
- **最相关前三条**：[US123A](链接)，[EP456B](链接)，[WO789C](链接)```