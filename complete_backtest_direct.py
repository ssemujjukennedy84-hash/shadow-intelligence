"""
COMPLETE ENGINE BACKTEST - DIRECT (No import issues)
"""

import json
import os
import time
import requests
import yfinance as yf
from datetime import datetime
from collections import defaultdict
from dotenv import load_dotenv

from engine.sun_tzu_engine import SunTzuEngine
from engine.quant_engine import QuantEngine
from engine.data_mapper import map_sports as dm

# Load environment variables
load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
API_FOOTBALL_KEY = os.getenv("FOOTBALL_KEY", "")

LEAGUE_NAMES = {"epl":"Premier League","laliga":"La Liga","bundesliga":"Bundesliga","seriea":"Serie A","ligue1":"Ligue 1"}

# Simple CompleteEngine class (copied from your file)
TEAM_CITIES = {
    "france":(48.85,2.35),"senegal":(14.69,-17.44),"brazil":(-23.55,-46.63),
    "england":(51.50,-0.12),"germany":(52.52,13.40),"spain":(40.41,-3.70),
    "italy":(41.90,12.49),"netherlands":(52.37,4.89),"portugal":(38.71,-9.13),
    "man city":(53.48,-2.24),"arsenal":(51.55,-0.10),"liverpool":(53.43,-2.96),
    "man united":(53.46,-2.29),"chelsea":(51.48,-0.19),"tottenham":(51.60,-0.06),
    "real madrid":(40.45,-3.68),"barcelona":(41.38,2.15),"bayern":(48.21,11.62),
    "inter":(45.47,9.19),"ac milan":(45.47,9.19),"psg":(48.84,2.25),
}

class SimpleCompleteEngine:
    def __init__(self):
        self.year = datetime.now().year
    
    def get_all(self, name, domain):
        data = {"name": name}
        data.update(self._team_stats(name))
        data.update(self._weather(name))
        return data
    
    def _team_stats(self, name):
        try:
            headers = {"x-apisports-key": API_FOOTBALL_KEY}
            r = requests.get(f"https://v3.football.api-sports.io/teams?search={name}", headers=headers, timeout=5)
            if r.status_code == 200 and r.json().get("response"):
                team = r.json()["response"][0]["team"]
                tid = team["id"]
                result = {"team_id": tid}
                r2 = requests.get(f"https://v3.football.api-sports.io/teams/statistics?team={tid}&season={self.year}", headers=headers, timeout=5)
                if r2.status_code == 200:
                    stats = r2.json().get("response",{})
                    if isinstance(stats, list): stats = stats[0] if stats else {}
                    fixtures = stats.get("fixtures",{})
                    goals = stats.get("goals",{})
                    gf = goals.get("for",{}).get("total",{}).get("total",0)
                    if isinstance(gf, dict): gf = 0
                    ga = goals.get("against",{}).get("total",{}).get("total",0)
                    if isinstance(ga, dict): ga = 0
                    result.update({
                        "form": stats.get("form",""),
                        "played": fixtures.get("played",{}).get("total",0),
                        "wins": fixtures.get("wins",{}).get("total",0),
                        "draws": fixtures.get("draws",{}).get("total",0),
                        "losses": fixtures.get("loses",{}).get("total",0),
                        "goals_for": gf,
                        "goals_against": ga,
                    })
                return result
        except: pass
        return {}
    
    def _weather(self, name):
        key = name.lower().strip()
        coords = TEAM_CITIES.get(key)
        if not coords:
            for k in TEAM_CITIES:
                if k in key or key in k: coords = TEAM_CITIES[k]; break
        if coords:
            try:
                r = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={coords[0]}&longitude={coords[1]}&current_weather=true", timeout=5)
                if r.status_code == 200:
                    w = r.json()["current_weather"]
                    codes = {0:"Clear",1:"Clear",2:"Cloudy",3:"Overcast",45:"Fog",51:"Drizzle",61:"Rain",71:"Snow",95:"Storm"}
                    return {"weather": codes.get(w["weathercode"],"Unknown"),"temperature": w["temperature"],"wind_speed": w["windspeed"]}
            except: pass
        return {"weather": "Unknown"}
    
    def get_h2h(self, team1, team2):
        try:
            headers = {"x-apisports-key": API_FOOTBALL_KEY}
            r1 = requests.get(f"https://v3.football.api-sports.io/teams?search={team1}", headers=headers, timeout=5)
            r2 = requests.get(f"https://v3.football.api-sports.io/teams?search={team2}", headers=headers, timeout=5)
            if r1.status_code==200 and r2.status_code==200:
                t1 = r1.json().get("response",[])
                t2 = r2.json().get("response",[])
                if t1 and t2:
                    id1, id2 = t1[0]["team"]["id"], t2[0]["team"]["id"]
                    r = requests.get(f"https://v3.football.api-sports.io/fixtures/headtohead?h2h={id1}-{id2}&last=5", headers=headers, timeout=5)
                    if r.status_code == 200:
                        matches = r.json().get("response",[])
                        t1w = sum(1 for m in matches if (m["teams"]["home"]["id"]==id1 and m["teams"]["home"]["winner"]) or (m["teams"]["away"]["id"]==id1 and m["teams"]["away"]["winner"]))
                        t2w = sum(1 for m in matches if (m["teams"]["home"]["id"]==id2 and m["teams"]["home"]["winner"]) or (m["teams"]["away"]["id"]==id2 and m["teams"]["away"]["winner"]))
                        return {"matches_played":len(matches),"team1_wins":t1w,"team2_wins":t2w,"draws":len(matches)-t1w-t2w}
        except: pass
        return {}

