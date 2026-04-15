import sys
import os
import json

# Add skill python path to sys.path
SKILL_ROOT = r'c:\Users\admin\Desktop\工作\medpatent\.agents\skills\bigquery-patent-search'
sys.path.insert(0, os.path.join(SKILL_ROOT, 'python'))

from bigquery_search import BigQueryPatentSearch

def main():
    # Environment Setup
    os.environ['GOOGLE_CLOUD_PROJECT'] = 'my-project-gemini-test-485607'
    
    try:
        searcher = BigQueryPatentSearch()
        
        # Execute search for 10 patents
        # Keywords: 3D imaging, vision system
        # Assignee: Intuitive Surgical
        print("Executing BigQuery patent search for Intuitive Surgical (3D imaging)...")
        results = searcher.search_patents(
            query="3D imaging", 
            limit=10,
            assignee="Intuitive Surgical"
        )
        
        # Save results to search_results.json for traceability
        output_file = 'search_results.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully retrieved {len(results)} patents.")
        print(f"Results saved to {output_file}")
        
    except Exception as e:
        print(f"Error during search: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
