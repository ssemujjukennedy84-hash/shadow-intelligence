import sqlite3

db = sqlite3.connect('data/shadow_history.db')

print('=== SHADOW STATUS ===')
print()

total = db.execute("SELECT COUNT(*) FROM predictions WHERE outcome!='pending'").fetchone()[0]
correct = db.execute("SELECT SUM(accuracy) FROM predictions WHERE outcome!='pending'").fetchone()[0]
print(f'Total Predictions: {total}')
print(f'Total Correct: {int(correct or 0)}')
if total > 0: print(f'Overall Win Rate: {correct/total*100:.1f}%')

print()
print('=== BY LEAGUE ===')
for league in ['epl','laliga','bundesliga','seriea']:
    t = db.execute(f"SELECT COUNT(*) FROM predictions WHERE league='{league}' AND outcome!='pending'").fetchone()[0]
    c = db.execute(f"SELECT SUM(accuracy) FROM predictions WHERE league='{league}' AND outcome!='pending'").fetchone()[0]
    if t > 0:
        print(f'{league.upper()}: {int(c or 0)}/{t} ({c/t*100:.1f}%)')
    else:
        print(f'{league.upper()}: Not yet backtested')

print()
print('=== TRADING ===')
tt = db.execute("SELECT COUNT(*) FROM predictions WHERE domain='trading' AND outcome!='pending'").fetchone()[0]
tc = db.execute("SELECT SUM(accuracy) FROM predictions WHERE domain='trading' AND outcome!='pending'").fetchone()[0]
if tt > 0: print(f'Trading: {int(tc or 0)}/{tt} ({tc/tt*100:.1f}%)')
else: print('Trading: Not yet backtested')

db.close()