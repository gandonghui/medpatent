import json
import csv
import re
from pathlib import Path

# Paths (Relativized)
BASE_DIR = Path(__file__).parent
SOURCE_JSON = BASE_DIR / ".agents" / "harness" / "data" / "search_results" / "lens_full_report_20260419_182653.json"
DOWNLOAD_DIR = BASE_DIR / "downloaded_patents"
OUTPUT_CSV = BASE_DIR / "doc" / "analysis" / "intuitive_vision_full_claims_all.csv"
OUTPUT_REPORT = BASE_DIR / "doc" / "analysis" / "intuitive_vision_full_report_all.md"

def extract_claim_texts(obj):
    """Recursively find all claim_text lists in nested Lens JSON."""
    texts = []
    if isinstance(obj, dict):
        if "claim_text" in obj and isinstance(obj["claim_text"], list):
            texts.extend(obj["claim_text"])
        for v in obj.values():
            texts.extend(extract_claim_texts(v))
    elif isinstance(obj, list):
        for item in obj:
            texts.extend(extract_claim_texts(item))
    return texts

def is_independent(text):
    """Smarter detection of independent claims."""
    if not re.match(r"^\s*\d+\.", text):
        return False
    text_lower = text.lower()
    if re.match(r"^\s*1\.", text):
        return True
    snippet = text_lower[:200]
    dependency_markers = ["claim of", "claim 1", "claim 2", "according to claim", "as claimed in"]
    for marker in dependency_markers:
        if marker in snippet:
            return False
    return True

def main():
    # 1. Load Local IDs
    purified_ids = set()
    for md_file in DOWNLOAD_DIR.rglob("*.md"):
        content = md_file.read_text(encoding='utf-8', errors='replace')
        m_id = re.search(r"\*\*Lens ID\*\*\s*\|\s*`([^`]+)`", content)
        if m_id:
            purified_ids.add(m_id.group(1))
    print(f"Found {len(purified_ids)} purified IDs in {DOWNLOAD_DIR}")

    # 2. Load JSON
    with open(SOURCE_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    all_patents = data.get("raw", {}).get("data", [])

    csv_data = []
    for p in all_patents:
        lens_id = p.get("lens_id", "N/A")
        # FILTER ONLY PURIFIED PATENTS
        if lens_id not in purified_ids:
            continue

        biblio = p.get("biblio", {})
        pub_ref = biblio.get("publication_reference", {})
        
        jur = pub_ref.get("jurisdiction", "N/A")
        doc_num = pub_ref.get("doc_number", "N/A")
        kind = pub_ref.get("kind", "N/A")
        pub_key = f"{jur}-{doc_num}-{kind}"
        pub_date = pub_ref.get("date", "N/A")
        
        # Title logic
        titles = biblio.get("invention_title", [])
        title = next((t.get("text") for t in titles if t.get("lang") == "en"), "N/A")
        if title == "N/A" and titles: title = titles[0].get("text", "N/A")
        
        # Applicants
        applicants = [a.get("extracted_name", {}).get("value") for a in biblio.get("parties", {}).get("applicants", [])]
        app_str = "; ".join(filter(None, applicants)) if applicants else "N/A"
        
        # CPC
        cpc_raw = biblio.get("classifications_cpc", [])
        if isinstance(cpc_raw, dict): cpc_raw = cpc_raw.get("classifications", [])
        cpcs = [c.get("symbol") for c in (cpc_raw if isinstance(cpc_raw, list) else []) if isinstance(c, dict) and c.get("symbol")]
        cpc_str = " | ".join(cpcs) if cpcs else "N/A"

        # Claims
        claims_raw = p.get("claims", [])
        all_texts = extract_claim_texts(claims_raw)
        unique_claims = []
        seen = set()
        for t in all_texts:
            if t and t.strip() and t not in seen:
                unique_claims.append(t.strip())
                seen.add(t)
        
        claim_count = len(unique_claims)
        ind_claim_count = sum(1 for c in unique_claims if is_independent(c))
        
        if claim_count == 0:
            raw_text = claims_raw[0].get("text", "") if (isinstance(claims_raw, list) and claims_raw) else ""
            if raw_text:
                matches = re.findall(r"(?m)^\s*\d+\.", raw_text)
                claim_count = len(matches)
                ind_claim_count = 1 if claim_count > 0 else 0

        if lens_id == "190-841-018-116-930":
            print(f"VERIFICATION: WO-2025198970-A1 -> Claims: {claim_count}, Ind: {ind_claim_count}")

        csv_data.append({
            "lens_id": lens_id,
            "pub_key": pub_key,
            "jurisdiction": jur,
            "date_published": pub_date,
            "title": title,
            "applicants": app_str,
            "cpc_codes": cpc_str,
            "claim_count": claim_count,
            "independent_claim_count": ind_claim_count,
            "has_full_text": "Yes" if claim_count > 0 else "No"
        })

    # Sort CSV by date descending
    csv_data.sort(key=lambda x: x["date_published"], reverse=True)

    # 1. Write CSV
    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
        writer.writeheader()
        writer.writerows(csv_data)
    print(f"Final Purified CSV ({len(csv_data)} rows) written to {OUTPUT_CSV}")

    # 2. Write Report
    total_patents = len(csv_data)
    with_full_text = sum(1 for x in csv_data if x["has_full_text"] == "Yes")
    
    report_content = f"""# Intuitive Surgical 视觉系统专利深度分析报告 (最终净化版)

## 1. 项目数据统计 (Project Statistics)

- **提纯核心专利数**: {total_patents}
- **包含全文/权利要求件数**: {with_full_text}
- **数据来源**: Lens.org Authority JSON (固化版本)
- **更新日期**: 2026-04-21

## 2. 核心专利清单 (最新排序)

| 公开号 | 标题 | 权利要求数 | 独立项 | CPC 分类 |
|--------|------|------------|--------|----------|
"""
    for d in csv_data:
        report_content += f"| {d['pub_key']} | {d['title'][:60]}... | {d['claim_count']} | {d['independent_claim_count']} | `{d['cpc_codes'][:40]}...` |\n"

    report_content += """
---
*提示：本报告仅包含已存入 /downloaded_patents/ 目录的提纯专利，已剔除无关噪声数据。*
"""
    OUTPUT_REPORT.write_text(report_content, encoding='utf-8')
    print(f"Final Purified Report updated at {OUTPUT_REPORT}")

if __name__ == "__main__":
    main()
