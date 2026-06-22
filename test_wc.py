import requests

headers = {'X-Auth-Token': '3f866159549e4972825cecea5b405b5d'}

# Test Uruguay
r = requests.get('https://api.football-data.org/v4/teams?search=Uruguay', headers=headers)
print('Search status:', r.status_code)

if r.status_code == 200:
    teams = r.json().get('teams', [])
    if teams:
        t = teams[0]
        print('Found:', t.get('name'), 'ID:', t.get('id'))
        
        r2 = requests.get(f'https://api.football-data.org/v4/teams/{t["id"]}/matches?limit=5&status=FINISHED', headers=headers)
        print('Matches status:', r2.status_code)
        matches = r2.json().get('matches', [])
        print('Matches found:', len(matches))
        for m in matches[:3]:
            home = m['homeTeam']['name']
            away = m['awayTeam']['name']
            hg = m['score']['fullTime']['home']
            ag = m['score']['fullTime']['away']
            print(f'  {home} {hg}-{ag} {away}')
    else:
        print('No teams found')

# Test Cape Verde
print()
r = requests.get('https://api.football-data.org/v4/teams?search=Cape Verde', headers=headers)
print('Search status:', r.status_code)
if r.status_code == 200:
    teams = r.json().get('teams', [])
    if teams:
        t = teams[0]
        print('Found:', t.get('name'), 'ID:', t.get('id'))