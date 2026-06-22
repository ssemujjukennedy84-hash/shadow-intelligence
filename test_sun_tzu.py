from engine.sun_tzu_mind import SunTzuMind

print("Loading Sun Tzu...")
mind = SunTzuMind()

print("\nAnalyzing France vs Senegal...\n")
result = mind.analyze(
    {'name': 'France', 'strength': 8.2, 'energy': 78, 'morale': 8, 'wins': 7, 'losses': 1, 'goals_for': 22, 'goals_against': 5, 'form': 'WWDWW'},
    {'name': 'Senegal', 'strength': 5.4, 'energy': 52, 'morale': 5, 'wins': 4, 'losses': 3, 'goals_for': 12, 'goals_against': 10, 'form': 'WLDLW'},
    'sports'
)

print(f"\nPICK: {result['pick']}")
print(f"VOTE: {result['pro_count']} PRO / {result['con_count']} CON / {result['neutral_count']} NEUTRAL")
print(f"\nBATTLE PLAN: {result['battle_plan'][:400]}")
print("\nCHAPTERS:")
for v in result['chapter_verdicts']:
    print(f"  Ch.{v['chapter']} {v['chapter_name']}: {v['verdict']}")