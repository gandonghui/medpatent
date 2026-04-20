import json
import urllib.request
import os
import sys
import time
from datetime import datetime
from pathlib import Path

def run_multi_page_search(label, query_body, max_results=2000):
    with open('.env') as f:
        env = f.read()
    
    api_key = ''
    for line in env.splitlines():
        if line.startswith('LENS_API_KEY='):
            api_key = line.split('=')[1].strip().strip('"').strip("'")
            break
            
    results_dir = Path(".agents/harness/data/search_results")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"--- Full Search: {label} ---")
    all_hits = []
    offset = 0
    limit = 100 
    
    while len(all_hits) < max_results:
        payload = {
            **query_body,
            "size": limit,
            "from": offset,
            "sort": [{"date_published": "desc"}],
            "include": ["lens_id", "biblio", "abstract", "claims", "description", "families", "legal_status"]
        }
        
        req = urllib.request.Request(
            'https://api.lens.org/patent/search',
            data=json.dumps(payload).encode('utf-8'),
            headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
            method='POST'
        )
        
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                hits = data.get("data", [])
                total = data.get("total", 0)
                if isinstance(total, dict): total = total.get("value", 0)
                
                if not hits:
                    print("  No more hits returned.")
                    break
                    
                all_hits.extend(hits)
                print(f"  Fetched {len(all_hits)} / {total}...")
                
                if len(all_hits) >= total:
                    break
                    
                offset += limit
                if offset >= 10000:
                    break
                time.sleep(0.5)
        except Exception as e:
            print(f"  Error: {e}")
            break
            
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = results_dir / f"lens_full_report_{ts}.json"
    
    envelope = {
        "meta": {
            "source": "lens.org",
            "query_label": label,
            "timestamp": datetime.now().isoformat(),
            "total_hits": len(all_hits),
            "original_total": total
        },
        "raw": {"data": all_hits, "total": len(all_hits)}
    }
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(envelope, f, ensure_ascii=False, indent=2)
    print(f"  Saved total {len(all_hits)} results to {out_path}")
    return out_path

if __name__ == "__main__":
    # 使用与 lens_search.py 相同逻辑的关键词检索
    query = {
        "query": {
            "query_string": {
                "query": "intuitive surgical",
                "fields": ["title", "abstract", "claims.text", "description.text"],
                "default_operator": "AND"
            }
        }
    }
    run_multi_page_search("Intuitive_Surgical_Full", query)
