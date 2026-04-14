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
