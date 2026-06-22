import sqlite3
db = sqlite3.connect('data/shadow_history.db')
total = db.execute('SELECT COUNT(*) FROM predictions').fetchone()[0]
correct = db.execute(\"SELECT COUNT(*) FROM predictions WHERE outcome='correct'\").fetchone()[0]
wrong = db.execute(\"SELECT COUNT(*) FROM predictions WHERE outcome='incorrect'\").fetchone()[0]
print(f'Total: {total}, Correct: {correct}, Wrong: {wrong}')
if correct + wrong > 0:
    print(f'Win rate: {correct/(correct+wrong)*100:.1f}%')
db.close()
