# 🚦 medpatent: Progressive Context Router

**Avoid Hallucination. Stick to Atomized Steps.**
Identify the **Primary Domain** of your task and load ONLY the specified references, **Local Skills**, and **Global Skills**.

## 🛡️ Atomic Rules
1. **Fact Tracing (MANDATORY)**: Every claim made during analysis MUST cite a source (e.g., [US10123456B2, Col 4]).
2. **Local Skill Priority**: Read `../skills/[skill-name]/SKILL.md` before calling a skill.
3. **Step Atomization**: Follow the 4-domain lifecycle of patent processing. Do not skip steps.
4. **Reference Loading**: Only load references for the active domain.
5. **Agent Identification**: Always consult `Agents.md` to identify the correct specialist role for the task.
6. **Short-Term Memory**: Always check `doc/exec-plans/active/` to pick up active task state before reading general background references.

---

## 🏗️ Domains & Required Context

### 🔍 Patent Search & Prior Art (专利检索)
*Primary Domain: Finding existing patents and identifying technical novelty.*
- **Local Skills**: `../skills/patents-search`, `../skills/prior-art-search`
- **Global Skills**: @[/find-skills]
- **References**: `./references/search_playbook.md`

### 📥 Patent Download & Parsing (专利下载与解析)
*Primary Domain: Extracting technical data from PDFs or XMLs.*
- **Local Skills**: `../skills/pdf`
- **References**: `./references/parsing_standards.md`

### 📊 Patent Classification & Assessment (专利分类与评估)
*Primary Domain: Evaluating claims, identifying IPC/CPC codes.*
- **Local Skills**: `../skills/patent-claims-analyzer`, `../skills/patent-examiner`
- **References**: `./references/classification_guidelines.md`

### ✍️ Patent Drafting & Generation (专利撰写与生成)
*Primary Domain: Creating new patent applications.*
- **Local Skills**: `../skills/patent-application-creator`, `../skills/patent-architect`
- **References**: `./references/drafting_standards.md`

---

## 👥 Agents & Specialized Roles
Check `./Agents.md` for designated roles (Researcher, Analyst, Architect) and their specific safety guardrails.

---

## 📓 FAULT_DIARY.md
Always check `./FAULT_DIARY.md` for known hallucination patterns or search failures in this project before proceeding.



# 🚦 medpatent：渐进式上下文路由器
**避免幻觉。遵循分步操作原则。**
确定您任务的**主要领域**，仅加载指定的参考资料、**本地技能**和**全局技能**。
## 🛡️ 原子规则1. **事实追溯（必填项）**：在分析过程中提出的每一项主张都必须引用出处（例如，[美国专利 10123456B2，第 4 节]）。2. **本地技能优先级**：在调用任何技能之前，请先阅读 `../skills/[技能名称]/SKILL.md` 文件。3. **步骤分解**：遵循专利处理的 4 个阶段的生命周期流程。切勿跳过任何步骤。4. **参考加载**：仅加载当前域的相关参考文献。5. **代理识别**：在执行任务时，请务必查阅 `Agents.md` 文件以确定相应的专业人员角色。6. **短期记忆**：在阅读一般背景资料之前，务必先查看 `doc/exec-plans/active/` 文件夹以获取当前任务的状态信息。
---

## 🏗️ 域名及所需背景信息
### 🔍 专利检索与现有技术（专利检索）
*主要领域：查找现有专利并识别技术新颖性。*
- **本地技能**：`../技能/专利检索`，`../技能/现有技术检索`
- **全球技能**：@[/技能列表]
- **参考文献**：`./参考资料/检索手册.md`
### 📥 专利下载与解析（从 PDF 或 XML 文件中提取技术数据）
*主要领域：从 PDF 或 XML 文件中提取技术数据。*
- **本地技能要求**：`../技能/PDF`
- **参考文献**：`./参考文献/解析标准.md`
### 📊 专利分类与评估（专利分类与评估）
*主要领域：评估专利主张、确定 IPC/CPC 编码。*
- **本地技能**：`../技能/专利主张分析员`，`../技能/专利审查员`
- **参考文献**：`./参考文献/分类指南.md`
### ✍️ 专利撰写与生成（专利申请的创建）
*主要领域：创建新的专利申请。*
- **本地技能**：`../技能/专利申请创建者`，`../技能/专利设计师`
- **参考文献**：`./参考资料/撰写标准.md`
---

## 👥 代理与特定角色
请查阅 `./Agents.md` 文件以了解指定的角色（研究员、分析师、架构师）及其具体的安全规范。
---

## 📜 FAULT_DIARY.md
在继续操作之前，请务必查看 `./FAULT_DIARY.md` 文件，以了解已知的幻觉模式或项目中的搜索失败情况。