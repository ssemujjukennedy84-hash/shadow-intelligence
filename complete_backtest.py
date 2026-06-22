"""
COMPLETE ENGINE BACKTEST - Uses weather, injuries, manager, H2H
"""

import json
import os
import time
from collections import defaultdict

from engine.sun_tzu_engine import SunTzuEngine
from engine.quant_engine import QuantEngine
from engine.data_mapper import map_sports as dm
from complete_engine import CompleteEngine  # YOUR original engine!

LEAGUE_NAMES = {"epl":"Premier League","laliga":"La Liga","bundesliga":"Bundesliga","seriea":"Serie A","ligue1":"Ligue 1"}

class CompleteBacktest:
    def __init__(self):
        self.sun_tzu = SunTzuEngine()
        self.quant = QuantEngine()
        self.engine = CompleteEngine()
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
            
            # GET COMPLETE DATA - Includes weather, injuries, manager!
            try:
                home_data = self.engine.get_all(home_name, "sports")
                away_data = self.engine.get_all(away_name, "sports")
                h2h = self.engine.get_h2h(home_name, away_name)
            except:
                continue
            
            # MAP TO SUN TZU CONCEPTS
            home_mapped = dm(home_data)
            away_mapped = dm(away_data)
            
            # QUANT SCORING
            home_scored = self.quant.score_sports(home_mapped)
            away_scored = self.quant.score_sports(away_mapped)
            
            # ADD H2H ADVANTAGE
            if h2h:
                h2h_adv = (h2h.get("team1_wins", 0) - h2h.get("team2_wins", 0)) / max(1, h2h.get("matches_played", 1))
                home_scored["strength"] = home_scored.get("strength", 5) + h2h_adv * 2
                away_scored["strength"] = away_scored.get("strength", 5) - h2h_adv * 2
            
            home_final = {
                "name": home_name,
                "strength": home_scored.get("strength", 5),
                "energy": home_scored.get("energy", 50),
                "morale": home_scored.get("morale", 5)
            }
            away_final = {
                "name": away_name,
                "strength": away_scored.get("strength", 5),
                "energy": away_scored.get("energy", 50),
                "morale": away_scored.get("morale", 5)
            }
            
            # SUN TZU ANALYSIS
            try:
                result = self.sun_tzu.analyze(home_final, away_final)
            except:
                continue
            
            # GET ACTUAL RESULT
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
            
            # PROGRESS
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
        print("   Weather · Injuries · Manager · H2H · News")
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
        
        with open("complete_backtest_results.json", "w") as f:
            json.dump(self.results, f, indent=2)

def main():
    tester = CompleteBacktest()
    tester.run_all()

if __name__ == "__main__":
    main()
