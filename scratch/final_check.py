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
            
    # Test Payload with NO SORT
    payload = {
        "query": {"match": {"applicants.name": "Intuitive Surgical"}},
        "size": 1
    }

    print(f"\n--- Submitting Payload (No Sort) ---")
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
            print("Success!")
            print(f"Total: {data.get('total')}")
            if data.get('data'):
                print(f"First result: {data['data'][0].get('pub_key')}")
    except Exception as e:
        print(f"Failed: {e}")
        if hasattr(e, 'read'):
            print(e.read().decode('utf-8'))

if __name__ == "__main__":
    test()
