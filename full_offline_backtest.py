"""
FULL OFFLINE BACKTEST - ALL LEAGUES ALL SEASONS
Uses your local data files - NO API calls!
"""

import json
import os
import time
from collections import defaultdict

from engine.sun_tzu_engine import SunTzuEngine
from engine.quant_engine import QuantEngine
from engine.data_mapper import map_sports as dm
from engine.self_learner import SelfLearner

LEAGUE_NAMES = {
    "epl": "Premier League",
    "laliga": "La Liga",
    "bundesliga": "Bundesliga",
    "seriea": "Serie A",
    "ligue1": "Ligue 1"
}

class FullOfflineBacktester:
    def __init__(self):
        self.sun_tzu = SunTzuEngine()
        self.quant = QuantEngine()
        self.learner = SelfLearner()
        self.total_matches = 0
        self.total_correct = 0
        self.all_results = []
        
    def load_matches(self, league_key):
        """Load matches from offline JSON file"""
        file_path = f"data/offline_matches/{league_key}.json"
        if not os.path.exists(file_path):
            print(f"  No file: {file_path}")
            return []
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Handle different formats
            if isinstance(data, dict) and "matches" in data:
                return data["matches"]
            elif isinstance(data, list):
                return data
            else:
                return []
        except Exception as e:
            print(f"  Error loading: {e}")
            return []
    
    def get_team_stats(self, team_name, matches):
        """Calculate team stats from match history"""
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
    
    def get_season_from_match(self, match):
        """Extract season from match data"""
        # Try different fields
        if "season" in match:
            if isinstance(match["season"], dict):
                return match["season"].get("id", "unknown")
            return str(match["season"])
        elif "season_id" in match:
            return str(match["season_id"])
        elif "year" in match:
            return str(match["year"])
        return "unknown"
    
    def backtest_league(self, league_key):
        """Run backtest for a league using offline data"""
        league_name = LEAGUE_NAMES[league_key]
        
        print(f"\n{'='*50}")
        print(f"📊 {league_name} (OFFLINE)")
        print(f"{'='*50}")
        
        matches = self.load_matches(league_key)
        if not matches:
            print(f"  No matches found")
            return []
        
        print(f"  Found {len(matches)} matches")
        
        # Group matches by season
        seasons = {}
        for m in matches:
            season = self.get_season_from_match(m)
            if season not in seasons:
                seasons[season] = []
            seasons[season].append(m)
        
        print(f"  Seasons: {sorted(seasons.keys())}")
        
        league_results = []
        
        for season, season_matches in sorted(seasons.items()):
            print(f"\n  📅 Season {season}: {len(season_matches)} matches")
            
            # Get all teams
            teams = set()
            for m in season_matches:
                home = m.get("homeTeam", {}).get("name", "")
                away = m.get("awayTeam", {}).get("name", "")
                if home: teams.add(home)
                if away: teams.add(away)
            
            # Calculate team stats
            team_stats = {}
            for team in teams:
                team_stats[team] = self.get_team_stats(team, season_matches)
            
            season_correct = 0
            season_total = 0
            
            for idx, match in enumerate(season_matches):
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
                
                score = match.get("score", {}).get("fullTime", {})
                hg = score.get("home", 0) or 0
                ag = score.get("away", 0) or 0
                
                if hg > ag: actual = "home_win"
                elif ag > hg: actual = "away_win"
                else: actual = "draw"
                
                pred = result.get("pick", "")
                if pred == "WAIT" or pred == "":
                    correct = actual == "draw"
                elif pred == home_name:
                    correct = actual == "home_win"
                elif pred == away_name:
                    correct = actual == "away_win"
                else:
                    correct = False
                
                if correct:
                    season_correct += 1
                season_total += 1
                
                # Update weights in SQLite
                chapter_scores = {}
                for ch in result.get("chapter_breakdown", []):
                    ch_num = ch.get("chapter", 0)
                    verdict = ch.get("verdict", "NEUTRAL")
                    if correct:
                        chapter_scores[ch_num] = (verdict == "PRO")
                    else:
                        chapter_scores[ch_num] = (verdict == "CON")
                
                if chapter_scores:
                    pred_id = result.get("prediction_id", f"offline_{season}_{idx}")
                    try:
                        self.quant.record_outcome(pred_id, correct, "sports", league_key, chapter_scores)
                    except:
                        pass
                
                if (idx + 1) % 100 == 0:
                    print(f"    Processed {idx + 1}/{len(season_matches)}...")
            
            acc = (season_correct / season_total * 100) if season_total > 0 else 0
            print(f"    ✅ {season_correct}/{season_total} = {acc:.1f}%")
            
            self.total_correct += season_correct
            self.total_matches += season_total
            
            league_results.append({
                "league": league_name,
                "season": season,
                "total": season_total,
                "correct": season_correct,
                "accuracy": acc
            })
        
        return league_results
    
    def run_all(self):
        """Run backtest for all leagues"""
        leagues = ["epl", "laliga", "bundesliga", "seriea", "ligue1"]
        
        for league in leagues:
            results = self.backtest_league(league)
            self.all_results.extend(results)
            self.print_summary()
            print(f"\n⏳ Moving to next league...\n")
            time.sleep(1)
        
        return self.all_results
    
    def print_summary(self):
        print("\n" + "=" * 60)
        print("📊 OVERALL SUMMARY")
        print("=" * 60)
        
        league_stats = defaultdict(lambda: {"total": 0, "correct": 0})
        season_stats = defaultdict(lambda: {"total": 0, "correct": 0})
        
        for r in self.all_results:
            league = r.get("league")
            season = r.get("season")
            league_stats[league]["total"] += r.get("total", 0)
            league_stats[league]["correct"] += r.get("correct", 0)
            season_stats[season]["total"] += r.get("total", 0)
            season_stats[season]["correct"] += r.get("correct", 0)
        
        print("\n📈 Per League:")
        print("-" * 40)
        for league, stats in sorted(league_stats.items()):
            acc = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
            print(f"  {league}: {stats['correct']}/{stats['total']} = {acc:.1f}%")
        
        print("\n📈 Per Season:")
        print("-" * 40)
        for season in sorted(season_stats.keys()):
            stats = season_stats[season]
            acc = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
            print(f"  {season}: {stats['correct']}/{stats['total']} = {acc:.1f}%")
        
        overall = (self.total_correct / self.total_matches * 100) if self.total_matches > 0 else 0
        print("\n" + "=" * 60)
        print(f"🏆 OVERALL: {self.total_correct}/{self.total_matches} = {overall:.1f}%")
        print("=" * 60)
        
        # Save to file
        with open("offline_full_results.json", "w") as f:
            json.dump(self.all_results, f, indent=2)

def main():
    print("=" * 60)
    print("🔶 FULL OFFLINE BACKTEST")
    print("   ALL Leagues · ALL Seasons · NO API")
    print("=" * 60)
    
    tester = FullOfflineBacktester()
    tester.run_all()
    tester.print_summary()
    
    print("\n✅ Complete!")
    print("📁 Results saved to offline_full_results.json")
    print("📊 Weights updated in SQLite")

if __name__ == "__main__":
    main()
