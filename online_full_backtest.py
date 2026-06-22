"""
FULL ONLINE BACKTEST - WITH DELAYS
All leagues · All seasons · API with rate limit handling
"""

import json
import os
import time
import requests
from collections import defaultdict

from engine.sun_tzu_engine import SunTzuEngine
from engine.quant_engine import QuantEngine
from engine.data_mapper import map_sports as dm
from engine.self_learner import SelfLearner

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

class FullOnlineBacktester:
    def __init__(self):
        self.api_url = "https://api.football-data.org/v4"
        self.sun_tzu = SunTzuEngine()
        self.quant = QuantEngine()
        self.learner = SelfLearner()
        self.total_matches = 0
        self.total_correct = 0
        self.all_results = []
        self.delay = 3  # Seconds between API calls
        
    def wait(self, seconds=None):
        """Wait to avoid rate limiting"""
        if seconds is None:
            seconds = self.delay
        print(".", end="", flush=True)
        time.sleep(seconds)
    
    def fetch_matches(self, league_code, season):
        """Fetch matches with retry and delay"""
        url = f"{self.api_url}/competitions/{league_code}/matches"
        params = {"season": season, "status": "FINISHED"}
        headers = {"X-Auth-Token": API_KEY}
        
        for attempt in range(3):
            try:
                print(f"\n  Fetching {season}...", end=" ")
                response = requests.get(url, headers=headers, params=params, timeout=15)
                self.wait(2)  # Delay after each API call
                
                if response.status_code == 200:
                    data = response.json()
                    matches = data.get("matches", [])
                    print(f"found {len(matches)}")
                    return matches
                elif response.status_code == 429:
                    print(f"Rate limited. Waiting 60s...")
                    time.sleep(60)
                elif response.status_code == 403:
                    print(f"Access denied. Skipping...")
                    return []
                else:
                    print(f"Error: {response.status_code}")
                    self.wait(5)
            except Exception as e:
                print(f"Error: {e}")
                self.wait(10)
        
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
    
    def backtest_league_season(self, league_key, season):
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
        
        # Get all teams
        teams = set()
        for m in matches:
            home = m.get("homeTeam", {}).get("name", "")
            away = m.get("awayTeam", {}).get("name", "")
            if home: teams.add(home)
            if away: teams.add(away)
        
        print(f"  {len(teams)} teams, {len(matches)} matches")
        
        # Calculate team stats
        team_stats = {}
        for team in teams:
            team_stats[team] = self.get_team_stats(team, matches)
        
        season_correct = 0
        season_total = 0
        
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
            
            # Update chapter weights in SQLite
            chapter_scores = {}
            for ch in result.get("chapter_breakdown", []):
                ch_num = ch.get("chapter", 0)
                verdict = ch.get("verdict", "NEUTRAL")
                if correct:
                    chapter_scores[ch_num] = (verdict == "PRO")
                else:
                    chapter_scores[ch_num] = (verdict == "CON")
            
            if chapter_scores:
                pred_id = result.get("prediction_id", f"online_{season}_{idx}")
                try:
                    self.quant.record_outcome(pred_id, correct, "sports", league_key, chapter_scores)
                except:
                    pass
            
            if (idx + 1) % 50 == 0:
                print(f"  Processed {idx + 1}/{len(matches)}...")
        
        acc = (season_correct / season_total * 100) if season_total > 0 else 0
        print(f"  ✅ {season_correct}/{season_total} = {acc:.1f}%")
        
        self.total_correct += season_correct
        self.total_matches += season_total
        
        return {
            "league": league_name,
            "season": season,
            "total": season_total,
            "correct": season_correct,
            "accuracy": acc
        }
    
    def run_all(self):
        """Run backtest for all leagues and seasons"""
        seasons = ["2022", "2023", "2024", "2025"]
        leagues = ["epl", "laliga", "bundesliga", "seriea", "ligue1"]
        
        print("\n⏳ Starting backtest with 3-second delays...")
        print("   This will take time but will avoid rate limits.\n")
        
        for league in leagues:
            for season in seasons:
                result = self.backtest_league_season(league, season)
                if result:
                    self.all_results.append(result)
                    self.print_summary()
                
                # Extra delay between seasons
                print(f"  ⏳ Waiting 5 seconds before next...")
                time.sleep(5)
            
            # Extra delay between leagues
            print(f"\n⏳ Waiting 10 seconds before next league...")
            time.sleep(10)
        
        return self.all_results
    
    def print_summary(self):
        print("\n" + "=" * 60)
        print("📊 BACKTEST SUMMARY")
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
        with open("online_full_results.json", "w") as f:
            json.dump(self.all_results, f, indent=2)

def main():
    print("=" * 60)
    print("🔶 FULL ONLINE BACKTEST - WITH DELAYS")
    print("   ALL Leagues · ALL Seasons (2022-2025)")
    print("   Rate limit: 3s delay between API calls")
    print("=" * 60)
    
    tester = FullOnlineBacktester()
    tester.run_all()
    tester.print_summary()
    
    print("\n✅ Complete!")
    print("📁 Results saved to online_full_results.json")
    print("📊 Weights updated in SQLite")

if __name__ == "__main__":
    main()
