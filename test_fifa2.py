import requests, json

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.fifa.com/"
}

r = requests.get("https://api.fifa.com/api/v3/calendar/matches?competitionId=17&season=2026&limit=5", headers=headers)

if r.status_code == 200:
    data = r.json()
    results = data.get("Results", [])
    print(f"Total results: {len(results)}")
    
    for m in results[:3]:
        print(f"\n--- Match ---")
        # Print all keys to understand structure
        if isinstance(m, dict):
            for key in m:
                val = m[key]
                if isinstance(val, (str, int, float)):
                    print(f"  {key}: {val}")
                elif isinstance(val, dict):
                    for k2, v2 in val.items():
                        if isinstance(v2, (str, int, float)):
                            print(f"  {key}.{k2}: {v2}")
                        elif isinstance(v2, list):
                            print(f"  {key}.{k2}: [list len={len(v2)}]")
                        elif isinstance(v2, dict):
                            print(f"  {key}.{k2}: [dict]")
else:
    print(f"Failed: {r.status_code}")
    print(r.text[:500])