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
| 2026-04-27| Classification | Semantic Drift (Mechanical hallucinated as AI). Case: US9283050B2. | Implemented **Collision Protocol** (Evidence Triplet + CPC Audit). |
| 2026-04-27| Pipeline | Data Integrity failure (81 patents dropped to 59, missing baselines). | Implemented **Rigid Pipeline** (Python deduplication + Baseline verification). |

## 🛡️ Corrective Guardrails
- **MANDATORY**: Valid publication number format validation (`US\d{7,8}[A-Z]\d`).
- **MANDATORY**: For every claim, point to a specific column and line range.
- **MANDATORY**: If the Valyu/Google Patents API returns no results, state "No results found" explicitly.



# 📝 medpatent：幻觉与可追溯性账本
检查人工智能代理逻辑中的错误、虚幻的先前研究成果以及追踪失败情况。
## 🚩 幻觉模式
- [ ] 示例：虚构的专利编号（人工智能创造出不存在的专利）。
- [ ] 示例：虚假引用（将一项功能归功于某项专利，而该专利并未提及此内容）。
## 🧩 步骤失败日志
| 日期 | 领域 | 失败案例 | 修复/缓解措施 ||------|--------|--------------|----------------|
| 2026 年 4 月 14 日 | 搜索 | 初始设置 | 定义 `search_playbook.md` 文件中的规则。|
| 2026-04-14 | 搜索 | 代理因未配置 Valyu API 密钥而被阻止。 | 将 `搜索脚本` 更新为第 4 条规则（API 预设置检查）。|
| 2026-04-14 | 分类 | 搜索结果与分类步骤之间存在脱节。 | 强制使用“专利审查员”技能，并在“分类指南.md”中添加了统一模板。|
| 2026-04-27 | 分类 | 语义漂移（机械专利幻觉为 AI）。案例：US9283050B2。 | 实施**冲突对撞协议**（证据三元组 + CPC 审计）。|
| 2026-04-27 | 管道 | 数据完整性故障（81 件专利丢失至 59 件，遗漏基准）。 | 实施**刚性管道**（Python 去重 + 基准验证）。|

## 🛡️ 补救性防护栏
- **必填项**：有效的出版编号格式验证（“US\d{7,8}[A-Z]\d”）。
- **必填项**：对于每一项声明，需指明具体的列和行范围。
- **必填项**：如果 Valyu/谷歌专利 API 没有返回任何结果，请明确指出“未找到结果”。