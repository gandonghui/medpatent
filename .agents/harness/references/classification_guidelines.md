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



# 📊 medpatent：分类与评估指南
专利分类分析及法定合规性检查的标准。
[重要提示]
若要自主执行这些分类操作，您必须调用“专利审查员”技能，以便在构建重叠矩阵之前全面模拟《美国法典》第 35 篇的法定审查流程。
## 🚩 规则 1：分类映射
- **强制要求**：将每次搜索结果对应至其相应的 IPC/CPC 主要和次要代码。
- **示例**：`A61B 34/30`（机器人手术）和 `A61B 90/00`（手术器械）。
## 🚩 规则 2：法定审查（美国/中国）
- **35 USC 101**：技术主题的可授予性（机器人控制算法、诊断方法）。
- **35 USC 102/103**：新颖性和非显而易见性的比较。
- **35 USC 112**：说明性、书面描述和明确性。
## 🚩 第 3 条：技术重叠分析
- 为前 5 个搜索结果创建重叠矩阵。
- **指标**：高（重叠度 75% - 100%），中（50% - 74%），低（< 50%）。
## 📜 统一分类与重叠矩阵模板
| 特征 | US101...（标题） | EP202...（标题） ||---------|------------------|------------------|
| **分类映射** | IPC/CPC（例如：A61B 34/30） | IPC/CPC |
| **法定标准（§ 101/112）** | 通过/不通过（原因） | 通过/不通过 |
| **特征 1（例如，触觉）| ✅ 高 [C1, L5] | ❌ 低 |
| **特征 2（例如，人工智能） | ⚠️ 中等 | ✅ 高 [C12] |