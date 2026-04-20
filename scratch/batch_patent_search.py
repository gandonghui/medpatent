import json
import urllib.request
import os
import sys
import time
from datetime import datetime
from pathlib import Path

def run_search(label, query_payload):
    with open('.env') as f:
        env = f.read()
    
    api_key = ''
    for line in env.splitlines():
        if line.startswith('LENS_API_KEY='):
            api_key = line.split('=')[1].strip().strip('"').strip("'")
            break
            
    results_dir = Path(".agents/harness/data/search_results")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"--- Running search: {label} ---")
    all_hits = []
    offset = 0
    limit = 100
    
    while True:
        payload = query_payload.copy()
        payload["size"] = limit
        payload["from"] = offset
        payload["sort"] = [{"date_published": "desc"}]
        payload["include"] = ["lens_id", "biblio", "abstract", "claims", "description", "families", "legal_status"]
        
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
                
                all_hits.extend(hits)
                print(f"  Fetched {len(all_hits)} / {total}...")
                
                if not hits or len(all_hits) >= total or len(all_hits) >= 1000:
                    break
                offset += limit
                time.sleep(1) 
        except Exception as e:
            print(f"  Error: {e}")
            break
            
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = results_dir / f"lens_batch_{label.lower().replace(' ', '_')}_{ts}.json"
    
    envelope = {
        "meta": {
            "source": "lens.org",
            "query_label": label,
            "timestamp": datetime.now().isoformat(),
            "total_hits": len(all_hits),
            "payload": query_payload
        },
        "raw": {"data": all_hits, "total": len(all_hits)}
    }
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(envelope, f, ensure_ascii=False, indent=2)
    print(f"  Saved {len(all_hits)} results to {out_path}")
    return out_path

if __name__ == "__main__":
    # Entity 1: Intuitive Surgical, Inc.
    query_inc = {
        "query": {
            "bool": {
                "must": [
                    {"query_string": {
                        "query": "\"Intuitive Surgical Inc\"",
                        "fields": ["biblio.parties.applicants.extracted_name.value"]
                    }},
                    {"query_string": {
                        "query": "3D OR vision OR image OR optical OR stereoscopic OR visualization OR camera OR endoscope",
                        "fields": ["biblio.title.text", "abstract.text", "claims.text"]
                    }}
                ]
            }
        }
    }
    run_search("Intuitive Inc Accurate", query_inc)
    
    # Entity 2: Intuitive Surgical Operations, Inc.
    query_ops = {
        "query": {
            "bool": {
                "must": [
                    {"query_string": {
                        "query": "\"Intuitive Surgical Operations\"",
                        "fields": ["biblio.parties.applicants.extracted_name.value"]
                    }},
                    {"query_string": {
                        "query": "3D OR vision OR image OR optical OR stereoscopic OR visualization OR camera OR endoscope",
                        "fields": ["biblio.title.text", "abstract.text", "claims.text"]
                    }}
                ]
            }
        }
    }
    run_search("Intuitive Operations Accurate", query_ops)
