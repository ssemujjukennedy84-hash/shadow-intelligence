import requests
from datetime import datetime

# FIFA World Cup 2026 API endpoint
# This endpoint serves the official match data
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Origin": "https://www.fifa.com",
    "Referer": "https://www.fifa.com/"
}

# FIFA World Cup 2026 match data
urls = [
    "https://fdh-api.fifa.com/v1/competitions/17/matches?season=2026&stage=GROUP&limit=50",
    "https://api.fifa.com/api/v3/calendar/matches?competitionId=17&season=2026&limit=50",
    "https://www.fifa.com/api/competitions/17/matches?season=2026&limit=50"
]

for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=15)
        print(f"\nURL: {url[:60]}...")
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            # Try different response structures
            if isinstance(data, list):
                print(f"Matches: {len(data)}")
                for m in data[:3]:
                    print(f"  {m}")
            elif isinstance(data, dict):
                results = data.get("Results") or data.get("results") or data.get("data") or data.get("matches") or []
                if results:
                    print(f"Matches found: {len(results)}")
                    for m in results[:3]:
                        if isinstance(m, dict):
                            ht = m.get("HomeTeam") or m.get("homeTeam") or m.get("home", {})
                            at = m.get("AwayTeam") or m.get("awayTeam") or m.get("away", {})
                            h_name = ht.get("TeamName") or ht.get("name") or ht.get("teamName", "") if isinstance(ht, dict) else ""
                            a_name = at.get("TeamName") or at.get("name") or at.get("teamName", "") if isinstance(at, dict) else ""
                            score = m.get("Score") or m.get("score") or {}
                            print(f"  {h_name} vs {a_name}")
                else:
                    print(f"Keys: {list(data.keys())[:5]}")
            else:
                print(f"Type: {type(data)}")
    except Exception as e:
        print(f"Error: {e}")