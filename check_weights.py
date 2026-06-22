import sqlite3
conn = sqlite3.connect("data/shadow_history.db")
rows = conn.execute("SELECT chapter, correct, total, weight FROM chapter_weights_v4 WHERE domain='sports' ORDER BY chapter").fetchall()
print("Chapter | Correct | Total | Weight")
print("-" * 40)
for r in rows:
    print(f"  {r[0]:2}    | {r[1]:5}   | {r[2]:4}  | {r[3]:.2f}")
conn.close()
