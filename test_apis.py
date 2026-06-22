import requests

# Test 1: API-Football (your existing key)
print("=== API-FOOTBALL ===")
headers = {"x-apisports-key": "dd28cc88d9d6aa5d195a88d04b9c401c"}
r = requests.get("https://v3.football.api-sports.io/teams?search=Uruguay", headers=headers)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    teams = r.json().get("response", [])
    if teams:
        t = teams[0]["team"]
        print(f"Found: {t['name']} (ID: {t['id']})")
        # Get stats
        r2 = requests.get(f"https://v3.football.api-sports.io/teams/statistics?team={t['id']}&season=2026", headers=headers)
        print(f"Stats status: {r2.status_code}")
        if r2.status_code == 200:
            stats = r2.json().get("response", {})
            fixtures = stats.get("fixtures", {})
            print(f"Played: {fixtures.get('played',{}).get('total',0)}")
            print(f"Wins: {fixtures.get('wins',{}).get('total',0)}")

# Test 2: OpenLigaDB (free, no key)
print("\n=== OPENLIGADB ===")
r = requests.get("https://api.openligadb.de/getmatchdata/wm/2026")
print(f"Status: {r.status_code}")
if r.status_code == 200:
    print(f"Matches found: {len(r.json())}")

# Test 3: TheSportsDB (free, no key)
print("\n=== THESPORTSDB ===")
r = requests.get("https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t=Uruguay")
print(f"Status: {r.status_code}")
if r.status_code == 200:
    teams = r.json().get("teams", [])
    print(f"Teams found: {len(teams)}")