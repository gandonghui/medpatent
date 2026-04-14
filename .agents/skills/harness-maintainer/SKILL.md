---
name: harness-maintainer
description: >
  Skill for maintaining the project's Harness (router.md, FAULT_DIARY.md, references).
  Use whenever analyzing trajectories for Doom-Loops, adding a new fault, creating a new skill, updating project-wide standards, or doing Doc-Gardening.
metadata:
  pattern: pipeline
  interaction: multi-turn
---

# 🛠️ Harness Maintainer (Architecture Caretaker & Trace Analyzer)

You are responsible for the health, accuracy, and continuous self-improvement of the **MedPatent** project's AI infrastructure located in `.agents/harness`.
You act as both a **Doc Gardener** (keeping context minimal) and a **Trace Analyzer** (preventing repeating failures) in accordance with the **2026 AI Engineering Paradigm**.

## 📜 Progressive Disclosure (Core Files)

- **`../../harness/router.md`**: The definitive context loading map.
- **`../../harness/FAULT_DIARY.md`**: The recurring fault system of record.
- **`../../harness/references/`**: Project-wide standards (Search, Classification, Parsing, Drafting).
- **`../../harness/scripts/`**: Automation scripts (e.g., `extract_patents.ps1`).

---

## 🏗️ Execution Pipeline (Pattern: Pipeline)

### Step 1: Trace Analysis & Fault Recording
Instead of just waiting for other agents to report bugs, actively analyze the recent agent activity logs:
1. Scan `../../trajectories/` (if available) for "Doom Loops" (where a file was edited 3-5+ times or where similar prompts repeated).
2. Distill the root failure mode into a new entry.
3. Load **`../../harness/FAULT_DIARY.md`**.
4. **MANDATORY**: For every patent-related fault, ensure the "Fix/Mitigation" enforces specific column and line range citations for claims.
5. Format the new entry according to the existing table schema.

### Step 2: Skill/Domain Registration & Layering
When a new local skill is created or a new reference file is added:
1. Load **`../../harness/router.md`**.
2. Identify the correct **Domain** (Search, Analysis, Drafting, etc.).
3. Append the new skill path or reference file path to the domain's list.
4. If a new capability is foundational, update **`../../Agents.md`** to reflect the new **Layer 0 (Harness)** or **Layer 3 (Persona)** skills.

### Step 3: Reference Centralization & Doc Gardening (Garbage Collection)
If you discover a procedural standard that is being duplicated across multiple local skills:
1. Move valid duplicative content to a centralized file in `../../harness/references/`.
2. **Doc-Gardening**: Prune and delete dead rules, redundant plans in `.agents/plans/`, and out-of-date patterns from `router.md` to fight **Context Rot**.
3. Update the affected `SKILL.md` files to point to centralized locations.

### Step 4: Tooling Maintenance & Health Check
1. Ensure scripts in `../../harness/scripts/` (like `extract_patents.ps1`) are documented and functional.
2. Fix any reported broken links or orphaned files in the harness directory.
3. Report the health status and newly distilled Guardrails to the user.

## ⚠️ Gotchas (Maintenance)
- **Context Rot**: Overloading `router.md` with too many global references will degrade model performance. Keep domains focused.
- **Statutory Accuracy**: Every rule change in `classification_guidelines.md` must be reconcilable with actual USPTO/MPEP requirements.
- **Broken Pipes**: Ensure PowerShell scripts in `harness/scripts/` handle Windows-specific path separators and character encoding (UTF-8).

