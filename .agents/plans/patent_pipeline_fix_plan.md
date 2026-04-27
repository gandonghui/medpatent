# Implementation Plan: Patent Analysis Data Pipeline Fix

Based on your feedback, it is clear that the underlying data pipeline parsing the Lens API JSON into CSV and Markdown has issues. This plan outlines how we will fix the data source, extract standard publication numbers, and regenerate traceable reports.

## User Review Required

> [!CAUTION]
> - **File Deletion**: I will permanently delete `.md` files from `downloaded_patents/` that do not belong to Intuitive Surgical (approx. 450+ files).
> - **Overwriting**: Previous analysis reports and CSVs will be replaced with corrected versions.

## Root Cause Analysis & Proposed Changes

### 1. Dataset Contamination (521 vs 65 patents)
**Cause**: The original Lens API search was performed without a strict `applicant:(Intuitive Surgical)` Boolean filter, causing the retrieval of thousands of competitors' patents.
**Fix**: I will write a script to deeply filter the existing raw JSON file (`lens_full_report_20260419_182653.json`) to strictly extract *only* those patents where the applicant contains "Intuitive Surgical".

### 2 & 3. Useless Primary Key & Missing "公开号" (N/A)
**Cause**: The `lens_analyze.py` script has a bug. On line 103, it attempts to read a field called `pub_key` from the Lens JSON's `publication_reference` object. However, Lens.org does not provide a single `pub_key` field. Instead, it provides `jurisdiction`, `doc_number`, and `kind`. Because `pub_key` was missing, it defaulted to `"N/A"`, forcing the system to rely on the proprietary `lens_id`.
**Fix**: 
#### [MODIFY] [lens_analyze.py](file:///c:/Users/pumch/Desktop/medpatent/.agents/skills/lens-patent-search/scripts/lens_analyze.py)
I will update the script to dynamically construct the standard publication number:
```python
pub_ref = biblio.get("publication_reference", {})
jur = pub_ref.get("jurisdiction", "")
doc_num = pub_ref.get("doc_number", "")
kind = pub_ref.get("kind", "")
pub_key = f"{jur}-{doc_num}-{kind}" if jur and doc_num else "N/A"
```

### 3. File System Cleanup & Full-Text Audit
- **Cleanup**: I will cross-reference the filtered list of ~65 patents with the files in `downloaded_patents/`. Any file NOT on the list will be deleted to keep the folder clean.
- **Full-Text Audit**: I will analyze the remaining Markdown files to determine if they contain a "Description/说明书" section.
- **Reporting**: I will generate a summary table in `download_audit.md` showing:
    - Standard Publication Number
    - Title
    - Status (Full Text Available vs. Abstract Only)

### 4. Traceable Deep Dive Report
**Fix**: I will rewrite the deep dive report (`da_vinci_5_vision_deep_report.md`) to explicitly cite the standard publication numbers for every major technical claim (e.g., "Fluorescence image fusion described in US-11076922-B2").

### 5. Full-Text Limitations for CN Patents
**Cause**: This is an inherent limitation of the Lens.org global database API. While WO/US/EP full texts are usually complete, CN patents often only syndicate their abstracts/claims to the platform without full-text or diagrams.
**Recommendation**: We accept this limitation for Lens. If full CN text with images is strictly required later, we can execute a secondary run using the `patent-search-cn-us` agent skill, which is optimized for CNIPA deep retrieval.

## Verification Plan

### Automated Tests
- Run the patched `lens_analyze.py` and verify `pub_key` is a standard string (e.g., `US-11076922-B2`) in the resulting CSV, not `N/A`.
- Verify the total count in the CSV drops to only Intuitive Surgical patents (approx. 65).
- Verify the generated Deep Dive Report cites exact `[JUR]-[NUM]-[KIND]` identifiers.
