import requests, json, os

FOOTBALL_DATA_KEY = "3f866159549e4972825cecea5b405b5d"

LEAGUES = {
    "epl": {"id": "PL", "name": "Premier League"},
    "laliga": {"id": "PD", "name": "La Liga"},
    "bundesliga": {"id": "BL1", "name": "Bundesliga"},
    "seriea": {"id": "SA", "name": "Serie A"},
    "ligue1": {"id": "FL1", "name": "Ligue 1"},    "worldcup": {"id": "WC", "name": "World Cup 2026"},
}

os.makedirs("data/offline_matches", exist_ok=True)

for key, info in LEAGUES.items():
    print(f"Downloading {info['name']}...")
    headers = {"X-Auth-Token": FOOTBALL_DATA_KEY}
    url = f"https://api.football-data.org/v4/competitions/{info['id']}/matches?status=FINISHED&limit=380&season=2025"
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            data = r.json()
            filename = f"data/offline_matches/{key}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f)
            count = len(data.get("matches", []))
            print(f"  Saved {count} matches")
        else:
            print(f"  Error: {r.status_code}")
    except Exception as e:
        print(f"  Failed: {e}")

print("\nDone. All leagues saved offline.")