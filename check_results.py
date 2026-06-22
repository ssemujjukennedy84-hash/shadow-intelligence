import sqlite3

db = sqlite3.connect('data/shadow_history.db')

total = db.execute("SELECT COUNT(*) FROM predictions WHERE outcome!='pending'").fetchone()[0]
correct = db.execute("SELECT SUM(accuracy) FROM predictions WHERE outcome!='pending'").fetchone()[0]

print(f'Total predictions recorded: {total}')
print(f'Total correct: {int(correct or 0)}')
if total > 0:
    print(f'Overall win rate: {correct/total*100:.1f}%')
print()

for league in ['epl','laliga','bundesliga','seriea','ligue1']:
    t = db.execute(f"SELECT COUNT(*) FROM predictions WHERE league='{league}' AND outcome!='pending'").fetchone()[0]
    c = db.execute(f"SELECT SUM(accuracy) FROM predictions WHERE league='{league}' AND outcome!='pending'").fetchone()[0]
    if t > 0:
        print(f'{league}: {int(c or 0)}/{t} ({c/t*100:.1f}%)')

print()
print('Top 5 chapter weights (EPL):')
rows = db.execute("SELECT chapter, weight, correct, total FROM chapter_weights_v4 WHERE league='epl' AND total>10 ORDER BY weight DESC LIMIT 5").fetchall()
names = ["","Laying Plans","Waging War","Attack by Stratagem","Tactical Dispositions","Energy","Weak Points and Strong","Maneuvering","Variation in Tactics","The Army on the March","Terrain","The Nine Situations","Attack by Fire","Use of Spies"]
for r in rows:
    name = names[r[0]] if r[0] < len(names) else f'Ch.{r[0]}'
    print(f'  {name}: {r[1]:.2f} ({r[2]}/{r[3]} correct)')

db.close()
