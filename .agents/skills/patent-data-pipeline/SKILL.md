---
name: patent-data-pipeline
description: 专门负责专利数据完整性的刚性管道。处理家族去重、基准校验以及生成中间表示层 (IR)。使用确定性 Python 脚本执行物理层任务。
tools: Bash, Read, Write
model: sonnet
---

# Patent Data Pipeline Skill

本 Skill 负责 medpatent 架构中的“刚性管道”层，确保进入分析环节的数据是完整且无重复的。

## 核心功能

1. **家族去重 (`deduplicate.py`)**
   - 输入：包含原始专利列表的 JSON 或目录。
   - 逻辑：解析专利号，根据 INPADOC 家族 ID 或标准申请号基准进行合并（合并 A1, B1, B2 等）。
   - 输出：去重后的专利清单。

2. **基准校验 (`baseline_verify.py`)**
   - 输入：去重后的清单 + 必选专利列表。
   - 逻辑：自动碰撞校验。如果必选专利（Baseline）缺失，则抛出系统级错误并中断后续流程。
   - 输出：校验通过的清单。

3. **IR 生成 (`generate_ir.py`)**
   - 将专利元数据转换为统一的中间表示格式 (`structured_findings.json`)，作为后续“弹性审判”的事实基座。

## 使用场景

- 在执行任何专利分析（如 `patent-claims-analyzer`）之前。
- 在从检索结果导入数据到项目时。
- 在生成最终报告前，确保数据源的一致性。

## 调用协议

1. **初始化**：
   ```bash
   python .agents/skills/patent-data-pipeline/scripts/deduplicate.py --input raw_data.json --output unique_families.json
   ```

2. **校验**：
   ```bash
   python .agents/skills/patent-data-pipeline/scripts/baseline_verify.py --input unique_families.json --baselines US20220015832A1
   ```

## 约束规则

- **严禁 AI 修改去重逻辑**：去重必须基于 Python 脚本的硬规则。
- **错误拦截**：基准校验失败必须作为“致命错误”处理。
