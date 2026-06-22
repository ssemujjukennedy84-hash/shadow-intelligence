import requests, json

r = requests.post('http://127.0.0.1:8000/analyze', json={
    'entity_1': 'Manchester City', 'entity_2': 'Luton Town',
    'domain': 'sports', 'league': 'epl', 'is_home_1': True,
    'home_stats': {'wins': 25, 'draws': 5, 'losses': 3, 'goals_for': 78, 'goals_against': 22, 'clean_sheets': 15, 'form': 'WWWWW', 'played': 33},
    'away_stats': {'wins': 4, 'draws': 6, 'losses': 23, 'goals_for': 28, 'goals_against': 72, 'clean_sheets': 2, 'form': 'LLLDL', 'played': 33}
}, timeout=90)

d = r.json()
print('Pick:', d.get('pick'))
print('Score:', d.get('pick_score'), '/', d.get('opponent_score'))
print('Margin:', d.get('margin'))
print('Conv:', d.get('convergence_score'))
print()

reports = d.get('audit_reports', [])
if reports:
    for rpt in reports:
        v = rpt.get('verdict', '?')
        expl = rpt.get('verdict_explanation', '')[:100]
        print(f"Ch.{rpt.get('chapter')}: {v} - {expl}")
else:
    print('No audit reports')
    print('Available keys:', list(d.keys()))