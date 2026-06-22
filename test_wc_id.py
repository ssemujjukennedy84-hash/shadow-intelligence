import requests

headers = {"x-apisports-key": "dd28cc88d9d6aa5d195a88d04b9c401c"}

# Search for World Cup leagues
r = requests.get("https://v3.football.api-sports.io/leagues?search=world&season=2026", headers=headers)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    leagues = r.json().get("response", [])
    for l in leagues[:10]:
        league = l.get("league", {})
        country = l.get("country", {})
        print(f"  ID={league.get('id')} - {league.get('name')} ({country.get('name')})")

# Also try searching for current seasons
print("\n=== ALL LEAGUES WITH SEASON 2026 ===")
r = requests.get("https://v3.football.api-sports.io/leagues?season=2026&current=true", headers=headers)
if r.status_code == 200:
    leagues = r.json().get("response", [])
    for l in leagues[:15]:
        league = l.get("league", {})
        country = l.get("country", {})
        print(f"  ID={league.get('id')} - {league.get('name')} ({country.get('name')})")