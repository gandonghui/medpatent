import json
import urllib.request
import os
import sys
from datetime import datetime
from pathlib import Path

def search_intuitive_vision():
    with open('.env') as f:
        env = f.read()
    
    api_key = ''
    for line in env.splitlines():
        if line.startswith('LENS_API_KEY='):
            api_key = line.split('=')[1].strip().strip('"').strip("'")
            break
            
    payload = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"applicants.name": "Intuitive Surgical"}},
                    {"query_string": {
                        "query": "3D OR imaging OR vision OR optical OR camera",
                        "fields": ["biblio.title.text", "abstract.text"]
                    }}
                ]
            }
        },
        "size": 50,
        "sort": [{"relevance": "desc"}],
        "include": ["lens_id", "biblio", "abstract", "claims", "description", "families", "legal_status"]
    }
    
    print(f"Submitting targeted query...")
    req = urllib.request.Request(
        'https://api.lens.org/patent/search',
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            total = data.get('total', 0)
            if isinstance(total, dict): total = total.get('value', 0)
            print(f"Success! Found {total} results.")
            
            # Save format compatible with lens_search.py
            results_dir = Path(".agents/harness/data/search_results")
            results_dir.mkdir(parents=True, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_path = results_dir / f"lens_intuitive_vision_{ts}.json"
            
            envelope = {
                "meta": {
                    "source": "lens.org",
                    "query": "Intuitive Surgical 3D/Vision Targeted",
                    "timestamp": datetime.now().isoformat(),
                    "total_hits": total,
                    "returned": len(data.get("data", [])),
                    "assignee": "Intuitive Surgical"
                },
                "raw": data
            }
            
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(envelope, f, ensure_ascii=False, indent=2)
            print(f"Results saved to {out_path}")
            return str(out_path)
    except Exception as e:
        print(f"Failed: {e}")
        if hasattr(e, 'read'):
            print(e.read().decode('utf-8'))
        return None

if __name__ == "__main__":
    search_intuitive_vision()
