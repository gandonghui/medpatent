# medpatent 项目架构说明文档 (Architecture)

## 1. 核心架构设计思想

整个项目的核心理念是基于 **Progressive Context Router (渐进式上下文路由)** 与 **Agent Harness (智能体线束/护栏系统)** 构建的。这是一个具有极高工程化水准、高度专业化的多智能体协同系统（Multi-Agent System），能够极大地减少大模型的“幻觉”现象，并针对垂直领域的重度分析任务（如专利解析）提供稳定的产出。

具体架构层次如下：

*   **中央调度大脑 (`.agents/harness/router.md`)**：
    系统的主要交通指挥中心。采用**“原子化步骤”**和**“上下文隔离”**策略，将长业务流强行划分为四个核心领域（Patent Search 检索、Parsing 解析、Classification 评估、Drafting 撰写）。通过路由控制，确保智能体仅在对应阶段加载对应领域的规则库（`references`），避免模型因输入过多干扰信息而产生上下文污染。
*   **多职能智能体矩阵 (`.agents/harness/Agents.md`)**：
    明确切分了三个“角色（Role）”的边界：
    *   **Patent Researcher (专利检索专家)**：负责 Boolean/语义检索、提取 IPC/CPC 代码，禁止捏造专利号。
    *   **Patent Analyst (专利分析师)**：基于美国专利法 35 USC (101/102/103/112) 进行侵权合规性审查。
    *   **Patent Architect (专利架构师)**：负责撰写权利要求书，并确保符合专利披露要求的 Enablement。
*   **动作执行层/技能集 (`.agents/skills/`)**：
    遵从模块化（Skill）范式，将底层的执行逻辑（搜索 API 交互、报告生成等）封装为特定的技能节点（如 `patents-search`, `patent-claims-analyzer` 等）。
*   **自反思与纠错系统 (`FAULT_DIARY.md` & `trajectories/`)**：
    基于 _"Harness is the Dataset"_ 的思想，系统内置了错题本机制来长期纠正模型路线的偏移。这构成了一个闭环的“爬山算法（Hill Climbing）”，不断发现模型错误并补充针对性的“强制约束规则（MANDATORY guardrails）”。

## 2. 核心功能与业务流

该系统通过组合不同的智能体，实现了深度垂直的医疗专利业务工作流：

1.  **高精度专利检索数据挖掘**：调用底层工具抓取专利并结构化输出海量技术词以匹配目标技术。
2.  **法理解析与合规审查**：智能体按照预设判定树进行审查以防在创造性与新颖性层面出漏洞。
3.  **专家级情报生成**：如本项目中产出的《达芬奇手术系统五代技术架构深度分析》，自动从海量长文本（`search_results.json` 等材料）中精准抽离核心价值（如力反馈传感、Blackwell 算力架构、视频影像 AI），生成高级分析简报及 PPT 原材料。
4.  **端到端工作流闭环**：通过 `exec-plans` 短期记忆接驳，完成“输入需求 -> 检索提取 -> 法理验证 -> 商业分析生成”的自动流转。

## 3. 架构优势 (Pros)

1.  **极度克制，对抗幻觉能力强**：强制要求列和行的准确引用溯源（Col & Line 引文），辅以专利号正则化校验。这对于需要 100% 准确率的法律与专利业务场景至关重要。
2.  **"瘦"上下文管理 (Surgical Context loading)**：按需切分并加载特定的 Playbook 和 Guideline，显著提升了大模型理解深度并节约 Token。
3.  **内建长期进化机制**：`FAULT_DIARY.md` 反向优化机制让项目不断积累人类（或模型试错后的）经验教训，不再犯同样的逻辑错误。
4.  **极高专业度的高价值交付物**：所输出的技术分析不仅仅停留在字面摘要，更具备医疗行业的洞察能力和投资/研判视角。

## 4. 架构局限性与排雷建议 (Cons & Improvements)

