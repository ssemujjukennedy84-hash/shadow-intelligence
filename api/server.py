"""
Shadow - Unified API v2
Trading | Leagues (with selector) | World Cup (manual)
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sys, os, importlib.util, json, requests as req
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(BASE, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

ct = load_module("combined_trading", "engine/combined_trading.py")
ste = load_module("sun_tzu_engine", "engine/sun_tzu_engine.py")
qe = load_module("quant_engine", "engine/quant_engine.py")
dm = load_module("data_mapper", "engine/data_mapper.py")

CombinedTrading = ct.CombinedTrading
SunTzuEngine = ste.SunTzuEngine
QuantEngine = qe.QuantEngine

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

LEAGUE_IDS = {"epl":39,"laliga":140,"bundesliga":78,"seriea":135,"ligue1":61}

@app.get("/")
def root():
    return {"name":"Shadow - Unified v2","domains":["trading","leagues","worldcup"],"status":"active"}

@app.post("/analyze/trading")
async def analyze_trading(request: Request):
    try:
        r = await request.json()
        engine = CombinedTrading(r.get("symbol","BTC-USD"))
        return engine.analyze()
    except Exception as e:
        return {"action":"WAIT","error":str(e)}

@app.post("/analyze/leagues")
async def analyze_leagues(request: Request):
    try:
        r = await request.json()
        e1_name = r.get("entity_1",""); e2_name = r.get("entity_2","")
        league = r.get("league","epl")
        league_id = LEAGUE_IDS.get(league, 39)
        
        raw1 = r.get("home_stats",{}) or {}; raw1["name"] = e1_name
        raw2 = r.get("away_stats",{}) or {}; raw2["name"] = e2_name
        
        data_found = False
        
        try:
            headers = {"x-apisports-key": "dd28cc88d9d6aa5d195a88d04b9c401c"}
            for name, raw in [(e1_name, raw1), (e2_name, raw2)]:
                resp = req.get(f"https://v3.football.api-sports.io/teams?search={name}", headers=headers, timeout=8)
                if resp.status_code == 200 and resp.json().get("response"):
                    team = resp.json()["response"][0]["team"]
                    tid = team["id"]
                    raw["team_id"] = tid; raw["venue"] = team.get("venue_name","")
                    raw["capacity"] = team.get("venue_capacity",0)
                    stats_resp = req.get(f"https://v3.football.api-sports.io/teams/statistics?team={tid}&season=2026&league={league_id}", headers=headers, timeout=8)
                    if stats_resp.status_code == 200:
                        stats = stats_resp.json().get("response",{})
                        if isinstance(stats, list): stats = stats[0] if stats else {}
                        fixtures = stats.get("fixtures",{})
                        played = fixtures.get("played",{}).get("total",0)
                        if played > 0:
                            data_found = True
                            goals = stats.get("goals",{})
                            raw.update({
                                "form":stats.get("form",""),"played":played,
                                "wins":fixtures.get("wins",{}).get("total",0),
                                "draws":fixtures.get("draws",{}).get("total",0),
                                "losses":fixtures.get("loses",{}).get("total",0),
                                "goals_for":goals.get("for",{}).get("total",{}).get("total",0) if isinstance(goals.get("for",{}).get("total",{}),dict) else 0,
                                "goals_against":goals.get("against",{}).get("total",{}).get("total",0) if isinstance(goals.get("against",{}).get("total",{}),dict) else 0,
                                "clean_sheets":fixtures.get("clean_sheet",{}).get("total",0),
                            })
        except: pass
        
        if not data_found:
            return {
                "pick":"NO DATA","pro_count":0,"con_count":0,"neutral_count":13,
                "battle_plan":f"Off-season. No live {league.upper()} data. Season starts August 2026.",
                "chapter_breakdown":[],"data_source":"OFF-SEASON",
                "quant":{"e1":{"strength":0,"energy":0,"morale":0},"e2":{"strength":0,"energy":0,"morale":0}},
                "execution":{"markets":["N/A"],"confidence":"NONE","hedge":"Wait for season"}
            }
        
        raw1 = dm.map_sports(raw1); raw2 = dm.map_sports(raw2)
        quant = QuantEngine()
        q1 = quant.score_sports(raw1); q2 = quant.score_sports(raw2)
        e1 = {**raw1,"strength":q1.get("strength",5),"energy":q1.get("energy",50),"morale":q1.get("morale",5)}
        e2 = {**raw2,"strength":q2.get("strength",5),"energy":q2.get("energy",50),"morale":q2.get("morale",5)}
        
        engine = SunTzuEngine()
        result = engine.analyze(e1, e2)
        result["quant"] = {"e1":q1,"e2":q2}
        result["data_source"] = f"LIVE ({league.upper()})"
        
        margin = abs(e1.get("strength",5)-e2.get("strength",5))
        if margin>3: markets,conf=["Match Winner","Handicap -1.5","Over 2.5 Goals"],"HIGH"
        elif margin>1.5: markets,conf=["Match Winner","Double Chance","Under 3.5 Goals"],"MEDIUM"
        else: markets,conf=["Draw No Bet","Under 2.5 Goals","BTTS NO"],"LOW"
        result["execution"] = {"markets":markets,"confidence":conf,"hedge":"Hedge on draw" if margin<2 else "No hedge needed"}
        return result
    except Exception as e:
        return {"error":str(e)}

@app.post("/analyze/worldcup")
async def analyze_worldcup(request: Request):
    try:
        r = await request.json()
        e1_name = r.get("entity_1",""); e2_name = r.get("entity_2","")
        raw1 = r.get("home_stats",{}) or {}; raw1["name"] = e1_name
        raw2 = r.get("away_stats",{}) or {}; raw2["name"] = e2_name
        
        raw1 = dm.map_sports(raw1); raw2 = dm.map_sports(raw2)
        quant = QuantEngine()
        q1 = quant.score_sports(raw1); q2 = quant.score_sports(raw2)
        e1 = {**raw1,"strength":q1.get("strength",5),"energy":q1.get("energy",50),"morale":q1.get("morale",5)}
        e2 = {**raw2,"strength":q2.get("strength",5),"energy":q2.get("energy",50),"morale":q2.get("morale",5)}
        
        engine = SunTzuEngine()
        result = engine.analyze(e1, e2)
        result["quant"] = {"e1":q1,"e2":q2}
        result["data_source"] = "MANUAL"
        
        margin = abs(e1.get("strength",5)-e2.get("strength",5))
        if margin>3: markets,conf=["Match Winner","Handicap -1.5","Over 2.5 Goals"],"HIGH"
        elif margin>1.5: markets,conf=["Match Winner","Double Chance","Under 3.5 Goals"],"MEDIUM"
        else: markets,conf=["Draw No Bet","Under 2.5 Goals","BTTS NO"],"LOW"
        result["execution"] = {"markets":markets,"confidence":conf,"hedge":"Hedge on draw" if margin<2 else "No hedge needed"}
        return result
    except Exception as e:
        return {"error":str(e)}

if __name__ == "__main__":
    import uvicorn
    print("SHADOW - UNIFIED v2")
    uvicorn.run(app, host="0.0.0.0", port=8000)