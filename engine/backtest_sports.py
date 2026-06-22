"""
Sports Backtesting System - Learns from historical matches across multiple seasons
"""

import json
import os
import time
import requests
from datetime import datetime
from collections import defaultdict

# Import engines
from engine.sun_tzu_engine import SunTzuEngine
from engine.quant_engine import QuantEngine
from engine.data_mapper import map_sports as dm
from engine.self_learner import SelfLearner

LEAGUE_IDS = {
    "epl": 39,
    "laliga": 140,
    "bundesliga": 78,
    "seriea": 135,
    "ligue1": 61
}

LEAGUE_NAMES = {
    "epl": "Premier League",
    "laliga": "La Liga",
    "bundesliga": "Bundesliga",
    "seriea": "Serie A",
    "ligue1": "Ligue 1"
}

class SportsBacktester:
    def __init__(self):
        self.api_key = "dd28cc88d9d6aa5d195a88d04b9c401c"
        self.engine = SunTzuEngine()
        self.quant = QuantEngine()
        self.learner = SelfLearner()
        self.results = []
        self.stats = defaultdict(lambda: {"total": 0, "correct": 0, "accuracy": 0})
        
    def fetch_league_matches(self, league_id, season):
        """Fetch all matches for a league in a given season"""
        url = f"https://v3.football.api-sports.io/fixtures?league={league_id}&season={season}"
        headers = {"x-apisports-key": self.api_key}
        
        try:
            print(f"  Fetching {season} matches...")
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                return data.get("response", [])
            else:
                print(f"  Error: {response.status_code}")
                return []
        except Exception as e:
            print(f"  Error: {e}")
            return []
    
    def get_team_stats(self, team_id, league_id, season):
        """Get team statistics for a season"""
        url = f"https://v3.football.api-sports.io/teams/statistics?team={team_id}&league={league_id}&season={season}"
        headers = {"x-apisports-key": self.api_key}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                stats = response.json().get("response", {})
                if isinstance(stats, list):
                    stats = stats[0] if stats else {}
                return stats
            return {}
        except:
            return {}
    
    def map_team_data(self, team_name, team_id, league_id, season):
        """Build team data for prediction"""
        stats = self.get_team_stats(team_id, league_id, season)
        
        if not stats:
            return {"name": team_name, "strength": 5, "energy": 50, "morale": 5}
        
        fixtures = stats.get("fixtures", {})
        goals = stats.get("goals", {})
        
        played = fixtures.get("played", {}).get("total", 0)
        wins = fixtures.get("wins", {}).get("total", 0)
        draws = fixtures.get("draws", {}).get("total", 0)
        losses = fixtures.get("loses", {}).get("total", 0)
        
        goals_for = goals.get("for", {}).get("total", {}).get("total", 0)
        if isinstance(goals_for, dict):
            goals_for = goals_for.get("total", 0)
        
        goals_against = goals.get("against", {}).get("total", {}).get("total", 0)
        if isinstance(goals_against, dict):
            goals_against = goals_against.get("total", 0)
        
        form = stats.get("form", "")
        
        raw_data = {
            "name": team_name,
            "played": played,
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "goals_for": goals_for,
            "goals_against": goals_against,
            "form": form
        }
        
        # Map using data_mapper
        mapped = dm(raw_data)
        
        # Score with quant engine
        scored = self.quant.score_sports(mapped)
        
        return {
            "name": team_name,
            "strength": scored.get("strength", 5),
            "energy": scored.get("energy", 50),
            "morale": scored.get("morale", 5),
            "played": played,
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "goals_for": goals_for,
            "goals_against": goals_against,
            "form": form
        }
    
    def get_team_id(self, team_name, league_id):
        """Get team ID by name"""
        url = f"https://v3.football.api-sports.io/teams?search={team_name}&league={league_id}"
        headers = {"x-apisports-key": self.api_key}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                teams = response.json().get("response", [])
                if teams:
                    return teams[0]["team"]["id"]
            return None
        except:
            return None
    
    def get_actual_outcome(self, match):
        """Determine actual outcome of a match"""
        score = match.get("score", {})
        fulltime = score.get("fulltime", {})
        home_goals = fulltime.get("home", 0) or 0
        away_goals = fulltime.get("away", 0) or 0
        
        if home_goals > away_goals:
            return "home_win"
        elif away_goals > home_goals:
            return "away_win"
        else:
            return "draw"
    
    def determine_prediction_correct(self, prediction, actual):
        """Check if prediction was correct"""
        predicted_action = prediction.get("action", "")
        entity_1 = prediction.get("entity_1", "")
        entity_2 = prediction.get("entity_2", "")
        
        if predicted_action == "WAIT":
            return actual == "draw"
        elif predicted_action == entity_1:
            return actual == "home_win"
        elif predicted_action == entity_2:
            return actual == "away_win"
        
        return False
    
    def backtest_season(self, league_key, season):
        """Run backtest for a league season"""
        league_id = LEAGUE_IDS[league_key]
        league_name = LEAGUE_NAMES[league_key]
        
        print(f"\n📊 Testing {league_name} {season}")
        print("-" * 50)
        
        matches = self.fetch_league_matches(league_id, season)
        
        if not matches:
            print(f"  No matches found for {league_name} {season}")
            return
        
        season_results = []
        correct_count = 0
        total_count = 0
        
        # Get all unique team names from matches
        teams = {}
        for match in matches:
            home = match.get("teams", {}).get("home", {}).get("name", "")
            away = match.get("teams", {}).get("away", {}).get("name", "")
            if home:
                teams[home] = None
            if away:
                teams[away] = None
        
        # Get team IDs
        for team_name in teams.keys():
            team_id = self.get_team_id(team_name, league_id)
            if team_id:
                teams[team_name] = team_id
        
        # Process each match
        for idx, match in enumerate(matches):
            home_name = match.get("teams", {}).get("home", {}).get("name", "")
            away_name = match.get("teams", {}).get("away", {}).get("name", "")
            home_id = teams.get(home_name)
            away_id = teams.get(away_name)
            
            if not home_id or not away_id:
                continue
            
            # Get team data
            home_data = self.map_team_data(home_name, home_id, league_id, season)
            away_data = self.map_team_data(away_name, away_id, league_id, season)
            
            # Run prediction
            try:
                result = self.engine.analyze(home_data, away_data)
            except Exception as e:
                continue
            
            # Get actual outcome
            actual = self.get_actual_outcome(match)
            correct = self.determine_prediction_correct(result, actual)
            
            if correct:
                correct_count += 1
            total_count += 1
            
            # Record result
            match_result = {
                "league": league_name,
                "season": season,
                "home": home_name,
                "away": away_name,
                "prediction": result.get("action"),
                "confidence": result.get("confidence"),
                "actual": actual,
                "correct": correct,
                "prediction_id": result.get("prediction_id")
            }
            season_results.append(match_result)
            
            # Provide feedback to learner if prediction was not WAIT
            if result.get("action") != "WAIT":
                price_change = 1.0 if correct else -1.0
                self.learner.learn_from_outcome(result.get("prediction_id"), price_change)
            
            # Progress update
            if idx % 50 == 0 and idx > 0:
                print(f"  Processed {idx} matches...")
        
        # Season stats
        accuracy = (correct_count / total_count * 100) if total_count > 0 else 0
        print(f"\n  📈 {league_name} {season}: {correct_count}/{total_count} correct = {accuracy:.1f}%")
        
        return {
            "league": league_name,
            "season": season,
            "total": total_count,
            "correct": correct_count,
            "accuracy": accuracy,
            "results": season_results
        }
    
    def run_all_seasons(self):
        """Run backtest for all leagues and seasons"""
        seasons = ["2022", "2023", "2024", "2025"]
        leagues = ["epl", "laliga", "bundesliga", "seriea", "ligue1"]
        
        all_results = []
        
        for league in leagues:
            for season in seasons:
                result = self.backtest_season(league, season)
                if result:
                    all_results.append(result)
                    # Save progress
                    self.save_results(all_results)
                    self.print_summary(all_results)
        
        return all_results
    
    def save_results(self, results):
        """Save backtest results to file"""
        with open("backtest_results.json", "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to backtest_results.json")
    
    def print_summary(self, results):
        """Print overall summary"""
        print("\n" + "=" * 60)
        print("📊 OVERALL BACKTEST SUMMARY")
        print("=" * 60)
        
        total_correct = 0
        total_matches = 0
        
        league_stats = {}
        
        for result in results:
            league = result.get("league")
            season = result.get("season")
            
            if league not in league_stats:
                league_stats[league] = {"total": 0, "correct": 0}
            
            league_stats[league]["total"] += result.get("total", 0)
            league_stats[league]["correct"] += result.get("correct", 0)
            
            total_correct += result.get("correct", 0)
            total_matches += result.get("total", 0)
        
        # Print per league
        print("\n📈 Per League Performance:")
        print("-" * 40)
        for league, stats in league_stats.items():
            acc = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
            print(f"  {league}: {stats['correct']}/{stats['total']} = {acc:.1f}%")
        
        # Print overall
        overall_acc = (total_correct / total_matches * 100) if total_matches > 0 else 0
        print("\n" + "=" * 60)
        print(f"🏆 OVERALL: {total_correct}/{total_matches} correct = {overall_acc:.1f}%")
        print("=" * 60)
        
        # Show updated weights
        print("\n📊 Updated Chapter Weights:")
        weights = self.learner.get_weights()
        for chapter, weight in sorted(weights.items()):
            bar = "█" * int(weight * 5)
            print(f"  {chapter}: {weight:.2f} {bar}")
        
        # Save weights
        self.learner.save_weights()
        print("\n✅ Weights saved to weights.json")


def main():
    print("=" * 60)
    print("🔶 SHADOW SPORTS BACKTESTER")
    print("   Learning from 2022-2026 seasons")
    print("=" * 60)
    
    backtester = SportsBacktester()
    results = backtester.run_all_seasons()
    backtester.print_summary(results)
    
    print("\n✅ Backtest complete!")
    print(f"📁 Results saved to backtest_results.json")
    print(f"📊 Weights saved to weights.json")

if __name__ == "__main__":
    main()