class CompleteBacktest:
    def __init__(self):
        self.sun_tzu = SunTzuEngine()
        self.quant = QuantEngine()
        self.engine = SimpleCompleteEngine()
        self.results = []
        self.total_correct = 0
        self.total_matches = 0
        
    def load_matches(self, league_key):
        with open(f"data/offline_matches/{league_key}.json","r") as f:
            data = json.load(f)
        return data.get("matches", [])
    
    def backtest_league(self, league_key):
        league_name = LEAGUE_NAMES[league_key]
        matches = self.load_matches(league_key)
        
        if not matches:
            print(f"  No matches for {league_name}")
            return None
        
        print(f"\n📊 {league_name} - {len(matches)} matches")
        print("-" * 40)
        
        correct = 0
        total = 0
        
        for idx, match in enumerate(matches):
            home_name = match.get("homeTeam", {}).get("name", "")
            away_name = match.get("awayTeam", {}).get("name", "")
            
            if not home_name or not away_name:
                continue
            
            try:
                home_data = self.engine.get_all(home_name, "sports")
                away_data = self.engine.get_all(away_name, "sports")
                h2h = self.engine.get_h2h(home_name, away_name)
            except:
                continue
            
            home_mapped = dm(home_data)
            away_mapped = dm(away_data)
            
            home_scored = self.quant.score_sports(home_mapped)
            away_scored = self.quant.score_sports(away_mapped)
            
            if h2h and h2h.get("matches_played", 0) > 0:
                h2h_adv = (h2h.get("team1_wins", 0) - h2h.get("team2_wins", 0)) / max(1, h2h.get("matches_played", 1))
                home_scored["strength"] = home_scored.get("strength", 5) + h2h_adv * 2
                away_scored["strength"] = away_scored.get("strength", 5) - h2h_adv * 2
            
            home_final = {"name": home_name, "strength": home_scored.get("strength", 5), "energy": home_scored.get("energy", 50), "morale": home_scored.get("morale", 5)}
            away_final = {"name": away_name, "strength": away_scored.get("strength", 5), "energy": away_scored.get("energy", 50), "morale": away_scored.get("morale", 5)}
            
            try:
                result = self.sun_tzu.analyze(home_final, away_final)
            except:
                continue
            
            score = match.get("score", {}).get("fullTime", {})
            hg = score.get("home", 0) or 0
            ag = score.get("away", 0) or 0
            
            if hg > ag: actual = "home_win"
            elif ag > hg: actual = "away_win"
            else: actual = "draw"
            
            pred = result.get("pick", "")
            if pred == "WAIT" or pred == "":
                correct_pred = actual == "draw"
            elif pred == home_name:
                correct_pred = actual == "home_win"
            elif pred == away_name:
                correct_pred = actual == "away_win"
            else:
                correct_pred = False
            
            if correct_pred:
                correct += 1
            total += 1
            
            if (idx + 1) % 50 == 0:
                print(f"  Processed {idx + 1}/{len(matches)}...")
        
        acc = (correct / total * 100) if total > 0 else 0
        print(f"  ✅ {correct}/{total} = {acc:.1f}%")
        
        self.total_correct += correct
        self.total_matches += total
        
        return {"league": league_name, "total": total, "correct": correct, "accuracy": acc}
    
    def run_all(self):
        print("=" * 60)
        print("🔶 COMPLETE ENGINE BACKTEST")
        print("   Weather · H2H · Team Stats")
        print("=" * 60)
        
        for league in ["epl", "laliga", "bundesliga", "seriea", "ligue1"]:
            result = self.backtest_league(league)
            if result:
                self.results.append(result)
        
        self.print_summary()
    
    def print_summary(self):
        print("\n" + "=" * 60)
        print("📊 COMPLETE ENGINE - FINAL SUMMARY")
        print("=" * 60)
        
        for r in self.results:
            acc = r.get("accuracy", 0)
            print(f"  {r['league']}: {r['correct']}/{r['total']} = {acc:.1f}%")
        
        overall = (self.total_correct / self.total_matches * 100) if self.total_matches > 0 else 0
        print("\n" + "=" * 60)
        print(f"🏆 OVERALL: {self.total_correct}/{self.total_matches} = {overall:.1f}%")
        print("=" * 60)

def main():
    tester = CompleteBacktest()
    tester.run_all()

if __name__ == "__main__":
    main()
