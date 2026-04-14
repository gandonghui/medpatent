# 📓 medpatent: Hallucination & Traceability Ledger

Track errors in AI agent logic, hallucinated prior art, and tracing failures here.

## 🚩 Hallucination Patterns
- [ ] Example: Fictional Publication Numbers (AI inventing non-existent patents).
- [ ] Example: False Citations (Attributing a feature to a patent that doesn't say it).

## 🧩 Step Failure Diary
| Date | Domain | Failure Case | Fix/Mitigation |
|------|--------|--------------|----------------|
| 2026-04-14| Search | Initial setup | Define `search_playbook.md` rules. |
| 2026-04-14| Search | Agent hit blocker due to unconfigured Valyu API Key. | Updated `search_playbook` with Rule 4 (API pre-setup check). |
| 2026-04-14| Search | BigQuery 403: Missing `cloud-platform` scope in ADC. | Use `gcloud auth application-default login --scopes=https://www.googleapis.com/auth/cloud-platform`. |
| 2026-04-14| Search | BigQuery 400: SQL schema mismatch (inventor array vs record). | Verify current table schema (e.g. `inventor` vs `inventor_harmonized`) before assuming record fields like `.name`. |
| 2026-04-14| Search | UnicodeDecodeError: PowerShell outputting UTF-16 BOM by default. | Use `encoding='utf-8-sig'` in Python and pipe with `Out-File -Encoding utf8`. |
| 2026-04-14| Classification | Disconnect between Search output and Classification step. | Enforced use of `patent-examiner` skill and added unified template in `classification_guidelines.md`. |
| 2026-04-14| Data | Improper file naming (no country/kind) in legacy extraction. | Standardized on `country_number_kind.md` and moved malformed files to `review_required/`. |
| 2026-04-14| Data | Missing metadata in downloads (name only extraction). | Updated `unify_patent_names.py` with defensive logic to quarantine files missing bibliographic data. |

## 🛡️ Corrective Guardrails
- **MANDATORY**: Valid publication number format validation (`US\d{7,8}[A-Z]\d`).
- **MANDATORY**: For every claim, point to a specific column and line range.
- **MANDATORY**: If the Valyu/Google Patents API returns no results, state "No results found" explicitly.
