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

## 🛡️ 补救性防护栏
- **必填项**：有效的出版编号格式验证（“US\d{7,8}[A-Z]\d”）。
- **必填项**：对于每一项声明，需指明具体的列和行范围。
- **必填项**：如果 Valyu/谷歌专利 API 没有返回任何结果，请明确指出“未找到结果”。