import os
from google.cloud import bigquery
from typing import List, Dict, Optional

class BigQueryPatentSearch:
    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.environ.get('GOOGLE_CLOUD_PROJECT')
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable or project_id must be set")
        self.client = bigquery.Client(project=self.project_id)
        self.dataset = "patents-public-data.patents"

    def search_patents(self, 
                       query: str, 
                       limit: int = 100, 
                       country: Optional[str] = None, 
                       assignee: Optional[str] = None,
                       start_year: Optional[int] = None, 
                       end_year: Optional[int] = None) -> List[Dict]:
        """
        Search for patents using keyword search in titles, abstracts and claims.
        """
        filters = []
        if country:
            filters.append(f"tp.country_code = '{country}'")
        if start_year:
            filters.append(f"EXTRACT(YEAR FROM tp.filing_date) >= {start_year}")
        if end_year:
            filters.append(f"EXTRACT(YEAR FROM tp.filing_date) <= {end_year}")
        
        if assignee:
            # Check unnested assignee array
            filters.append(f"EXISTS (SELECT 1 FROM UNNEST(tp.assignee) AS a WHERE REGEXP_CONTAINS(a, r'(?i){assignee}'))")

        # Split keywords from query and ensure they appear in title or abstract
        keywords = query.split()
        keyword_filters = []
        for kw in keywords:
            kw_clean = kw.strip().replace("'", "\\'")
            keyword_filters.append(f"""(
                REGEXP_CONTAINS(tp.title_localized[SAFE_OFFSET(0)].text, r'(?i){kw_clean}') OR
                REGEXP_CONTAINS(tp.abstract_localized[SAFE_OFFSET(0)].text, r'(?i){kw_clean}')
            )""")
        
        where_clause = " AND ".join(keyword_filters)
        if filters:
            where_clause = (where_clause + " AND " if where_clause else "") + " AND ".join(filters)

        sql = f"""
            SELECT 
                tp.publication_number,
                tp.title_localized[SAFE_OFFSET(0)].text as title,
                tp.abstract_localized[SAFE_OFFSET(0)].text as abstract,
                tp.filing_date,
                tp.grant_date,
                tp.country_code as country,
                (SELECT ARRAY_AGG(DISTINCT c.code) FROM UNNEST(tp.cpc) as c) as cpc_codes,
                (SELECT ARRAY_AGG(DISTINCT i) FROM UNNEST(tp.inventor) as i) as inventors,
                (SELECT a FROM UNNEST(tp.assignee) as a LIMIT 1) as assignee
            FROM 
                `patents-public-data.patents.publications` as tp
            WHERE 
                {where_clause}
            ORDER BY tp.filing_date DESC
            LIMIT {limit}
        """
        
        query_job = self.client.query(sql)
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
        return results

    def get_patent(self, patent_number: str) -> Optional[Dict]:
        """
        Retrieve full details for a single patent.
        """
        sql = f"""
            SELECT 
                publication_number,
                title_localized[SAFE_OFFSET(0)].text as title,
                abstract_localized[SAFE_OFFSET(0)].text as abstract,
                claims_localized[SAFE_OFFSET(0)].text as claims,
                description_localized[SAFE_OFFSET(0)].text as description,
                filing_date,
                grant_date,
                country_code as country,
                (SELECT ARRAY_AGG(DISTINCT c.code) FROM UNNEST(cpc) as c) as cpc_codes,
                (SELECT ARRAY_AGG(DISTINCT i) FROM UNNEST(inventor) as i) as inventors,
                (SELECT a FROM UNNEST(assignee) as a LIMIT 1) as assignee
            FROM 
                `patents-public-data.patents.publications`
            WHERE 
                publication_number = '{patent_number}'
            LIMIT 1
        """
        query_job = self.client.query(sql)
        for row in query_job:
            return {
                "publication_number": row.publication_number,
                "title": row.title,
                "abstract": row.abstract,
                "claims": row.claims,
                "description": row.description,
                "filing_date": str(row.filing_date) if row.filing_date else None,
                "grant_date": str(row.grant_date) if row.grant_date else None,
                "country": row.country,
                "cpc_codes": row.cpc_codes,
                "inventors": row.inventors,
                "assignee": row.assignee
            }
        return None
