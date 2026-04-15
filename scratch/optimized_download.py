import sys
import os
import json
from pathlib import Path
from google.cloud import bigquery

# Add skill python path to sys.path
SKILL_ROOT = r'c:\Users\admin\Desktop\工作\medpatent\.agents\skills\bigquery-patent-search'
sys.path.insert(0, os.path.join(SKILL_ROOT, 'python'))

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
    else:
        md += f"## Claims\n[Full claims not found in this query]\n\n"
    
    md += f"## Description\n[Description skipped to conserve BigQuery quota - see Bibliographic data/Abstract for summary]\n"
        
    return md

def main():
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'patent-search-3d-02'
    output_dir = Path(r"c:\Users\admin\Desktop\工作\medpatent\doc\downloaded_patents")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # IDs from previous search
    ids = [
        'US-2024350121-A1', 'US-2022414914-A1', 'US-12205315-B2', 
        'US-2020022769-A1', 'US-11304771-B2', 'US-2017181798-A1', 
        'US-10334227-B2', 'US-2017181808-A1', 'US-2017180704-A1', 
        'US-10555788-B2'
    ]
    id_list = ", ".join([f"'{i}'" for i in ids])
    
    client = bigquery.Client(project=os.environ['GOOGLE_CLOUD_PROJECT'])
    
    # Optimized Batch Query (Skipping 'description' column to save 90%+ quota)
    sql = f"""
        SELECT 
            publication_number, 
            title_localized[SAFE_OFFSET(0)].text as title,
            abstract_localized[SAFE_OFFSET(0)].text as abstract,
            claims_localized[SAFE_OFFSET(0)].text as claims,
            filing_date,
            grant_date,
            country_code as country,
            (SELECT ARRAY_AGG(DISTINCT c.code) FROM UNNEST(cpc) as c) as cpc_codes,
            (SELECT ARRAY_AGG(DISTINCT i) FROM UNNEST(inventor) as i) as inventors,
            (SELECT a FROM UNNEST(assignee) as a LIMIT 1) as assignee
        FROM 
            `patents-public-data.patents.publications`
        WHERE 
            publication_number IN ({id_list})
    """
    
    print("Executing optimized batch query (scanning metadata and claims)...")
    query_job = client.query(sql)
    count = 0
    for row in query_job:
        p = {
            "publication_number": row.publication_number,
            "title": row.title,
            "abstract": row.abstract,
            "claims": row.claims,
            "filing_date": str(row.filing_date) if row.filing_date else None,
            "grant_date": str(row.grant_date) if row.grant_date else None,
            "country": row.country,
            "cpc_codes": row.cpc_codes,
            "inventors": row.inventors,
            "assignee": row.assignee
        }
        
        file_name = p['publication_number'].replace('-', '_').lower() + ".md"
        target_path = output_dir / file_name
        
        md_content = format_as_markdown(p)
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        count += 1
        print(f"[{count}] Saved: {target_path}")

    print(f"Successfully processed {count} patents.")

if __name__ == "__main__":
    main()
