import sys
import os
import json
from pathlib import Path
from google.cloud import bigquery

def main():
    # Use the new project ID with fresh quota
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'patent-search-3d-02'
    
    client = bigquery.Client(project=os.environ['GOOGLE_CLOUD_PROJECT'])
    
    # Target: Intuitive Surgical, 3D imaging/vision
    # Using REGEXP_CONTAINS for assignee to catch variations
    # Using keywords in title/abstract
    sql = """
        SELECT 
            publication_number, 
            title_localized[SAFE_OFFSET(0)].text as title,
            abstract_localized[SAFE_OFFSET(0)].text as abstract,
            filing_date,
            grant_date,
            country_code as country,
            (SELECT ARRAY_AGG(DISTINCT c.code) FROM UNNEST(cpc) as c) as cpc_codes,
            (SELECT ARRAY_AGG(DISTINCT i) FROM UNNEST(inventor) as i) as inventors,
            (SELECT a FROM UNNEST(assignee) as a LIMIT 1) as assignee
        FROM 
            `patents-public-data.patents.publications`
        WHERE 
            (
                REGEXP_CONTAINS(LOWER(ARRAY_TO_STRING(assignee, ' ')), r'intuitive surgical')
            )
            AND (
                REGEXP_CONTAINS(LOWER(title_localized[SAFE_OFFSET(0)].text), r'3d|three-dimensional|stereoscopic|vision|imaging|endoscope') OR
                REGEXP_CONTAINS(LOWER(abstract_localized[SAFE_OFFSET(0)].text), r'3d|three-dimensional|stereoscopic|vision|imaging|endoscope')
            )
        ORDER BY filing_date DESC
        LIMIT 500
    """
    
    print("Executing comprehensive metadata-only search...")
    query_job = client.query(sql)
    
    results = []
    for row in query_job:
        results.append({
            "publication_number": row.publication_number,
            "title": row.title,
            "abstract": row.abstract,
            "filing_date": str(row.filing_date) if row.filing_date else None,
            "grant_date": str(row.grant_date) if row.grant_date else None,
            "country": row.country,
            "cpc_codes": row.cpc_codes,
            "inventors": row.inventors,
            "assignee": row.assignee
        })
    
    output_path = Path("doc/analysis/comprehensive_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully retrieved {len(results)} patents.")
    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    main()
