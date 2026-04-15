import sys
import os
import json

# Add skill python path to sys.path
SKILL_ROOT = r'c:\Users\admin\Desktop\工作\medpatent\.agents\skills\bigquery-patent-search'
sys.path.insert(0, os.path.join(SKILL_ROOT, 'python'))

from bigquery_search import BigQueryPatentSearch

def main():
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'my-project-gemini-test-485607'
    try:
        searcher = BigQueryPatentSearch()
        
        # Broader Query: just find any recent patents from Intuitive to see the assignee structure
        print("Checking recent patents from Intuitive Surgical to see assignee name...")
        results = searcher.search_patents(
            query="surgical", 
            limit=5,
            assignee="Intuitive Surgical"
        )
        
        if not results:
            print("Still 0. Trying fuzzy assignee search...")
            # Let's adjust the search logic to see if we can find them
            # I'll just run a manual SQL query via searcher.client to be sure
            sql = """
                SELECT DISTINCT a 
                FROM `patents-public-data.patents.publications`, UNNEST(assignee) as a 
                WHERE REGEXP_CONTAINS(a, r'(?i)Intuitive Surgical') 
                LIMIT 10
            """
            print(f"Running SQL: {sql}")
            query_job = searcher.client.query(sql)
            assignees = [row.a for row in query_job]
            print(f"Found assignee variants: {assignees}")
        else:
            print(f"Found patents. Assignee in results: {results[0]['assignee']}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
