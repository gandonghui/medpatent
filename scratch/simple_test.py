import json
import urllib.request
import os

def test():
    with open('.env') as f:
        env = f.read()
    
    api_key = ''
    for line in env.splitlines():
        if line.startswith('LENS_API_KEY='):
            api_key = line.split('=')[1].strip().strip('"').strip("'")
            break
            
    # Test Payload
    payload = {
        "query": {"match": {"applicants.name": "Intuitive Surgical"}},
        "size": 1
    }

    print(f"\n--- Submitting Payload ---")
    req = urllib.request.Request(
        'https://api.lens.org/patent/search',
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        },
        method='POST'
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    test()
