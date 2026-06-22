import requests

headers = {"x-apisports-key": "dd28cc88d9d6aa5d195a88d04b9c401c"}

# Get World Cup 2026 - both finished and scheduled
print("=== FINISHED MATCHES ===")
r = requests.get("https://v3.football.api-sports.io/fixtures?league=1&season=2026&status=FT&limit=5", headers=headers)
if r.status_code == 200:
    for f in r.json().get("response", [])[:3]:
        home = f["teams"]["home"]["name"]
        away = f["teams"]["away"]["name"]
        hg = f["goals"]["home"]
        ag = f["goals"]["away"]
        print(f"  {home} {hg}-{ag} {away}")

print("\n=== UPCOMING ===")
r = requests.get("https://v3.football.api-sports.io/fixtures?league=1&season=2026&status=NS&limit=5", headers=headers)
if r.status_code == 200:
    for f in r.json().get("response", [])[:5]:
        home = f["teams"]["home"]["name"]
        away = f["teams"]["away"]["name"]
        date = f["fixture"]["date"][:10]
        print(f"  {home} vs {away} ({date})")