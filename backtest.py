"""
Shadow Backtest - Train on 2023/24, Test on 2025/26
Learns from old season, validates on new season.
"""

import json, requests, time, sqlite3, os
from collections import defaultdict

API = "http://127.0.0.1:8000"
FD_KEY = "3f866159549e4972825cecea5b405b5d"
LEAGUES = {"epl":"PL","laliga":"PD","bundesliga":"BL1","seriea":"SA","ligue1":"FL1"}
LEAGUE_NAMES = {"epl":"Premier League","laliga":"La Liga","bundesliga":"Bundesliga","seriea":"Serie A","ligue1":"Ligue 1"}

def fetch(league_key, season):
    info = LEAGUES[league_key]
    url = f"https://api.football-data.org/v4/competitions/{info}/matches?status=FINISHED&limit=380&season={season}"
    headers = {"X-Auth-Token": FD_KEY}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200: return []
        matches = r.json().get("matches",[])
        results = []
        for m in matches:
            ht = m.get("homeTeam",{}).get("name",""); at = m.get("awayTeam",{}).get("name","")
            sc = m.get("score",{}).get("fullTime",{}); fthg = sc.get("home",0) or 0; ftag = sc.get("away",0) or 0
            if not ht or not at: continue
            results.append({"home":ht,"away":at,"winner":ht if fthg>ftag else at if ftag>fthg else "draw","home_goals":fthg,"away_goals":ftag,"date":m.get("utcDate","")[:10]})
        results.sort(key=lambda x:x["date"])
        print(f"  {len(results)} matches fetched")
        return results
    except Exception as e:
        print(f"  Error: {e}")
        return []

def calc(matches, before_date):
    s = defaultdict(lambda:{"played":0,"wins":0,"draws":0,"losses":0,"goals_for":0,"goals_against":0,"clean_sheets":0,"form":[]})
    for m in matches:
        if m["date"] >= before_date: break
        h,a = m["home"],m["away"]; fh,fa = m["home_goals"],m["away_goals"]
        s[h]["played"]+=1; s[h]["goals_for"]+=fh; s[h]["goals_against"]+=fa
        if fa==0: s[h]["clean_sheets"]+=1
        if fh>fa: s[h]["wins"]+=1; s[h]["form"].append("W")
        elif fh<fa: s[h]["losses"]+=1; s[h]["form"].append("L")
        else: s[h]["draws"]+=1; s[h]["form"].append("D")
        s[a]["played"]+=1; s[a]["goals_for"]+=fa; s[a]["goals_against"]+=fh
        if fh==0: s[a]["clean_sheets"]+=1
        if fa>fh: s[a]["wins"]+=1; s[a]["form"].append("W")
        elif fa<fh: s[a]["losses"]+=1; s[a]["form"].append("L")
        else: s[a]["draws"]+=1; s[a]["form"].append("D")
    for t in s: s[t]["form"]="".join(s[t]["form"][-10:])
    return dict(s)

def run(league_key, matches, mode="train"):
    name = LEAGUE_NAMES[league_key]
    print(f"\n{'='*60}")
    print(f"{'TRAINING' if mode=='train' else 'TESTING'}: {name} ({len(matches)} matches)")
    print(f"{'='*60}")
    
    st = {"total":0,"correct":0,"wrong":0,"no_signal":0,"draws":0,"errors":0}
    test = matches[50:]
    
    for i, fix in enumerate(test):
        h,a,w = fix["home"],fix["away"],fix["winner"]
        if w == "draw": st["draws"] += 1; continue
        
        ts = calc(matches, fix["date"]); hs = ts.get(h,{}); aws = ts.get(a,{})
        
        try:
            resp = requests.post(f"{API}/analyze", json={
                "entity_1":h,"entity_2":a,"domain":"sports","league":league_key,
                "home_stats":{"name":h,"wins":hs.get("wins",0),"draws":hs.get("draws",0),"losses":hs.get("losses",0),"goals_for":hs.get("goals_for",0),"goals_against":hs.get("goals_against",0),"clean_sheets":hs.get("clean_sheets",0),"form":hs.get("form",""),"played":hs.get("played",0),"home_away":"home"},
                "away_stats":{"name":a,"wins":aws.get("wins",0),"draws":aws.get("draws",0),"losses":aws.get("losses",0),"goals_for":aws.get("goals_for",0),"goals_against":aws.get("goals_against",0),"clean_sheets":aws.get("clean_sheets",0),"form":aws.get("form",""),"played":aws.get("played",0),"home_away":"away"}
            }, timeout=30)
            
            if resp.status_code != 200: st["errors"] += 1; continue
            r = resp.json()
            
            pick = r.get("pick","")
            correct = (pick.lower() == w.lower())
            
            # LEARN from this outcome
            pid = r.get("pred_id","")
            if pid:
                try:
                    requests.post(f"{API}/learn", params={"pred_id":pid,"winner":w}, timeout=5)
                except: pass
            
            st["total"] += 1
            if correct: st["correct"] += 1
            else: st["wrong"] += 1
            
            if st["total"] % 30 == 0:
                wr = st["correct"]/st["total"]*100 if st["total"]>0 else 0
                print(f"  [{st['total']}] {wr:.1f}%")
        
        except: st["errors"] += 1
    
    if st["total"] > 0:
        wr = st["correct"]/st["total"]*100
        print(f"  FINAL: {st['correct']}/{st['total']} ({wr:.1f}%)")
        if wr >= 65: print("  🔥 STRONG")
        elif wr >= 55: print("  📈 MODERATE")
        else: print("  ⚠️ BELOW")
    return st


