import json
import os
from collections import defaultdict
from engine.sun_tzu_engine import SunTzuEngine
from engine.quant_engine import QuantEngine
from engine.data_mapper import map_sports as dm

LEAGUE_NAMES = {"epl":"Premier League","laliga":"La Liga","bundesliga":"Bundesliga","seriea":"Serie A","ligue1":"Ligue 1"}

def load_matches(league_key):
    with open(f"data/offline_matches/{league_key}.json","r") as f:
        data=json.load(f)
    return data.get("matches",[])

def get_team_stats(team_name, matches):
    played=wins=draws=losses=gf=ga=0
    recent=[]
    for m in matches:
        home=m.get("homeTeam",{}).get("name","")
        away=m.get("awayTeam",{}).get("name","")
        score=m.get("score",{}).get("fullTime",{})
        hg=score.get("home",0) or 0
        ag=score.get("away",0) or 0
        if home==team_name:
            played+=1; gf+=hg; ga+=ag
            if hg>ag: wins+=1; recent.append("W")
            elif hg<ag: losses+=1; recent.append("L")
            else: draws+=1; recent.append("D")
        elif away==team_name:
            played+=1; gf+=ag; ga+=hg
            if ag>hg: wins+=1; recent.append("W")
            elif ag<hg: losses+=1; recent.append("L")
            else: draws+=1; recent.append("D")
    return {"name":team_name,"played":played,"wins":wins,"draws":draws,"losses":losses,"goals_for":gf,"goals_against":ga,"form":"".join(recent[-5:])}

st=SunTzuEngine()
quant=QuantEngine()
all_results=[]
total_correct=0
total_matches=0

for league_key in ["epl","laliga","bundesliga","seriea","ligue1"]:
    matches=load_matches(league_key)
    if not matches: continue
    teams=set()
    for m in matches:
        home=m.get("homeTeam",{}).get("name","")
        away=m.get("awayTeam",{}).get("name","")
        if home: teams.add(home)
        if away: teams.add(away)
    team_stats={}
    for team in teams:
        team_stats[team]=get_team_stats(team, matches)
    correct=0
    total=0
    for m in matches:
        home_name=m.get("homeTeam",{}).get("name","")
        away_name=m.get("awayTeam",{}).get("name","")
        if not home_name or not away_name: continue
        home_raw=team_stats.get(home_name,{})
        away_raw=team_stats.get(away_name,{})
        home_mapped=dm(home_raw)
        away_mapped=dm(away_raw)
        home_scored=quant.score_sports(home_mapped)
        away_scored=quant.score_sports(away_mapped)
        home_final={"name":home_name,"strength":home_scored.get("strength",5),"energy":home_scored.get("energy",50),"morale":home_scored.get("morale",5)}
        away_final={"name":away_name,"strength":away_scored.get("strength",5),"energy":away_scored.get("energy",50),"morale":away_scored.get("morale",5)}
        result=st.analyze(home_final, away_final)
        score=m.get("score",{}).get("fullTime",{})
        hg=score.get("home",0) or 0
        ag=score.get("away",0) or 0
        if hg>ag: actual="home_win"
        elif ag>hg: actual="away_win"
        else: actual="draw"
        pred=result.get("pick","")
        if pred=="WAIT" or pred=="": correct_pred=actual=="draw"
        elif pred==home_name: correct_pred=actual=="home_win"
        elif pred==away_name: correct_pred=actual=="away_win"
        else: correct_pred=False
        if correct_pred: correct+=1
        total+=1
    acc=(correct/total*100) if total>0 else 0
    print(f"{LEAGUE_NAMES[league_key]}: {correct}/{total} = {acc:.1f}%")
    all_results.append({"league":LEAGUE_NAMES[league_key],"total":total,"correct":correct,"accuracy":acc})
    total_correct+=correct
    total_matches+=total

print(f"\n🏆 OVERALL: {total_correct}/{total_matches} = {total_correct/total_matches*100:.1f}%")
with open("direct_backtest_results.json","w") as f:
    json.dump(all_results,f,indent=2)
