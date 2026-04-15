# 📥 medpatent: Parsing Standards & Provenance

Rules for extracting data (Claims, Background, Embodiments) from patent documents.

## 🚩 Rule 1: Structural Extraction
- **MANDATORY**: Separate the abstract, independent claims, and dependent claims.
- **MANDATORY**: For US patents, extract 35 USC 112(a)/(b) specific disclosures.

## 🚩 Rule 2: Citation Provenance
- Every technical fact MUST cite its location.
- **Format**: `[[PatentNumber, Location (Col, Line/Para)]]`
- **Example**: `The haptic feedback provides 12-bit resolution [[US10123456, Col 12, L15]].`

## 🚩 Rule 3: Text Clean-up
- Remove OCR artifacts, page numbers, and unrelated headers.
- **Translation Policy**: EN and CN terms must be tracked as a mapping (e.g., `Haptic Feedback -> 力反馈`).

## 📓 Parsing Log Template
```json
{
  "patent": "US10123456B2",
  "independent_claims": [1, 10, 15],
  "technical_features": [
    {
      "feature": "Haptic sensor",
      "location": "Col 4, Para 3",
      "description": "Pressure-sensitive resistive array..."
    }
  ]
}
```


# 📥 medpatent：解析标准与来源
从专利文件中提取数据（包括“主张”、“背景”、“实施例”）的规则。
## 🚩 规则 1：结构提取
- **必行**：将摘要、独立权利要求和从属权利要求分开。
- **必行**：对于美国专利，提取符合 35 USC 112(a)/(b) 规定的具体说明内容。
## 🚩 规则 2：引用来源
- 每个技术事实都必须标明其出处。
- **格式**：`[[专利号，位置（列、行/段落）]]`
- **示例**：`这种触觉反馈提供了 12 位分辨率 [[US10123456， 第 12 列，第 15 行]]`
## 🚩 第 3 条：文本清理
- 清除光学字符识别（OCR）产生的残余物、页码以及不相关的标题。
- **翻译政策**：英文和中文的术语必须作为映射关系进行记录（例如，“触觉反馈 -> 力反馈”）。
## 📜 解析日志模板
```json{
“专利号”：US10123456B2，
“独立权利要求”：1、10、15，
“技术特征”：{
“特征”：触觉传感器
“位置”：第 4 章第 3 段
“描述”：压敏电阻阵列……}
]
}
```