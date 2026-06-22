import sqlite3
conn = sqlite3.connect("data/shadow_history.db")
rows = conn.execute("SELECT league, chapter, correct, total, weight FROM chapter_weights_v4 WHERE domain='sports' ORDER BY league, chapter").fetchall()

print("\n" + "="*70)
print("📊 CHAPTER WEIGHTS PER LEAGUE")
print("="*70)

current_league = ""
for r in rows:
    league, chapter, correct, total, weight = r
    if league != current_league:
        print(f"\n🏆 {league.upper()}")
        print("-"*50)
        current_league = league
    print(f"  Chapter {chapter:2}: {correct:4}/{total:4} = {correct/total*100:.1f}%  |  Weight: {weight:.2f}")

conn.close()
