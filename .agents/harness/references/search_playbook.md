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
- **API Setup**: Ensure the Valyu API key is configured (`node search.mjs setup <key>`) or BigQuery is authenticated (`gcloud auth application-default login --scopes=https://www.googleapis.com/auth/cloud-platform`).
- **Results Extraction**: For Windows environments without `jq`, parse JSON using PowerShell: `Get-Content -Encoding utf8 .agents/harness/data/search_results/bq_results.json | ConvertFrom-Json`. Alternatively, use the centralized harness script: `python ../scripts/unify_patent_names.py`.
- **Character Encoding Safety**: **MANDATORY**: When piping from PowerShell to files, use `-Encoding utf8`. When reading in Python, use `utf-8-sig` to handle potential BoMs to prevent `UnicodeDecodeError`.
- **Pre-Classification Delivery**: Automatically export the full patent content to individual Markdown files (e.g., `downloaded_patents/[PatentID].md`) using `.agents/skills/bigquery-patent-search/scripts/download_full_patents.py`.

## 📓 Search Log Template
```markdown
### 🕵️ Search Trace [Date: YYYY-MM-DD]
- **Tool**: `patents-search` (Valyu)
- **Query**: "Da Vinci 5 robotic surgery haptic feedback"
- **Hits**: 15
- **Top 3 Relevance**: [US123A](link), [EP456B](link), [WO789C](link)
```
