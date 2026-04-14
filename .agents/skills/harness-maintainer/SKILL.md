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

You are responsible for the health, accuracy, and continuous self-improvement of the **Mihe (碰杯)** project's AI infrastructure located in `.agents/harness`.
You act as both a **Doc Gardener** (keeping context minimal) and a **Trace Analyzer** (preventing repeating failures).

## 📜 Progressive Disclosure (Core Files)

- **`../../harness/router.md`**: The definitive context loading map.
- **`../../harness/FAULT_DIARY.md`**: The recurring fault system of record.
- **`../../harness/references/`**: Project-wide invariants and standards.
- **`../../trajectories/`**: Ongoing Agent trajectory logs (Doom-Loop data source).

---

## 🏗️ Execution Pipeline (Pattern: Pipeline)

### Step 1: Trace Analysis & Fault Recording
Instead of just waiting for other agents to report bugs, actively analyze the recent agent activity logs:
1. Scan `../../trajectories/` for "Doom Loops" (where a file was edited 3-5+ times without success or where similar prompts repeated).
2. Distill the root failure mode into a new entry.
3. Load **`../../harness/FAULT_DIARY.md`**.
4. Format the new entry according to the existing table schema.
5. **MANDATORY**: Ensure the "Permanent Fix / Mitigation" column provides actionable, testable code-level advice to prevent this specific loop for future agents.

### Step 2: Skill/Domain Registration
When a new local skill is created or a new reference file is added:
1. Load **`../../harness/router.md`**.
2. Identify the correct **Domain** (UI, Backend, etc.).
3. Append the new skill path or reference file path to the domain's list.
4. Verify that the file link is valid from the root workspace.

### Step 3: Reference Centralization & Doc Gardening (Garbage Collection)
If you discover a procedural standard that is being duplicated across multiple local skills or is no longer relevant:
1. Execute structural checks or manually review codebase rules to ensure all constraints in `references/` still apply to the actual code.
2. Move valid duplicative content to a new or existing file in `../../harness/references/`.
3. **Doc-Gardening**: Prune and delete dead rules, inactive plans in `doc/exec-plans/active/`, and out-of-date patterns from `router.md` to keep context lightweight.
4. Update the affected `SKILL.md` files to point to centralized locations.

### Step 4: Health Check & Architecture Policing
1. Run `python ../../harness/scripts/harness_health_check.py` (if available) to validate markdown files.
2. Enforce strict Architectural Boundaries (e.g., UI should not query Data directly if there's a strict boundary logic). Flag and warn about deviations.
3. Fix any reported broken links or orphaned files.
4. Report the health status and newly distilled Guardrails to the user.

## ⚠️ Gotchas (Maintenance)
- **Broken Links**: Relative paths in `router.md` must be correct relative to the task execution environment.
- **Stale Faults**: Periodically review the fault diary to see if any older entries can be consolidated into `architecture_constraints.md` or deleted entirely due to framework upgrades.
