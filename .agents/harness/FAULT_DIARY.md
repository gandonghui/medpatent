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
| 2026-04-14| Classification | Disconnect between Search output and Classification step. | Enforced use of `patent-examiner` skill and added unified template in `classification_guidelines.md`. |

## 🛡️ Corrective Guardrails
- **MANDATORY**: Valid publication number format validation (`US\d{7,8}[A-Z]\d`).
- **MANDATORY**: For every claim, point to a specific column and line range.
- **MANDATORY**: If the Valyu/Google Patents API returns no results, state "No results found" explicitly.
