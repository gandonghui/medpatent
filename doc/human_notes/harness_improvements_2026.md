# Agent Harness 工程化优化建议 (2026版)

> **📝 核心主旨**
> 本文档专供人类开发者阅读（系统运行时 Agent 不会主动加载此文件）。这记录了如何将系统从“依赖大模型推理”的安全区，推向更具备工业级“确信度（Determinism）”与自洽性的高成熟度架构。

基于 Anthropic 与 OpenAI 最新发布的 Agent Harness 最佳实践，当前 `medpatent` 系统存在 5 个关键的改进切入点：

---

### 1. 状态追踪：从 Markdown 到 JSON 的防越界改造 (State Management)
**问题痛点：**
目前 `doc/exec-plans/active/README.md` 采用纯文本/Markdown 追踪状态。由于自然语言的灵活性，Agent 在多个上下文窗口间接力（如 Searcher 传递给 Analyst）时，极易不规范地篡改状态栏，或“提前臆断任务已完成”。

**改进建议：**
*   **启用 JSON 状态追踪机**：建立 `doc/exec-plans/active/progress_tracker.json`（代替现有的 `.md` 备忘录）。
*   **强制严格字段**：设置例如 `"passes": false`，`"dependencies": [...]` 等固化的控制位。
*   **修改提示词**：在 Router 中明令禁止大模型用自然语言汇报总进度，要求其“**只能通过使用工具（如 Python 脚本）修改 JSON 配置文件的状态字段来推进长流程**”。模型处理 JSON 结构数据的合规性远不抛错。

### 2. 引入“强制自验证”循环 (Build & Self-Verify Loop)
**问题痛点：**
目前的技能流（如产生 Office Action 或分析文档）呈线性。Agent 将文本生成完毕即视为完工，缺乏闭环测试。

**改进建议：**
*   **加入 Reviewer / 产品验证（Product Verification）型技能**：
*   在 `.agents/harness/scripts/` 中增设静态规则检查脚本，比如 `validate_citations.py`。
*   **设置 Exit Plan 面包屑门槛**：在 Agent 结束会话前注入特定 Middleware 或强制指令，要求它运行这些验证脚本（比如验证产出的 MD 文件里是否包含 100% 对应格式的文献出处引用 `[USXXXX, Col X]`），必须拿到 `Exit code 0`，否则转入 **修复模式 (Fix phase)**，禁止直接提交结果。

### 3. 解锁“死循环护栏”与时间预算 (Interrupting Doom Loops)
**问题痛点：**
`FAULT_DIARY.md` 中的错误大都是人类复盘。当 API 异常或模型死磕某一个难以处理的逻辑（如检索结果无返回还在硬拗）时，系统容易陷入消耗海量 Token 的“Doom Loop（死循环）”。

**改进建议：**
*   **预设预算意识 (Time Budget)**：在 Agent 进场提示前明确告知其试错阈值（比如：“如果调用检索 API 失败超过 3 次，立刻停止当前规划。”）。
*   利用已有的 `systematic-debugging` 技能思路，当脚本执行失败或无法识别出目标时，强制中止自治，调用 `AskUserQuestion` 回落请求人工（Human-in-the-loop）干预。

### 4. 技能文档中设立显性的 "Gotchas" 模块 (Failure Signaling)
**问题痛点：**
虽然具备 `FAULT_DIARY.md` 这个大错题本，但具体的技能文件（如 `.agents/skills/patents-search/SKILL.md`）偏向于写“最佳流程”，并未列出模型在这里容易摔跤的坑。

**改进建议：**
*   **高信噪比章节**：在各个核心 `SKILL.md` 中，开设一段专属的 `## Gotchas（常见陷阱/避坑指南）`。
*   **下沉血泪教训**：把 `FAULT_DIARY.md` 里遇到的情况具象化进去。例如在 Search 技能中写入：“*Gotcha：不要在没有任何工具输出确认的情况下编造专利号，如果检索长度超标引发解析崩溃，优先利用工具截断返回……*”。这能提前掐断特定场景下的固有幻觉倾向。

### 5. 将“逻辑消耗”重度转移到可执行代码 (Token offloading to Code)
**问题痛点：**
当获取到的 `search_results.json` 体积达到数百 Kb，若仍然依赖将大段内容导入模型上下文（Context Window）中让它寻找相关的 IPC 分类，会导致极其低效、昂贵并可能丢失焦点。

**改进建议：**
*   **将逻辑外包给代码工具**：应用 **Data Fetching & Analysis 技能原则**，将原本试图让模型阅读去解决的任务转化为预写好的 Python 脚本。
*   例如增加 `scripts/extract_top_ipc.py <json_path>`，通过代码硬计算将庞杂数据精准压缩成摘要。让大语言模型充当**调用控制者（Commander）**，通过确信的返回值去决策，而不是充当**文本阅读器（Reader）**生吞海量 JSON 结构。
