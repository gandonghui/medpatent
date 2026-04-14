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
