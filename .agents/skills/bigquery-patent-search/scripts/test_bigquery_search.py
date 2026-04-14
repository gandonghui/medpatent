import os
import sys
import json
from datetime import datetime

# Add python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))
from bigquery_search import BigQueryPatentSearch

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "Query required. Usage: python test_bigquery_search.py <query> [limit]"}))
        return

    query = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')

    if not project_id:
        print(json.dumps({"success": False, "error": "GOOGLE_CLOUD_PROJECT env var must be set"}))
        return

    try:
        searcher = BigQueryPatentSearch(project_id=project_id)
        print(f"Searching for: {query} (Limit: {limit})...", file=sys.stderr)
        
        results = searcher.search_patents(query=query, limit=limit)
        
        output = {
            "success": True,
            "query": query,
            "result_count": len(results),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(output, indent=2))
        
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))

if __name__ == "__main__":
    main()