1.  **环境脆弱性与强外部依赖 (Brittleness)**：高度依赖外置 API（如 Valyu 或 Google Patents）。如果 API Key 失效、网络连接错误（FAULT_DIARY 已经反馈过这种情况），极易造成单点阻塞 (Blocker)。建议在流程内构建 Dummy Data（本地测试数据集）进行回退测试。
2.  **状态交接与系统状态过载 (State Management Overhead)**：通过 `doc/exec-plans/active/` 传递进程状态，若执行计划状态机未能成功闭环，后面的智能体就无法承接上下文。建议未来增加基于黑板模式 (Blackboard Pattern) 或嵌入式数据库 (如 SQLite) 来进行上下文及业务对象数据的强结构化传递。
3.  **UI可视化层面的缺失**：作为一个高完成度的系统底座，仍缺乏可视化的管理与监控看板。可以通过你的 `developing-with-streamlit` 技能外挂一个 Dashboard 模块，使执行进程、API 消耗、错误报警直观可用。

---

## 5. 项目完整文件树架构 (Project Directory Structure)

```text
medpatent/
├── README.md                           # 项目简介说明
├── search_results.json                 # 专利检索结果全量原始数据
├── skills-lock.json                    # 本地技能包的锁/版本映射文件
├── Architecture.md                     # 本架构说明文档
│
├── .agents/                            # 智能体核心配置与工作流定义
│   ├── harness/                        # 路由管控与防幻觉护栏中心
│   │   ├── router.md                   # 动态语境路由规则 (4类域划分)
│   │   ├── Agents.md                   # Agent职能配置(分析师/架构师/检索员)
│   │   ├── FAULT_DIARY.md              # 智能体防幻觉测试与排故记录本
│   │   ├── references/                 # 按需分发的高管级“操作手册”
│   │   │   ├── search_playbook.md
│   │   │   ├── parsing_standards.md
│   │   │   ├── classification_guidelines.md
│   │   │   └── drafting_standards.md
│   │   └── scripts/
│   │       └── extract_patents.ps1     # 批量抽取专利数据脚本
│   ├── skills/                         # Agent核心技能库 (ADK机制)
│   │   ├── patents-search/             # 专利搜索API请求技能
│   │   ├── patent-examiner/            # 专利法案侵权审查技能
│   │   ├── patent-claims-analyzer/     # 权利要求结构分析技能
│   │   ├── patent-architect/           # 权利要求起草撰写架构技能
│   │   ├── patent-application-creator/ # 专利申请整体创建技能
│   │   ├── find-skills/                # 技能发现与寻找扩展
│   │   ├── caveman/                    # Token优化轻量级对话技能
│   │   ├── ralph-plan/                 # 交互式规划技能
│   │   ├── systematic-debugging/       # 系统性调试修正框架技能
│   │   ├── planning-with-files-zh/     # 中文文件驱动的任务规划系统
│   │   ├── harness-maintainer/         # Harness更新与标准花园管家
│   │   └── karpathy-skills/            # LLM预防常见代码错误的经验指引
│   └── trajectories/                   # AI执行决策路径日志采集点
│       └── README.md                   # 定义轨迹回放格式(Hill Climbing依据)
│
└── doc/                                # 业务文档产出与研究文献中心
    ├── da_vinci_5_patent_analysis.md   # 核心产出: 达芬奇5系统专利深度分析
    ├── da_vinci_5_patent_analysis_utf8.md
    ├── da_vinci_5_patent_analysis.pptx # 构建生成的幻灯片演示文件
    ├── ISRG_laparoscopic_patents.pptx
    ├── downloaded_patents/             # 下载的不同专利原始报告(按专利号命名)
    │   ├── 08281670.md
    │   ├── 09592093.md
    │   ├── 09737326.md
    │   ├── 09888966.md
    │   └── 10779856.md
    ├── exec-plans/                     # 智能体短时记忆与状态机(接力棒)
    │   ├── active/
    │   │   └── README.md               # 记录当前执行计划的状态
    │   └── completed/
    │       └── README.md
    ├── Harness/                        # 构建Agent架构的核心论文与技术理论
    │   ├── Agent Harness：2026年AI工程的核心范式.md
    │   ├── Effective harnesses for long-running agents.md
    │   ├── Harness engineering leveraging Codex in an agent-first world.md
    │   ├── Improving Deep Agents with harness engineering.md
    │   ├── Lessons from Building Claude Code Seeing like an Agent.md
    │   └── The importance of Agent Harness in 2026.md
    └── skills/                         # Skill设计与解耦相关学术研究文章
        ├── 5 Agent Skill design patterns every ADK developer should know.md
        ├── Equipping agents for the real world with Agent Skills.md
        └── Lessons from Building Claude Code How We Use Skills.md
```
