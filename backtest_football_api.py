"""
Sports Backtesting System - football-data.org API
"""

import json
import os
import time
import requests
from datetime import datetime
from collections import defaultdict

from engine.sun_tzu_engine import SunTzuEngine
from engine.quant_engine import QuantEngine
from engine.data_mapper import map_sports as dm
from engine.self_learner import SelfLearner

# football-data.org league IDs
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

API_KEY = "3f866159549e4972825cecea5b405b5d"

class SportsBacktester:
    def __init__(self):
        self.api_url = "https://api.football-data.org/v4"
        self.engine = SunTzuEngine()
        self.quant = QuantEngine()
        self.learner = SelfLearner()
        self.results = []
        
    def fetch_matches(self, league_code, season):
        """Fetch matches for a league season"""
        url = f"{self.api_url}/competitions/{league_code}/matches"
        params = {"season": season, "status": "FINISHED"}
        headers = {"X-Auth-Token": API_KEY}
        
        try:
            print(f"  Fetching {season} matches...", end=" ")
            response = requests.get(url, headers=headers, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                matches = data.get("matches", [])
                print(f"Found {len(matches)}")
                return matches
            elif response.status_code == 429:
                print("Rate limited. Waiting 60 seconds...")
                time.sleep(60)
                return self.fetch_matches(league_code, season)
            else:
                print(f"Error: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def get_team_stats_from_matches(self, team_name, matches):
        """Calculate team stats from match history"""
        played = 0
        wins = 0
        draws = 0
        losses = 0
        goals_for = 0
        goals_against = 0
        recent_results = []
        
        for match in matches:
            home_team = match.get("homeTeam", {}).get("name", "")
            away_team = match.get("awayTeam", {}).get("name", "")
            score = match.get("score", {})
            fulltime = score.get("fullTime", {})
            home_goals = fulltime.get("home", 0) or 0
            away_goals = fulltime.get("away", 0) or 0
            
            if home_team == team_name:
                played += 1
                goals_for += home_goals
                goals_against += away_goals
                if home_goals > away_goals:
                    wins += 1
                    recent_results.append("W")
                elif home_goals < away_goals:
                    losses += 1
                    recent_results.append("L")
                else:
                    draws += 1
                    recent_results.append("D")
            elif away_team == team_name:
                played += 1
                goals_for += away_goals
                goals_against += home_goals
                if away_goals > home_goals:
                    wins += 1
                    recent_results.append("W")
                elif away_goals < home_goals:
                    losses += 1
                    recent_results.append("L")
                else:
                    draws += 1
                    recent_results.append("D")
        
        form = "".join(recent_results[-5:]) if recent_results else ""
        
        return {
            "name": team_name,
            "played": played,
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "goals_for": goals_for,
            "goals_against": goals_against,
            "form": form
        }
    
    def get_actual_outcome(self, match):
        score = match.get("score", {})
        fulltime = score.get("fullTime", {})
        home_goals = fulltime.get("home", 0) or 0
        away_goals = fulltime.get("away", 0) or 0
        
        if home_goals > away_goals:
            return "home_win"
        elif away_goals > home_goals:
            return "away_win"
        else:
            return "draw"
    
    def backtest_season(self, league_key, season):
        """Run backtest for a league season"""
        league_code = LEAGUE_IDS[league_key]
        league_name = LEAGUE_NAMES[league_key]
        
        print(f"\n{'='*50}")
        print(f"📊 {league_name} {season}")
        print(f"{'='*50}")
        
        matches = self.fetch_matches(league_code, season)
        
        if not matches:
            print(f"  No matches found")
            return None
        
        # Get all unique teams
        teams = set()
        for match in matches:
            home = match.get("homeTeam", {}).get("name", "")
            away = match.get("awayTeam", {}).get("name", "")
            if home:
                teams.add(home)
            if away:
                teams.add(away)
        
        print(f"  {len(teams)} teams, {len(matches)} matches")
        
        # Calculate stats for each team
        team_stats = {}
        for team in teams:
            team_stats[team] = self.get_team_stats_from_matches(team, matches)
        
        correct_count = 0
        total_count = 0
        
        # Process each match
        for idx, match in enumerate(matches):
            home_name = match.get("homeTeam", {}).get("name", "")
            away_name = match.get("awayTeam", {}).get("name", "")
            
            if not home_name or not away_name:
                continue
            
            # Get team data
            home_data = team_stats.get(home_name, {"name": home_name})
            away_data = team_stats.get(away_name, {"name": away_name})
            
            # Map and score
            home_mapped = dm(home_data)
            away_mapped = dm(away_data)
            
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
            actual = self.get_actual_outcome(match)
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
            
            # Learn from outcome
            if predicted_action != "WAIT":
                price_change = 1.0 if correct else -1.0
                self.learner.learn_from_outcome(result.get("prediction_id"), price_change)
        
        accuracy = (correct_count / total_count * 100) if total_count > 0 else 0
        print(f"  ✅ {correct_count}/{total_count} = {accuracy:.1f}%")
        
        return {
            "league": league_name,
            "season": season,
            "total": total_count,
            "correct": correct_count,
            "accuracy": accuracy
        }
    
    def run_all(self):
        """Run backtest for all leagues and seasons"""
        seasons = ["2023", "2024", "2025"]
        leagues = ["epl", "laliga", "bundesliga", "seriea", "ligue1"]
        
        all_results = []
        
        for league in leagues:
            for season in seasons:
                result = self.backtest_season(league, season)
                if result:
                    all_results.append(result)
                    self.save_results(all_results)
                    self.print_summary(all_results)
                    time.sleep(2)  # Small delay between calls
        
        return all_results
    
    def save_results(self, results):
        with open("backtest_results.json", "w") as f:
            json.dump(results, f, indent=2)
    
    def print_summary(self, results):
        print("\n" + "=" * 60)
        print("📊 SUMMARY")
        print("=" * 60)
        
        total_correct = 0
        total_matches = 0
        league_stats = defaultdict(lambda: {"total": 0, "correct": 0})
        
        for result in results:
            league = result.get("league")
            league_stats[league]["total"] += result.get("total", 0)
            league_stats[league]["correct"] += result.get("correct", 0)
            total_correct += result.get("correct", 0)
            total_matches += result.get("total", 0)
        
        for league, stats in league_stats.items():
            acc = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
            print(f"  {league}: {stats['correct']}/{stats['total']} = {acc:.1f}%")
        
        overall_acc = (total_correct / total_matches * 100) if total_matches > 0 else 0
        print("=" * 60)
        print(f"🏆 OVERALL: {total_correct}/{total_matches} = {overall_acc:.1f}%")
        print("=" * 60)

def main():
    print("=" * 60)
    print("🔶 SHADOW BACKTESTER")
    print("   football-data.org API")
    print("=" * 60)
    
    backtester = SportsBacktester()
    results = backtester.run_all()
    backtester.print_summary(results)
    
    print("\n✅ Backtest complete!")

if __name__ == "__main__":
    main()
