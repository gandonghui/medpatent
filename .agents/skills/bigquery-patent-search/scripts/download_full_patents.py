import os
import sys
import json
from pathlib import Path

# Add python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))
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
        md += f"## Description Snippet\n{p['description'][:2000]}...\n" # Keeping snippets for quick review
        
    return md

def main():
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT', 'medpatent-493307')
    search_results_path = Path(r"c:\Users\gan\medpatent\.agents\harness\data\search_results\bq_results.json")
    output_dir = Path("downloaded_patents")
    output_dir.mkdir(exist_ok=True)

    if not search_results_path.exists():
        print(f"Error: {search_results_path} not found.")
        return

    with open(search_results_path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)

    if not data.get('success'):
        print("Error: Search result was not successful.")
        return

    results = data.get('results', [])
    searcher = BigQueryPatentSearch(project_id=project_id)

    print(f"Starting download of {len(results)} patents...")
    
    count = 0
    for item in results:
        pub_num = item['publication_number']
        file_name = pub_num.replace('-', '_').lower() + ".md"
        target_path = output_dir / file_name
        
        if target_path.exists():
            print(f"Skipping {pub_num}, already exists.")
            continue

        try:
            full_data = searcher.get_patent(pub_num)
            if full_data:
                md_content = format_as_markdown(full_data)
                with open(target_path, 'w', encoding='utf-8') as f_out:
                    f_out.write(md_content)
                count += 1
                if count % 10 == 0:
                    print(f"Downloaded {count}/{len(results)}...")
            else:
                print(f"Failed to fetch full data for {pub_num}")
        except Exception as e:
            print(f"Error processing {pub_num}: {e}")

    print(f"Successfully downloaded and formatted {count} patents to {output_dir}/")

if __name__ == "__main__":
    main()
