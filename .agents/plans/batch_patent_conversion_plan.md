# Batch Patent Markdown-to-Word Conversion Plan

The goal is to convert all patent Markdown files in the `downloaded_patents` directory into Microsoft Word (.docx) documents, preserving the jurisdiction-based folder structure, and saving them to `C:\Users\pumch\Desktop\patent`.

## User Review Required

> [!IMPORTANT]
> - **Scale**: There are hundreds of patents. Conversion will take several minutes.
> - **Conflict Management**: I will perform a **pre-check** and list any existing `.docx` files in the target directory that would be overwritten. I will ask for your confirmation before starting the actual conversion of those specific files.
> - **Error Reporting**: A detailed log file `conversion_errors.log` will be created to record any failed conversions or corrupted files.

## Proposed Changes

### Automation Script

#### [NEW] [batch_patent_to_word.ps1](file:///c:/Users/pumch/Desktop/medpatent/.agents/scripts/batch_patent_to_word.ps1)
A PowerShell script to automate the recursive conversion.

**Logic Highlights**:
1. Define `$SourceRoot` and `$TargetRoot`.
2. Find all `.md` files in `$SourceRoot` recursively.
3. For each file:
    - Calculate the relative path from `$SourceRoot`.
    - Determine the corresponding destination subfolder in `$TargetRoot`.
    - Create the subfolder if it does not exist.
    - Run the `markdown-to-docx` skill command to convert the file.

## Open Questions

1. **Conflict Confirmation Strategy**: Would you like me to:
    - a) List all conflicts up front and wait for one "yes/no" to proceed with all of them? 
    - b) Skip ALL conflicts automatically and only convert new files?
    - c) Prompt you manually for every single conflict (not recommended for large batches)?

## Verification Plan

### Automated Tests
- Run a search in the target directory after execution to verify that for every `.md` file in the source, a corresponding `.docx` exists in the target.
- Check for any error messages in the script output.

### Manual Verification
- Open at least one converted document from different jurisdictions (e.g., US, CN, WO) in Word to verify formatting.
