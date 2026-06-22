import requests

headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json", "Referer": "https://www.fifa.com/"}

# Try to find World Cup 2026 by searching competitions
# Common competition IDs: 17 (old World Cup), try different ones
ids = [17, 103, 200, 201, 202, 500, 512, 1000, 2026, 2000, 1, 3, 5, 10, 20, 50, 100]

for cid in ids:
    try:
        r = requests.get(f"https://api.fifa.com/api/v3/calendar/matches?competitionId={cid}&season=2026&limit=1", headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            results = data.get("Results", [])
            if results:
                m = results[0]
                date = m.get("Date", "?")
                home = m.get("Home", {})
                away = m.get("Away", {})
                # Try to get team names
                h_name = home.get("ShortClubName", "?") if isinstance(home, dict) else "?"
                a_name = away.get("ShortClubName", "?") if isinstance(away, dict) else "?"
                year = date[:4] if date else "?"
                print(f"ID {cid}: {h_name} vs {a_name} ({year})")
    except: pass