def show_weights():
    print(f"\n{'='*60}")
    print("LEARNED CHAPTER WEIGHTS")
    print(f"{'='*60}")
    try:
        db = sqlite3.connect("data/shadow_history.db")
        names = ["","Laying Plans","Waging War","Attack by Stratagem","Tactical Dispositions","Energy","Weak Points","Maneuvering","Variation","March","Terrain","Situations","Fire","Spies"]
        for lk in LEAGUES:
            rows = db.execute("SELECT chapter,weight,correct,total FROM chapter_weights_v4 WHERE domain='sports' AND league=? AND total>5 ORDER BY weight DESC LIMIT 5",(lk,)).fetchall()
            if rows:
                print(f"\n  {LEAGUE_NAMES[lk]}:")
                for r in rows:
                    n = names[r[0]] if r[0]<len(names) else f"Ch.{r[0]}"
                    bar = "█"*int(r[1]*10)
                    print(f"    {n:<20} {r[1]:.2f} {bar} ({r[2]}/{r[3]})")
        db.close()
    except: pass


if __name__ == "__main__":
    import sys
    
    try:
        r = requests.get(f"{API}/", timeout=3)
        if r.status_code != 200:
            print("API not running: python api/server.py")
            sys.exit(1)
    except:
        print("API not running: python api/server.py")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("PHASE 1: TRAINING ON 2023/24 SEASON")
    print("="*60)
    
    train_total = {"total":0,"correct":0}
    for lk in LEAGUES:
        print(f"\n📡 Training {LEAGUE_NAMES[lk]} on 2023...")
        matches = fetch(lk, 2023)
        if matches:
            st = run(lk, matches, "train")
            train_total["total"] += st["total"]
            train_total["correct"] += st["correct"]
    
    if train_total["total"] > 0:
        wr = train_total["correct"]/train_total["total"]*100
        print(f"\n📊 TRAINING COMPLETE: {train_total['correct']}/{train_total['total']} ({wr:.1f}%)")
    
    show_weights()
    
    print("\n" + "="*60)
    print("PHASE 2: TESTING ON 2025/26 SEASON")
    print("="*60)
    
    test_total = {"total":0,"correct":0}
    for lk in LEAGUES:
        print(f"\n📡 Testing {LEAGUE_NAMES[lk]} on 2025...")
        matches = fetch(lk, 2025)
        if matches:
            st = run(lk, matches, "test")
            test_total["total"] += st["total"]
            test_total["correct"] += st["correct"]
    
    if test_total["total"] > 0:
        wr = test_total["correct"]/test_total["total"]*100
        print(f"\n📊 TEST COMPLETE: {test_total['correct']}/{test_total['total']} ({wr:.1f}%)")
    
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    if train_total["total"] > 0:
        print(f"Training (2023/24): {train_total['correct']}/{train_total['total']} ({train_total['correct']/train_total['total']*100:.1f}%)")
    if test_total["total"] > 0:
        print(f"Testing  (2025/26): {test_total['correct']}/{test_total['total']} ({test_total['correct']/test_total['total']*100:.1f}%)")
    print("\n✅ Done.")