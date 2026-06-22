import requests

headers = {'X-Auth-Token': '3f866159549e4972825cecea5b405b5d'}
r = requests.get('https://api.football-data.org/v4/competitions', headers=headers)

if r.status_code == 200:
    comps = r.json().get('competitions', [])
    for c in comps[:15]:
        season = c.get('currentSeason', {})
        print(f"{c['id']} - {c['name']} ({c.get('area',{}).get('name','')}) - Season: {season.get('id','none')}")
else:
    print(f"Error: {r.status_code}")
    print(r.text[:300])