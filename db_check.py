import sqlite3

db = sqlite3.connect('data/shadow_history.db')

count = db.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]
pending = db.execute("SELECT COUNT(*) FROM predictions WHERE outcome='pending'").fetchone()[0]
correct = db.execute("SELECT SUM(accuracy) FROM predictions WHERE outcome='correct'").fetchone()[0]

print(f"All predictions: {count}")
print(f"Pending: {pending}")
print(f"Correct: {int(correct or 0)}")

tables = db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print(f"Tables: {[t[0] for t in tables]}")

db.close()