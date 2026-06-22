import requests

headers = {'x-apisports-key': 'dd28cc88d9d6aa5d195a88d04b9c401c'}

# Test Man City
r = requests.get('https://v3.football.api-sports.io/teams?search=Manchester City', headers=headers, timeout=10)
print('Search status:', r.status_code)

if r.status_code == 200:
    teams = r.json().get('response', [])
    if teams:
        t = teams[0]['team']
        tid = t['id']
        print('Found:', t['name'], 'ID:', tid)
        
        r2 = requests.get(f'https://v3.football.api-sports.io/teams/statistics?team={tid}&season=2026', headers=headers, timeout=10)
        print('Stats status:', r2.status_code)
        if r2.status_code == 200:
            stats = r2.json().get('response', {})
            if isinstance(stats, list):
                stats = stats[0] if stats else {}
            fixtures = stats.get('fixtures', {})
            goals = stats.get('goals', {})
            print('Played:', fixtures.get('played', {}).get('total', 0))
            print('Wins:', fixtures.get('wins', {}).get('total', 0))
            print('Draws:', fixtures.get('draws', {}).get('total', 0))
            print('Losses:', fixtures.get('loses', {}).get('total', 0))
    else:
        print('No teams found')
else:
    print('Error:', r.status_code)