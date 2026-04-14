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
- **API Setup**: Ensure the Valyu API key is configured (`node search.mjs setup <key>`) prior to executing `patents-search`.
- **Results Extraction**: For Windows environments without `jq`, parse the JSON arrays using PowerShell: `Get-Content <file.json> | ConvertFrom-Json` to extract required `cpc_classifications` and `patent_number`.
- **Pre-Classification Delivery**: Automatically export the full patent content to individual Markdown files (e.g., `downloaded_patents/[PatentID].md`) so that they can be digested systematically by the examiner skill.

## 📓 Search Log Template
```markdown
### 🕵️ Search Trace [Date: YYYY-MM-DD]
- **Tool**: `patents-search` (Valyu)
- **Query**: "Da Vinci 5 robotic surgery haptic feedback"
- **Hits**: 15
- **Top 3 Relevance**: [US123A](link), [EP456B](link), [WO789C](link)
```
