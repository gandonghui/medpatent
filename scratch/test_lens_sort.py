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
            
    # Test 1: Simple sort string
    print("Testing sort with simple string...")
    payload1 = {
        "query": {"match": {"applicants.name": "Intuitive Surgical"}},
        "size": 1,
        "sort": "date_published:desc"
    }
    
    # Test 2: Sort object without nested order
    print("Testing sort with simple object...")
    payload2 = {
        "query": {"match": {"applicants.name": "Intuitive Surgical"}},
        "size": 1,
        "sort": [{"date_published": "desc"}]
    }

    # Test 3: No sort (default)
    print("Testing no sort...")
    payload3 = {
        "query": {"match": {"applicants.name": "Intuitive Surgical"}},
        "size": 1
    }

    for i, payload in enumerate([payload1, payload2, payload3], 1):
        print(f"\n--- Submitting Payload {i} ---")
        try:
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
                print(f"Success! Found {data.get('total').get('value')} patents.")
        except urllib.error.HTTPError as e:
            print(f"Failed! Status {e.code}")
            print(e.read().decode('utf-8'))

if __name__ == "__main__":
    test()
