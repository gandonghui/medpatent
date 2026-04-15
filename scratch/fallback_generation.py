import sys
import os
import json
from pathlib import Path

def format_as_markdown(p):
    """Formats patent data into markdown according to parsing_standards.md"""
    md = f"# Patent: {p['publication_number']}\n\n"
    md += f"## Title\n{p.get('title', 'N/A')}\n\n"
    md += f"## Abstract\n{p.get('abstract', 'N/A')}\n\n"
    md += f"## Bibliographic Data\n"
    md += f"- **Filing Date**: {p.get('filing_date', 'N/A')}\n"
    md += f"- **Grant Date**: {p.get('grant_date', 'N/A')}\n"
    md += f"- **Country**: {p.get('country', 'N/A')}\n"
    md += f"- **Assignee**: {p.get('assignee', 'N/A')}\n"
    md += f"- **Inventors**: {', '.join(p.get('inventors', []) or [])}\n"
    md += f"- **CPC Codes**: {', '.join(p.get('cpc_codes', []) or [])}\n\n"
    
    md += f"## Claims\n[Quota Exceeded: Please visit https://patents.google.com/patent/{p['publication_number']} for full claims]\n\n"
    md += f"## Description\n[Quota Exceeded: Full description unavailable due to BigQuery free-tier limit]\n"
        
    return md

def main():
    output_dir = Path(r"c:\Users\admin\Desktop\工作\medpatent\doc\downloaded_patents")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results_file = 'search_results.json'
    if not os.path.exists(results_file):
        print("Error: search_results.json not found.")
        return

    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)

    print(f"Generating {len(results)} base patent files from metadata...")
    for item in results:
        file_name = item['publication_number'].replace('-', '_').lower() + ".md"
        target_path = output_dir / file_name
        
        md_content = format_as_markdown(item)
        with open(target_path, 'w', encoding='utf-8') as f_out:
            f_out.write(md_content)
        print(f"Generated: {target_path}")

    print("Success: Generated all metadata-based files.")

if __name__ == "__main__":
    main()
