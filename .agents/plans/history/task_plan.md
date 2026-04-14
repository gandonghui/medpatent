# Task: 100 Patent Data Retrieval (Intuitive Surgical)

- [x] Initial System Test with Valyu (Limited to 5 results)
- [x] Research BigQuery Patent Skill Alternatives
- [x] Implement BigQuery Patent Search (python/bigquery_search.py)
- [x] Update SQL schema to handle nested fields (inventor.name, assignee.name, cpc.code)
- [x] Configure Google Cloud Project (medpatent-493307)
- [x] Authenticate using Application Default Credentials (ADC)
- [x] Refine Search Strategy for 100 results (Intuitive Surgical + Robotic)
- [x] Batch Download 100 Full Patents (scripts/download_full_patents.py)
- [x] Verify and Format to Markdown (downloaded_patents/)
- [ ] Final Analysis of Retrieved Data

## Current Status
- Batch download completed. 104 patents retrieved from BigQuery.
- Data formatted as per `parsing_standards.md`.
