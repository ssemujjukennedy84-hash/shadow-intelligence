import requests, json

r = requests.post('http://127.0.0.1:8000/analyze', json={
    'entity_1': 'Manchester City',
    'entity_2': 'Luton Town',
    'domain': 'sports',
    'league': 'epl',
    'is_home_1': True,
    'home_stats': {
        'wins': 25, 'draws': 5, 'losses': 3,
        'goals_for': 78, 'goals_against': 22,
        'clean_sheets': 15, 'form': 'WWWWW', 'played': 33
    },
    'away_stats': {
        'wins': 4, 'draws': 6, 'losses': 23,
        'goals_for': 28, 'goals_against': 72,
        'clean_sheets': 2, 'form': 'LLLDL', 'played': 33
    }
}, timeout=120)

d = r.json()
reports = d.get('audit_reports', [])
pro = sum(1 for r in reports if r.get('verdict') == 'PRO')
con = sum(1 for r in reports if r.get('verdict') == 'CON')
neu = sum(1 for r in reports if r.get('verdict') == 'NEUTRAL')

print(f"Audits: {len(reports)} | PRO: {pro} | CON: {con} | NEUTRAL: {neu}")
print(f"Pick: {d.get('pick')}")
print(f"Convergence: {d.get('convergence_score')}")
print(f"Analysis: {d.get('final_analysis', '')[:250]}")
print()

for r in reports[:5]:
    print(f"  Ch.{r['chapter']} {r['chapter_name']}: {r['verdict']} - {r.get('strategic_insight', '')}")