import sqlite3
conn = sqlite3.connect("data/shadow_history.db")
rows = conn.execute("SELECT chapter, SUM(correct) as total_correct, SUM(total) as total_matches, AVG(weight) as avg_weight FROM chapter_weights_v4 WHERE domain='sports' GROUP BY chapter ORDER BY avg_weight DESC").fetchall()

print("\n" + "="*60)
print("📊 TOP PERFORMING CHAPTERS (ALL LEAGUES)")
print("="*60)
print("Chapter | Correct | Total | Win Rate | Avg Weight")
print("-"*50)
for r in rows:
    chapter, correct, total, weight = r
    print(f"  {chapter:2}    | {correct:5}  | {total:4}  | {correct/total*100:.1f}%   | {weight:.2f}")
conn.close()
