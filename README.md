# 🧬 MedPatent

专注于医疗机械与数字医疗领域的专利检索、自动化分析与声明撰写的 Agent-First 架构工程库 (Harness Engineering)。

本仓库基于 **Agent Harness: 2026 AI Engineering Paradigm** 设计，将复杂的美国专利（35 USC 验证）与技术重叠网络审查，通过预设规则集、强制性防幻觉护栏和隔离环境，使得 AI Agent 能以最高精准度长程作业。

---

## 🚀 快速启动

MedPatent 项目完全由内置 AI Agent 技能驱动。作为人类用户，您的核心任务不是写代码，而是“布置任务并提供凭证”。

### 1. 前置环境配置
本项目部分组件依赖 [Valyu API](https://valyu.network/) 执行高精度的全球语义专利检索。在使用前，请开启终端并执行以下配置动作以挂载您的个人密钥：
```powershell
# 进入 search 工具所在目录并执行注册
cd .agents/skills/patents-search
node scripts/search.mjs setup <YOUR_VALYU_API_KEY>
```

### 2. 引导 AI 开启工作流
在新的一轮交互中，直接向您的 AI 助手发送指令。为了触发正确的基建环境，请在**最开始**要求 AI Agent：
> "请通读 `AGENTS.md`，确认你的可用技能与所在层域，然后准备开始执行..."

---

## 🗺️ 推荐的工程化使用流水线 (Pipeline)

在处理“特定医疗器械（如 Da Vinci 手术机器人）的侵权排查与创新点挖掘”类复杂工作时，推荐按照以下四个步骤要求 Agent 串行执行：

### 阶段一：高维规划与知识留存 (Planning)
- **指令示例**："使用 `planning-with-files-zh` 技能，将我的需求（例如排查达芬奇手术机器人5代力反馈结构）拆解为里程碑任务置于 `.agents/plans/` 目录下。"
- **Agent 动作**：将不会盲目开写，而在磁盘创建持久化计划书并追踪状态，防止未来交互中发生上下文遗忘 (Context Rot)。

### 阶段二：精准召回与实体库提存 (Search & Extraction)
- **指令示例**："使用 `patents-search` 检索技术集合。拿到返回结果后，必须使用 `.agents/harness/scripts/extract_patents.ps1` 脚本，将搜回的 JSON 内容导出成结构化档案到 `/downloaded_patents/`。"
- **Agent 动作**：执行 Boolean 拓扑或 Semantic 组合检索，突破幻觉红线。它每次都会确保本地有可查的 Markdown 全文本标本，满足“可核查性”。

### 阶段三：法律检查与重叠矩阵组建 (Examination & Matrix)
- **指令示例**："读取下载下来的 `.md` 专利实体，**强制调起** `patent-examiner` 技能，根据 `classification_guidelines.md` 的要求，执行 35 USC (特别是 101/102/112条) 法定初筛，最后输出核心技术重叠矩阵（Overlap Matrix）。"
- **Agent 动作**：AI 化身 USPTO 审查员，寻找权利要求与说明书之间的支撑关系（必须精确到 column / line），筛除过度宽泛的主张。

### 阶段四：壁垒规避与架构起草 (Drafting & Architecture)
- **指令示例**："避开刚才分析中重叠度为 'High' 的权利主张，调用 `patent-application-creator` 技能构建我们的改良起草方案与权利架构树。"
- **Agent 动作**：使用严谨的法律声明体素，从说明书(Specification)到底层独立/从属权利要求(Independent/Dependent Claims)一体化输出。

---

## 🧱 了解工作流的底层核心引擎 (Harness Base)

为什么要这样限制流程？这套系统不是简单“一次发十几个 prompt 给模型”。为了保持机器的稳定性与动作耐久性，我们在引擎周围加装了重型装甲包（Harness）：

* **`AGENTS.md` (主协议)**：是执行一切任务的基础。它将项目分割为不同的子人设身份。
* **`.agents/harness/router.md` (按需加载组件)**：严禁 Agent “一口吞进所有规则”。Router 文件告诉系统什么场景下该载入哪一张指导卡片，以优化 Token 分配。
* **`.agents/harness/FAULT_DIARY.md` (事故与故障录记)**：Agent 宕机（如：陷入循环卡死、找不到API环境）时登记的“黑匣子记录带”。遇到任何报错，应让 Agent 先看这里避免又跌坑里。
* **`.agents/harness/references/` (执行细则宝典)**：内置了从怎样防幻觉（`search_playbook.md`）到怎么进行法务打标分类（`classification_guidelines.md`）的微型基准指导手册。

---

## ⚠️ 防死亡死循环指南 (Doom-Loop Breakout)

若您发觉 AI Agent 在某一层面上（如同一条法务检查反复报错无法过关）陷入了打转状态，且相同状况重演达到了 **3次**：
- **请果断强制打断它。**
- 让它强制启动 `ralph-plan` 或者跌落回 `systematic-debugging` 技能执行一次干净的根因排查。
- 确认出病因并修补漏洞后，**务必责令 AI 将相关教训载录至 `FAULT_DIARY.md` 中**，将其转化为项目的群体肌肉记忆。
