# 任务规划: medpatent 架构升级 v2.0

## 🎯 目标
升级 Harness 与 Skill 架构，采用“刚性管道 + 弹性审判”模式，解决专利去重、幻觉与不一致问题。

## 📋 任务阶段
### 阶段 1: 基础设施与刚性管道 (Complete)
- [x] 创建 `patent-data-pipeline` Skill
- [x] 开发 `deduplicate.py` 与 `baseline_verify.py`
- [x] 验证 81 -> 59 去重逻辑

### 阶段 2: 语义审判与协议更新 (Complete)
- [x] 修改 `classification_guidelines.md` (对撞协议)
- [x] 升级 `patent-claims-analyzer` (证据三元组)

### 阶段 3: 事实记录系统 (IR) 与生成器 (Complete)
- [x] 实现 `structured_findings.json` IR 层
- [x] 更新 `patent-application-creator` (只读生成模式)

### 阶段 4: 知识库与验收 (Complete)
- [x] 更新 `FAULT_DIARY.md`
- [x] 运行坏例测试 (US9283050B2)

## 🛠️ 当前状态
- 实施计划已获批
- 准备开始阶段 1
