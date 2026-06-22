"""
SIMPLE BACKTEST - FIXED for Original Engine
"""

import json
import os
import time
import requests
from collections import defaultdict

from engine.sun_tzu_engine import SunTzuEngine
from engine.quant_engine import QuantEngine
from engine.data_mapper import map_sports as dm

API_KEY = "3f866159549e4972825cecea5b405b5d"

LEAGUE_IDS = {
    "epl": "PL",
    "laliga": "PD",
    "bundesliga": "BL1",
    "seriea": "SA",
    "ligue1": "FL1"
}

LEAGUE_NAMES = {
    "epl": "Premier League",
    "laliga": "La Liga",
    "bundesliga": "Bundesliga",
    "seriea": "Serie A",
    "ligue1": "Ligue 1"
}

class SimpleBacktester:
    def __init__(self):
        self.api_url = "https://api.football-data.org/v4"
        self.sun_tzu = SunTzuEngine()
        self.quant = QuantEngine()
        
    def fetch_matches(self, league_code, season):
        url = f"{self.api_url}/competitions/{league_code}/matches"
        params = {"season": season, "status": "FINISHED"}
        headers = {"X-Auth-Token": API_KEY}
        
        try:
            print(f"  Fetching {season}...", end=" ")
            response = requests.get(url, headers=headers, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                matches = data.get("matches", [])
                print(f"found {len(matches)}")
                return matches
            elif response.status_code == 429:
                print("Rate limited, waiting...")
                time.sleep(60)
                return self.fetch_matches(league_code, season)
            else:
                print(f"Error: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def get_team_stats(self, team_name, matches):
        played = wins = draws = losses = gf = ga = 0
        recent = []
        
        for m in matches:
            home = m.get("homeTeam", {}).get("name", "")
            away = m.get("awayTeam", {}).get("name", "")
            score = m.get("score", {}).get("fullTime", {})
            hg = score.get("home", 0) or 0
            ag = score.get("away", 0) or 0
            
            if home == team_name:
                played += 1; gf += hg; ga += ag
                if hg > ag: wins += 1; recent.append("W")
                elif hg < ag: losses += 1; recent.append("L")
                else: draws += 1; recent.append("D")
            elif away == team_name:
                played += 1; gf += ag; ga += hg
                if ag > hg: wins += 1; recent.append("W")
                elif ag < hg: losses += 1; recent.append("L")
                else: draws += 1; recent.append("D")
        
        return {
            "name": team_name,
            "played": played,
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "goals_for": gf,
            "goals_against": ga,
            "form": "".join(recent[-5:])
        }
    
    def backtest_season(self, league_key, season):
        league_code = LEAGUE_IDS[league_key]
        league_name = LEAGUE_NAMES[league_key]
        
        print(f"\n{'='*50}")
        print(f"📊 {league_name} {season}")
        print(f"{'='*50}")
        
        matches = self.fetch_matches(league_code, season)
        if not matches:
            return None
        
        teams = set()
        for m in matches:
            home = m.get("homeTeam", {}).get("name", "")
            away = m.get("awayTeam", {}).get("name", "")
            if home: teams.add(home)
            if away: teams.add(away)
        
        print(f"  {len(teams)} teams")
        
        team_stats = {}
        for team in teams:
            team_stats[team] = self.get_team_stats(team, matches)
        
        season_correct = 0
        season_total = 0
        pick_counts = defaultdict(int)
        
        for idx, match in enumerate(matches):
            home_name = match.get("homeTeam", {}).get("name", "")
            away_name = match.get("awayTeam", {}).get("name", "")
            
            if not home_name or not away_name:
                continue
            
            home_raw = team_stats.get(home_name, {})
            away_raw = team_stats.get(away_name, {})
            
            home_mapped = dm(home_raw)
            away_mapped = dm(away_raw)
            
            home_scored = self.quant.score_sports(home_mapped)
            away_scored = self.quant.score_sports(away_mapped)
            
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
            
            try:
                result = self.sun_tzu.analyze(home_final, away_final)
            except Exception as e:
                continue
            
            # Get actual outcome
            score = match.get("score", {}).get("fullTime", {})
            hg = score.get("home", 0) or 0
            ag = score.get("away", 0) or 0
            
            if hg > ag: actual = "home_win"
            elif ag > hg: actual = "away_win"
            else: actual = "draw"
            
            # Prediction from engine - uses 'pick'
            pred = result.get("pick", "")
            pick_counts[pred] += 1
            
            # Determine if correct
            if pred == "WAIT" or pred == "":
                correct = actual == "draw"
            elif pred == home_name:
                correct = actual == "home_win"
            elif pred == away_name:
                correct = actual == "away_win"
            else:
                # If pick is something else (like a player or generic), compare to actual
                correct = False
            
            if correct:
                season_correct += 1
            season_total += 1
            
            if (idx + 1) % 50 == 0:
                print(f"  Processed {idx + 1}/{len(matches)}...")
        
        acc = (season_correct / season_total * 100) if season_total > 0 else 0
        print(f"  ✅ {season_correct}/{season_total} = {acc:.1f}%")
        print(f"  Picks: {dict(pick_counts)}")
        
        return {
            "league": league_name,
            "season": season,
            "total": season_total,
            "correct": season_correct,
            "accuracy": acc,
            "picks": dict(pick_counts)
        }
    
    def run_all(self):
        seasons = ["2023", "2024", "2025"]
        leagues = ["epl", "laliga", "bundesliga", "seriea", "ligue1"]
        all_results = []
        
        for league in leagues:
            for season in seasons:
                result = self.backtest_season(league, season)
                if result:
                    all_results.append(result)
                    self.print_summary(all_results)
                    time.sleep(2)
        
        return all_results
    
    def print_summary(self, results):
        print("\n" + "=" * 60)
        print("📊 BACKTEST SUMMARY")
        print("=" * 60)
        
        league_stats = defaultdict(lambda: {"total": 0, "correct": 0})
        total_correct = 0
        total_matches = 0
        
        for r in results:
            league = r.get("league")
            league_stats[league]["total"] += r.get("total", 0)
            league_stats[league]["correct"] += r.get("correct", 0)
            total_correct += r.get("correct", 0)
            total_matches += r.get("total", 0)
        
        for league, stats in league_stats.items():
            acc = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
            print(f"  {league}: {stats['correct']}/{stats['total']} = {acc:.1f}%")
        
        overall = (total_correct / total_matches * 100) if total_matches > 0 else 0
        print("=" * 60)
        print(f"🏆 OVERALL: {total_correct}/{total_matches} = {overall:.1f}%")
        print("=" * 60)

def main():
    print("=" * 60)
    print("🔶 BACKTEST - ORIGINAL ENGINE")
    print("=" * 60)
    
    tester = SimpleBacktester()
    results = tester.run_all()
    tester.print_summary(results)
    print("\n✅ Complete!")

if __name__ == "__main__":
    main()
