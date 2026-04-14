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
