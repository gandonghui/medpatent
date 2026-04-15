# Trajectory Logs

This directory serves as the dataset collection point for the **Agent Harness**. 

According to the "Harness is the Dataset" principle, AI agents operating in this repository must log their execution failures, hallucinations, dead-ends, and logical drifts here.

## Logging Format

Whenever you encounter a significant error or find that your initial plan failed due to model drift or lack of context durability, create a markdown file in this directory (e.g. `YYYY-MM-DD_issue_name.md`) containing:

1. **The Goal**: What you were trying to achieve.
2. **The Failure**: What went wrong (e.g., hallucinated a flex rule in Skyline, entered an infinite debug loop).
3. **The Root Cause**: Why the model failed (e.g., context window dropped previous rule, assumed standard web CSS).
4. **The Resolution**: How it was fixed.

This data will be used to systematically improve the agent harness and fine-tune future model iterations ("Hill Climbing").




# 轨迹日志
此目录是“代理框架”数据集的收集点。
根据“数据集即准则”这一原则，在此存储库中运行的 AI 代理必须在此记录其执行失败、幻觉、死胡同以及逻辑偏差等情况。
## 日志格式
每当您遇到重大错误，或者发现由于模型漂移或缺乏上下文的持久性而导致初始计划失败时，请在此目录中创建一个 markdown 文件（例如 `YYYY-MM-DD_issue_name.md`），其中应包含：
1. **目标**：你所试图达成的目的。2. **失败原因**：出现了什么问题（例如，在“Skyline”中误识别出了一条可变形规则，或者陷入了无限的调试循环）。3. **根本原因**：该模型为何失败（例如，上下文窗口舍弃了之前的规则，或假定使用了标准的网页 CSS）。4. **决议内容**：问题是如何解决的。
这些数据将被用于系统性地改进代理系统，并对未来的模型迭代进行微调（“爬山法”）。
