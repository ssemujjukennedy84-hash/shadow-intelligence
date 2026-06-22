"""
Sports Backtesting System - Uses OFFLINE data from your project
"""

import json
import os
from datetime import datetime
from collections import defaultdict

from engine.sun_tzu_engine import SunTzuEngine
from engine.quant_engine import QuantEngine
from engine.data_mapper import map_sports as dm
from engine.self_learner import SelfLearner

class SportsBacktester:
    def __init__(self):
        self.engine = SunTzuEngine()
        self.quant = QuantEngine()
        self.learner = SelfLearner()
        self.results = []
        
    def load_offline_matches(self, league_key):
        """Load matches from offline JSON files"""
        file_path = f"data/offline_matches/{league_key}.json"
        if not os.path.exists(file_path):
            print(f"  No offline data for {league_key}")
            return []
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Handle different JSON formats
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            # Try to find matches in dict
            for key in ["matches", "fixtures", "response", "data"]:
                if key in data:
                    return data[key]
            return [data]
        return []
    
    def extract_team_data(self, match, league_key):
        """Extract team data from match dict"""
        # Try different formats
        home = None
        away = None
        
        # Format 1: teams.home / teams.away
        if "teams" in match:
            home = match["teams"].get("home", {}).get("name", "")
            away = match["teams"].get("away", {}).get("name", "")
        # Format 2: home / away directly
        elif "home" in match and "away" in match:
            if isinstance(match["home"], dict):
                home = match["home"].get("name", str(match["home"]))
            else:
                home = str(match["home"])
            if isinstance(match["away"], dict):
                away = match["away"].get("name", str(match["away"]))
            else:
                away = str(match["away"])
        # Format 3: team_home / team_away
        elif "team_home" in match:
            home = match.get("team_home", "")
            away = match.get("team_away", "")
        
        return home, away
    
    def get_match_outcome(self, match):
        """Get actual match outcome"""
        # Try different formats
        home_goals = 0
        away_goals = 0
        
        if "score" in match:
            score = match["score"]
            if "fulltime" in score:
                home_goals = score["fulltime"].get("home", 0) or 0
                away_goals = score["fulltime"].get("away", 0) or 0
            elif "halftime" in score:
                home_goals = score["halftime"].get("home", 0) or 0
                away_goals = score["halftime"].get("away", 0) or 0
        elif "goals" in match:
            if isinstance(match["goals"], dict):
                home_goals = match["goals"].get("home", 0) or 0
                away_goals = match["goals"].get("away", 0) or 0
        
        if home_goals > away_goals:
            return "home_win"
        elif away_goals > home_goals:
            return "away_win"
        return "draw"
    
    def backtest_league(self, league_key):
        """Run backtest for a league using offline data"""
        league_name = league_key.upper()
        print(f"\n📊 Testing {league_name}")
        print("-" * 50)
        
        matches = self.load_offline_matches(league_key)
        if not matches:
            print(f"  No matches found for {league_name}")
            return
        
        print(f"  Found {len(matches)} matches")
        
        correct_count = 0
        total_count = 0
        
        for idx, match in enumerate(matches):
            home_name, away_name = self.extract_team_data(match, league_key)
            
            if not home_name or not away_name:
                continue
            
            # Create simple team data
            home_data = {
                "name": home_name,
                "played": 20,
                "wins": 8,
                "draws": 6,
                "losses": 6,
                "goals_for": 30,
                "goals_against": 25,
                "form": "WDLWW"
            }
            away_data = {
                "name": away_name,
                "played": 20,
                "wins": 7,
                "draws": 7,
                "losses": 6,
                "goals_for": 28,
                "goals_against": 26,
                "form": "DLWWL"
            }
            
            # Map data
            home_mapped = dm(home_data)
            away_mapped = dm(away_data)
            
            # Score with quant
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
            
            # Run prediction
            try:
                result = self.engine.analyze(home_final, away_final)
            except Exception as e:
                continue
            
            # Get actual outcome
            actual = self.get_match_outcome(match)
            predicted_action = result.get("action", "")
            
            # Determine if correct
            if predicted_action == "WAIT":
                correct = actual == "draw"
            elif predicted_action == home_name:
                correct = actual == "home_win"
            elif predicted_action == away_name:
                correct = actual == "away_win"
            else:
                correct = False
            
            if correct:
                correct_count += 1
            total_count += 1
            
            # Learn
            if predicted_action != "WAIT":
                price_change = 1.0 if correct else -1.0
                self.learner.learn_from_outcome(result.get("prediction_id"), price_change)
            
            if idx % 100 == 0 and idx > 0:
                print(f"  Processed {idx} matches...")
        
        accuracy = (correct_count / total_count * 100) if total_count > 0 else 0
        print(f"\n  📈 {league_name}: {correct_count}/{total_count} correct = {accuracy:.1f}%")
        
        return {
            "league": league_name,
            "total": total_count,
            "correct": correct_count,
            "accuracy": accuracy
        }
    
    def run_all(self):
        """Run backtest for all leagues"""
        leagues = ["epl", "laliga", "bundesliga", "seriea", "ligue1"]
        all_results = []
        
        for league in leagues:
            result = self.backtest_league(league)
            if result:
                all_results.append(result)
                self.save_results(all_results)
                self.print_summary(all_results)
        
        return all_results
    
    def save_results(self, results):
        with open("backtest_results_offline.json", "w") as f:
            json.dump(results, f, indent=2)
    
    def print_summary(self, results):
        print("\n" + "=" * 60)
        print("📊 BACKTEST SUMMARY (OFFLINE DATA)")
        print("=" * 60)
        
        total_correct = 0
        total_matches = 0
        
        for result in results:
            league = result.get("league")
            total = result.get("total", 0)
            correct = result.get("correct", 0)
            acc = (correct / total * 100) if total > 0 else 0
            print(f"  {league}: {correct}/{total} = {acc:.1f}%")
            total_correct += correct
            total_matches += total
        
        overall_acc = (total_correct / total_matches * 100) if total_matches > 0 else 0
        print("\n" + "=" * 60)
        print(f"🏆 OVERALL: {total_correct}/{total_matches} correct = {overall_acc:.1f}%")
        print("=" * 60)

def main():
    print("=" * 60)
    print("🔶 SHADOW OFFLINE BACKTESTER")
    print("   Using local data files")
    print("=" * 60)
    
    backtester = SportsBacktester()
    results = backtester.run_all()
    backtester.print_summary(results)
    
    print("\n✅ Backtest complete!")

if __name__ == "__main__":
    main()
