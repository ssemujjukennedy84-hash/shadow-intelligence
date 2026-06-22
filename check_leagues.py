import sqlite3
conn = sqlite3.connect("data/shadow_history.db")
rows = conn.execute("SELECT DISTINCT league FROM chapter_weights_v4 WHERE domain='sports'").fetchall()
print("Leagues in database:")
for r in rows:
    print(f"  {r[0]}")
conn.close()
