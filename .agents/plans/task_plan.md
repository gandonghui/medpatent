# 任务规划: Intuitive Surgical 专利检索 (BigQuery)

## 🎯 目标
使用 `@/bigquery-patent-search` 检索 10 个 Intuitive Surgical 公司在 3D 成像与视觉系统相关的专利，测试 Project ID: `my-project-gemini-test-485607`。

## 📋 任务列表
- [ ] 环境初始化 (安装 google-cloud-bigquery, 设置 ENV)
- [ ] 编写并执行检索脚本 (Intuitive Surgical + "3D imaging" + "vision system")
- [ ] 结果分析与归档 (依照 Search Playbook 记录 Findings)
- [ ] 生成最终报告

## 🛠️ 技术选型
- **工具**: BigQuery Patent Search Skill
- **Persona**: Patent Researcher (专利检索专家)
- **Dataset**: `patents-public-data.patents.publications`
