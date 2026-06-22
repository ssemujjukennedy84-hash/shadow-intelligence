"""
Shadow - Complete Universal Data Mapper
Every Sun Tzu concept mapped to trading & sports equivalents.
Zero NEUTRAL from missing data.
"""

def map_trading(raw):
    """Map market data to ALL Sun Tzu keys. Nothing left unmapped."""
    price = raw.get("price", 0)
    atr = raw.get("atr", price * 0.005)
    rsi = raw.get("rsi", 50)
    trend = raw.get("trend", "neutral")
    change = raw.get("change_pct", 0)
    volume = raw.get("volume_avg", 0)
    high = raw.get("high_30d", price * 1.1)
    low = raw.get("low_30d", price * 0.9)
    ma20 = raw.get("ma_20", price)
    ma50 = raw.get("ma_50", price)
    
    # Position in range
    price_range = high - low
    position = (price - low) / max(price_range, 0.01)
    
    # Trend strength
    if trend == "bullish": trend_strength = min(1.0, position)
    elif trend == "bearish": trend_strength = min(1.0, 1 - position)
    else: trend_strength = 0.5
    
    # Volume analysis
    vol_ratio = min(3.0, volume / 500000) if volume > 0 else 0.5
    
    return {
        **raw,  # Preserve original fields including name
        
        # ── CORE METRICS ──
        "strength": min(10, max(1, 5 + change/2 + (50-rsi)/10 + trend_strength * 3)),
        "energy": min(100, max(10, abs(change) * 5 + volume/100000 + (70 if trend=="bullish" else 30))),
        "morale": 8 if trend == "bullish" and rsi > 50 else 3 if trend == "bearish" and rsi < 50 else 5,
        "intelligence": 8 if raw.get("source") == "YAHOO" else 5,
        "resources": min(100, max(10, volume/5000)),
        
        # ── HEAVEN (Market Conditions) ──
        "weather": "Clear" if 30 < rsi < 70 and abs(change) < 3 else 
                   "Storm" if rsi > 80 or rsi < 20 or abs(change) > 5 else
                   "Rain" if rsi > 70 or rsi < 30 else "Cloudy",
        "temperature": int(50 + (rsi - 50)),
        "wind_speed": int(abs(change) * 10),
        "humidity": int(volume / 10000),
        "season_advantage": trend == "bullish",
        "time_advantage": rsi > 50 and rsi < 70,
        "heaven_score": min(10, max(1, 5 + (trend_strength * 3) + (1 if rsi > 50 else -1))),
        
        # ── EARTH (Market Structure) ──
        "altitude": int(price / 1000),
        "pitch_condition": "good" if trend != "neutral" and 30 < rsi < 70 else 
                          "average" if trend != "neutral" else "poor",
        "capacity": int(volume / 10),
        "travel_distance": int(abs(change) * 100) if change < 0 else 0,
        "home_away": "home" if trend == "bullish" else "away" if trend == "bearish" else "neutral",
        "earth_score": min(10, max(1, 5 + (position - 0.5) * 5)),
        
        # ── COMMANDER (Trader's Quality) ──
        "manager_quality": min(10, max(1, 5 + (1 if trend == "bullish" else -1) + (1 if rsi > 50 else -1))),
        "discipline": 7 if abs(change) < 3 else 5 if abs(change) < 5 else 3,
        "team_harmony": 8 if trend == "bullish" and rsi > 50 else 5 if trend != "neutral" else 3,
        "comeback_wins": 1 if rsi < 35 and trend == "bullish" else 0,
        "commander_score": min(10, max(1, (5 + (1 if trend=="bullish" else -1) + (1 if rsi>50 else -1)))),
        "preparation": 7 if 40 < rsi < 60 else 5,
        "organization": 7 if volume > 300000 else 5,
        "five_score": min(10, max(1, 5 + trend_strength * 3)),
        "seven_score": min(10, max(1, 5 + trend_strength * 2 + (1 if rsi > 50 else -1))),
        
        # ── METHOD (Capital & Risk) ──
        "squad_value": int(volume),
        "squad_depth": 25 if volume > 500000 else 15 if volume > 200000 else 8,
        "supply_line": 7 if trend == "bullish" else 5 if trend == "neutral" else 3,
        "fixture_congestion": 2 if abs(change) < 1 else 4 if abs(change) < 3 else 6,
        "method_score": min(10, max(1, 5 + vol_ratio)),
        
        # ── MOMENTUM (Energy) ──
        "momentum": round(change/5, 2),
        "change_pct": round(change, 2),
        "form": "WWW" if trend == "bullish" and rsi > 60 else 
                "WLL" if trend == "bearish" else 
                "WDL" if trend == "bullish" else "LDL",
        "trend": trend,
        "rsi": round(rsi, 1),
        "rsi_14": round(rsi, 1),
        "possession": 60 if volume > 300000 else 40,
        "shots_on_target": int(volume/50000),
        "recent_goals": int(price / 10000),
        "first_half": round(price * 0.3, 2),
        "second_half": round(price * 0.7, 2),
        
        # ── DEFENSE (Risk Management) ──
        "goals_against": round(atr * 100, 2),
        "clean_sheets": 1 if rsi < 50 and trend == "bullish" else 0,
        "losses": 1 if change < -2 else 0,
        "draws": 0 if abs(change) > 0.5 else 1,
        "defensive_strength": min(10, max(1, 10 - (atr / price * 1000))),
        "saves": int(volume / 10000),
        "tackles": int(volume / 50000),
        "interceptions": 1 if rsi > 70 or rsi < 30 else 0,
        
        # ── ATTACK (Entry Signals) ──
        "goals_for": round(price / 1000, 2),
        "home_goals": round(price * 0.6 / 1000, 2),
        "away_goals": round(price * 0.4 / 1000, 2),
        "counter_attack": 1 if rsi < 35 and trend == "bullish" else 0,
        "set_pieces": 0,
        "avg_goals_for": round(price / 50000, 2),
        "avg_goals_against": round(atr * 10, 2),
        
        # ── ASYMMETRIES (Weak Points) ──
        "high_30d": round(high, 4),
        "low_30d": round(low, 4),
        "ma_20": round(ma20, 4),
        "ma_50": round(ma50, 4),
        "volatility": round(atr, 4),
        "atr": round(atr, 4),
        
        # ── SITUATION ──
        "must_win": change < -5 or rsi < 25,
        "risk_level": min(10, max(1, int(abs(change) + (70 - min(70, max(30, rsi))) / 10))),
        "importance": 8 if abs(change) > 3 or rsi > 70 or rsi < 30 else 5,
        "played": 100,
        "tournament_stage": "final" if rsi > 75 or rsi < 25 else "group" if 40 < rsi < 60 else "knockout",
        "pressure": min(10, max(1, int(abs(change) * 2))),
        "rivalry": 1 if abs(change) > 3 else 0,
        
        # ── EXTERNAL FORCES (Fire) ──
        "crowd_support": 7 if volume > 500000 else 4,
        "crowd": 7 if volume > 500000 else 4,
        "media_pressure": 3 if abs(change) < 2 else 7 if abs(change) > 4 else 5,
        "media": 5,
        "referee_bias": 0,
        
        # ── INTELLIGENCE (Spies) ──
        "news_count": 3,
        "source": raw.get("source", "YAHOO"),
        "data_freshness": 1,
        "data_fresh": 1,
        "injury_news": [],
        "injuries": 0,
        "injury_count": 0,
        "suspension": 0,
        "scout_report": 1 if volume > 400000 else 0,
        "h2h_advantage": 1 if rsi > 60 and trend == "bullish" else 0,
        "h2h": 1 if rsi > 60 and trend == "bullish" else 0,
        
        # ── ADAPTABILITY ──
        "formation_changes": 2 if abs(change) > 2 else 1,
        "formations": 2 if abs(change) > 2 else 1,
        "lead_lost": 1 if rsi > 70 else 0,
        "morale_change": 1 if change > 0 else -1 if change < 0 else 0,
        "congestion": 3 if abs(change) < 2 else 5,
        
        # ── ADDITIONAL ──
        "wins": int(trend_strength * 10),
        "founded": "2009",
        "away_wins": 1 if trend == "bullish" else 0,
        "rest_days": 3,
        "fixture_congestion": 3 if abs(change) < 2 else 5,
        "volume_avg": volume,
    }


