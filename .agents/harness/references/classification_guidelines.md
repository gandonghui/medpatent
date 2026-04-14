# 📊 medpatent: Classification & Assessment Guidelines

Standards for patent classification analysis and statutory compliance checks.

> [!IMPORTANT]
> To execute these classifications autonomously, you MUST invoke the **`patent-examiner`** skill to comprehensively simulate the 35 USC statutory reviews before building the overlap matrix.

## 🚩 Rule 1: Classification Mapping
- **MANDATORY**: Map each search hit to its corresponding IPC/CPC primary and secondary codes.
- **Example**: `A61B 34/30` (Robotic Surgery) and `A61B 90/00` (Instruments for surgery).

## 🚩 Rule 2: Statutory Review (US/CN)
- **35 USC 101**: Subject matter eligibility (Robotic control algorithms, diagnostic methods).
- **35 USC 102/103**: Novelty and Non-obviousness comparison.
- **35 USC 112**: Enablement, written description, and definiteness.

## 🚩 Rule 3: Technical Overlap Analysis
- Create overlap matrices for the Top 5 search results.
- **Metric**: High (75-100% overlap), Medium (50-74%), Low (< 50%).

## 📓 Unified Classification & Overlap Matrix Template
| Feature | US101... (Title) | EP202... (Title) |
|---------|------------------|------------------|
| **Classification Mapping** | IPC/CPC (e.g. A61B 34/30) | IPC/CPC |
| **Statutory (§ 101/112)** | Pass/Fail (Reason) | Pass/Fail |
| **Feature 1 (e.g., Haptic)**| ✅ High [C1, L5] | ❌ Low |
| **Feature 2 (e.g., AI)** | ⚠️ Medium | ✅ High [C12]|
