import requests

headers = {"x-apisports-key": "dd28cc88d9d6aa5d195a88d04b9c401c"}

# Uruguay
r = requests.get("https://v3.football.api-sports.io/teams?search=Uruguay", headers=headers)
t1 = r.json()["response"][0]["team"]
print(f"Uruguay: ID={t1['id']}, Name={t1['name']}")

r2 = requests.get(f"https://v3.football.api-sports.io/teams/statistics?team={t1['id']}&season=2026", headers=headers)
stats = r2.json()["response"]
if isinstance(stats, list): stats = stats[0] if stats else {}
fixtures = stats.get("fixtures", {})
goals = stats.get("goals", {})
print(f"  Played: {fixtures.get('played',{}).get('total',0)}")
print(f"  Wins: {fixtures.get('wins',{}).get('total',0)}")
print(f"  Draws: {fixtures.get('draws',{}).get('total',0)}")
print(f"  Losses: {fixtures.get('loses',{}).get('total',0)}")
print(f"  Goals For: {goals.get('for',{}).get('total',{}).get('total',0)}")

# Cape Verde
r = requests.get("https://v3.football.api-sports.io/teams?search=Cape Verde", headers=headers)
if r.json()["response"]:
    t2 = r.json()["response"][0]["team"]
    print(f"\nCape Verde: ID={t2['id']}, Name={t2['name']}")
    r2 = requests.get(f"https://v3.football.api-sports.io/teams/statistics?team={t2['id']}&season=2026", headers=headers)
    stats = r2.json()["response"]
    if isinstance(stats, list): stats = stats[0] if stats else {}
    fixtures = stats.get("fixtures", {})
    goals = stats.get("goals", {})
    print(f"  Played: {fixtures.get('played',{}).get('total',0)}")
    print(f"  Wins: {fixtures.get('wins',{}).get('total',0)}")