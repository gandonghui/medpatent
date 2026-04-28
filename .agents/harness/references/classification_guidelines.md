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

## 🚩 Rule 4: Evidence Triplet Protocol (证据三元组协议)
- **MANDATORY**: For every technical feature identified, you MUST provide a triplet:
  1. **Label**: The technical tag (e.g., "AI", "Software Tracking").
  2. **Evidence**: Exact quote from the claims or description [e.g., Claim 1, Line 5].
  3. **CPC Anchor**: The relevant CPC code that supports this technical area.

## 🚩 Rule 5: Collision Detection (冲突对撞协议)
- **Mechanism**: Perform a "Reality Check" between the semantic Label and the physical CPC code.
- **Constraint**: If a patent is primarily in a **Mechanical Class** (e.g., A61B 17/00, A61B 34/30) but the Agent labels it as **"AI/Software"**:
  - The Agent MUST invoke the **High-Intensity Audit** mode.
  - **Audit Requirement**: Find at least two explicit computer architecture terms (e.g., "processor", "memory", "algorithm", "neural network") in the *Independent Claims*.
  - **Failure Action**: If explicit evidence is not found, the "AI/Software" label MUST be retracted or downgraded to "Pure Mechanical/Control".

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

## 🚩 规则 4：证据三元组协议 (Evidence Triplet Protocol)
- **强制要求**：对于识别出的每一个技术特征，必须提供三元组：
  1. **标签 (Label)**：技术标签（如“人工智能”、“软件追踪”）。
  2. **证据 (Evidence)**：权利要求或说明书中的精确引文 [例如：权利要求 1，第 5 行]。
  3. **CPC 锚点 (CPC Anchor)**：支持该技术领域的相关 CPC 代码。

## 🚩 规则 5：冲突对撞协议 (Collision Detection)
- **机制**：在语义“标签”与物理“CPC 代码”之间进行“现实检查”。
- **约束**：如果专利主要属于**机械类**（如 A61B 17/00, A61B 34/30），但代理将其标记为**“人工智能/软件”**：
  - 代理必须调用**高强度审计**模式。
  - **审计要求**：在*独立权利要求*中找到至少两个明确的计算机架构术语（如“处理器”、“存储器”、“算法”、“神经网络”）。
  - **失败操作**：如果未找到明确证据，必须撤回“人工智能/软件”标签，或将其降级为“纯机械/控制”。
## 📜 统一分类与重叠矩阵模板
| 特征 | US101...（标题） | EP202...（标题） ||---------|------------------|------------------|
| **分类映射** | IPC/CPC（例如：A61B 34/30） | IPC/CPC |
| **法定标准（§ 101/112）** | 通过/不通过（原因） | 通过/不通过 |
| **特征 1（例如，触觉）| ✅ 高 [C1, L5] | ❌ 低 |
| **特征 2（例如，人工智能） | ⚠️ 中等 | ✅ 高 [C12] |