# Markdown to Word Conversion Skill Implementation Plan

The goal is to provide a robust, batch-capable "Agent Skill" for converting Markdown (.md) files to Microsoft Word (.docx) documents, as requested by the user.

## User Review Required

The user needs to decide between two approaches for the conversion skill:

- **Option A: Install External Skill** (`duc01226/easyplatform@markdown-to-docx`)
    - **Pros**: Quick install, high install count (365), pure JavaScript (no external dependencies needed other than the skill itself).
    - **Cons**: Less customizable formatting than Pandoc.
- **Option B: Create Local Skill** (`pandoc-word-generation`)
    - **Pros**: Uses the industry-standard `pandoc` (already installed), highly customizable, supports advanced formatting (TOC, metadata, etc.), fits the existing repository's "local skills" pattern.
    - **Cons**: Requires manual creation of the skill structure.

> [!IMPORTANT]
> I have already installed **Pandoc** on your system, which works exceptionally well for Word conversion. I recommend **Option B** to leverage this tool and ensure it fits seamlessly into your `medpatent` harness.

## Proposed Changes

Assuming **Option B** (Local Skill), the follow structure will be created:

### [NEW] [.agents/skills/pandoc-word-generation/](file:///c:/Users/pumch/Desktop/medpatent/.agents/skills/pandoc-word-generation/)

#### [NEW] [SKILL.md](file:///c:/Users/pumch/Desktop/medpatent/.agents/skills/pandoc-word-generation/SKILL.md)
Detailed documentation, triggers, and usage instructions for the Word conversion skill.

#### [NEW] [scripts/convert_to_word.ps1](file:///c:/Users/pumch/Desktop/medpatent/.agents/skills/pandoc-word-generation/scripts/convert_to_word.ps1)
A PowerShell script that wraps Pandoc to handle batch conversion, filename mapping, and basic formatting options.

## Open Questions

1. Which option do you prefer: installing the community skill (**Option A**) or creating a custom local one (**Option B**)?
2. Do you have a specific target folder where your Markdown files are usually stored, or should the skill always search the current workspace?

## Verification Plan

### Automated Tests
- Run the newly created/installed skill on a sample `.md` file.
- Verify the resulting `.docx` file is created and readable.

### Manual Verification
- Visual inspection of the generated Word document to ensure formatting (headers, tables, lists) is correct.
