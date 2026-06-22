import requests

resp = requests.post('http://127.0.0.1:8000/analyze', json={
    'entity_1': 'Liverpool FC', 'entity_2': 'AFC Bournemouth', 'domain': 'sports', 'league': 'epl',
    'home_stats': {'name':'Liverpool FC','wins':20,'draws':5,'losses':3,'goals_for':65,'goals_against':25,'clean_sheets':12,'form':'WWDLW','played':28,'home_away':'home'},
    'away_stats': {'name':'AFC Bournemouth','wins':8,'draws':6,'losses':14,'goals_for':30,'goals_against':48,'clean_sheets':3,'form':'LLWLL','played':28,'home_away':'away'}
}, timeout=10)

d = resp.json()
pick = d.get('pick', '')
actual = 'Liverpool FC'
correct = (pick.lower() == actual.lower())

print(f'Pick: "{pick}"')
print(f'Actual: "{actual}"')
print(f'Match: {pick.lower() == actual.lower()}')
print(f'Correct: {correct}')