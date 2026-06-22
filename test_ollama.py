import requests, time

start = time.time()
r = requests.post("http://localhost:11434/api/generate", json={
    "model": "qwen2.5:1.5b",
    "prompt": "Say hello in one word",
    "stream": False
}, timeout=10)
print(f"Status: {r.status_code}")
print(f"Response: {r.json().get('response','')}")
print(f"Time: {time.time()-start:.1f}s")