def map_sports(raw):
    """Map sports data to Sun Tzu keys."""
    wins = raw.get("wins", 0) or 0
    losses = raw.get("losses", 0) or 0
    draws = raw.get("draws", 0) or 0
    played = wins + losses + draws
    gf = raw.get("goals_for", 0) or 0
    ga = raw.get("goals_against", 0) or 0
    form = raw.get("form", "")
    clean = raw.get("clean_sheets", 0) or 0
    
    win_rate = wins / max(played, 1)
    goal_diff = (gf - ga) / max(played, 1)
    form_wins = form.count("W")
    form_losses = form.count("L")
    
    return {
        **raw,
        "strength": min(10, max(1, win_rate * 8 + goal_diff * 2)),
        "energy": min(100, max(10, form_wins * 15 + wins * 5)),
        "morale": 9 if form_wins >= 3 else 5 if form_wins >= 1 else 3,
        "intelligence": 8 if raw.get("team_id") else 5,
        "resources": raw.get("squad_value", 300),
        
        "weather": raw.get("weather", "Clear"),
        "altitude": raw.get("altitude", 0),
        "temperature": raw.get("temperature", 20),
        "wind_speed": raw.get("wind_speed", 0),
        "humidity": raw.get("humidity", 50),
        "pitch_condition": raw.get("pitch_condition", "good"),
        "capacity": raw.get("capacity", 50000),
        "travel_distance": raw.get("travel_distance", 0),
        "home_away": raw.get("home_away", "neutral"),
        "season_advantage": raw.get("season_advantage", False),
        "time_advantage": raw.get("time_advantage", False),
        
        "manager_quality": raw.get("manager_quality", 6),
        "discipline": raw.get("discipline", 6),
        "team_harmony": raw.get("team_harmony", 6),
        "comeback_wins": raw.get("comeback_wins", 0),
        "preparation": raw.get("preparation", 6),
        "organization": 7 if played > 10 else 5,
        "five_score": win_rate * 10,
        "seven_score": win_rate * 7 + (clean/max(played,1)) * 3,
        "commander_score": raw.get("manager_quality", 6),
        "heaven_score": 5 + (1 if raw.get("weather","") in ["Clear","Cloudy"] else -1),
        "earth_score": 5 + (1 if raw.get("home_away","")=="home" else 0),
        "method_score": 5 + (1 if played > 10 else 0),
        
        "squad_value": raw.get("squad_value", 300),
        "squad_depth": raw.get("squad_depth", 20),
        "supply_line": 7 if raw.get("home_away") == "home" else 5,
        "fixture_congestion": raw.get("fixture_congestion", 3),
        
        "momentum": form_wins - form_losses,
        "change_pct": (win_rate - 0.5) * 20,
        "form": form,
        "trend": "bullish" if form_wins >= 3 else "bearish" if form_losses >= 3 else "neutral",
        "rsi": 50 + (form_wins - form_losses) * 10,
        "rsi_14": 50 + (form_wins - form_losses) * 10,
        "possession": raw.get("possession", 50),
        "shots_on_target": raw.get("shots_on_target", 0),
        "recent_goals": gf,
        "first_half": raw.get("first_half", 0),
        "second_half": raw.get("second_half", 0),
        
        "goals_for": gf,
        "goals_against": ga,
        "clean_sheets": clean,
        "losses": losses,
        "draws": draws,
        "wins": wins,
        "played": played,
        "defensive_strength": min(10, max(1, 10 - (ga/max(played,1))*2)),
        "saves": raw.get("saves", 0),
        "tackles": raw.get("tackles", 0),
        "interceptions": raw.get("interceptions", 0),
        
        "home_goals": raw.get("home_goals", 0),
        "away_goals": raw.get("away_goals", 0),
        "counter_attack": raw.get("counter_attack", 0),
        "set_pieces": raw.get("set_pieces", 0),
        "avg_goals_for": gf / max(played, 1),
        "avg_goals_against": ga / max(played, 1),
        
        "high_30d": raw.get("high_30d", 0),
        "low_30d": raw.get("low_30d", 0),
        "ma_20": raw.get("ma_20", 0),
        "ma_50": raw.get("ma_50", 0),
        "volatility": raw.get("volatility", 0),
        "atr": raw.get("atr", 0),
        
        "must_win": raw.get("must_win", False),
        "risk_level": 5 if abs(goal_diff) < 1 else 3,
        "importance": 8 if played > 20 else 5,
        "played": played,
        "tournament_stage": raw.get("tournament_stage", "group"),
        "pressure": raw.get("pressure", 5),
        "rivalry": raw.get("rivalry", 0),
        
        "crowd_support": raw.get("crowd_support", 5),
        "crowd": raw.get("crowd_support", 5),
        "media_pressure": raw.get("media_pressure", 5),
        "media": raw.get("media_pressure", 5),
        "referee_bias": raw.get("referee_bias", 0),
        
        "news_count": raw.get("news_count", 3),
        "source": raw.get("source", "MANUAL"),
        "data_freshness": raw.get("data_freshness", 24),
        "data_fresh": raw.get("data_freshness", 24),
        "injury_news": raw.get("injury_news", []),
        "injuries": raw.get("injury_count", 0),
        "injury_count": raw.get("injury_count", 0),
        "suspension": raw.get("suspension", 0),
        "scout_report": raw.get("scout_report", 0),
        "h2h_advantage": raw.get("h2h_advantage", 0),
        "h2h": raw.get("h2h_advantage", 0),
        
        "formation_changes": raw.get("formation_changes", 2),
        "formations": raw.get("formation_changes", 2),
        "lead_lost": raw.get("lead_lost", 0),
        "morale_change": 1 if form_wins >= 2 else -1 if form_losses >= 2 else 0,
        "congestion": raw.get("fixture_congestion", 3),
        
        "founded": raw.get("founded", "2000"),
        "away_wins": raw.get("away_wins", 0),
        "rest_days": raw.get("rest_days", 4),
        "volume_avg": raw.get("volume_avg", 0),
    }


def map_entity(raw, domain):
    if domain in ["trading", "crypto", "forex", "stocks"]:
        return map_trading(raw)
    elif domain in ["sports", "football", "soccer", "betting"]:
        return map_sports(raw)
    return raw