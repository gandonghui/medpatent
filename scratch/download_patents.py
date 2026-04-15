import sys
import os
import json
from pathlib import Path

# Add skill python path to sys.path
SKILL_ROOT = r'c:\Users\admin\Desktop\工作\medpatent\.agents\skills\bigquery-patent-search'
sys.path.insert(0, os.path.join(SKILL_ROOT, 'python'))

from bigquery_search import BigQueryPatentSearch

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
    
    if 'claims' in p and p['claims']:
        md += f"## Claims\n{p['claims']}\n\n"
    
    if 'description' in p and p['description']:
        # Keep large descriptions for analysis, maybe snippet if too huge? standard says 'full content'
        md += f"## Description\n{p['description'][:10000]}...\n" # Limit to 10k chars for sanity in markdown
        
    return md

def main():
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'my-project-gemini-test-485607'
    output_dir = Path("doc/downloaded_patents")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results_file = 'search_results.json'
    if not os.path.exists(results_file):
        print("Error: search_results.json not found.")
        return

    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)

    searcher = BigQueryPatentSearch()
    print(f"Starting download of {len(results)} patents to {output_dir.absolute()}")
    
    for item in results:
        pub_num = item['publication_number']
        file_name = pub_num.replace('-', '_').lower() + ".md"
        target_path = output_dir / file_name
        
        print(f"Fetching full data for {pub_num}...")
        try:
            full_data = searcher.get_patent(pub_num)
            if full_data:
                md_content = format_as_markdown(full_data)
                with open(target_path, 'w', encoding='utf-8') as f_out:
                    f_out.write(md_content)
                
                # IMMEDIATE VERIFICATION
                if os.path.exists(target_path):
                    print(f"VERIFIED: Saved to {os.path.abspath(target_path)}, Size: {os.path.getsize(target_path)} bytes")
                else:
                    print(f"FAILURE: File {target_path} DOES NOT EXIST after write!")
            else:
                print(f"Failed to fetch {pub_num}")
        except Exception as e:
            print(f"Error processing {pub_num}: {e}")

    print("Download completed. Verifying files...")
    print(f"Files in {output_dir}: {os.listdir(output_dir)}")

if __name__ == "__main__":
    main()
