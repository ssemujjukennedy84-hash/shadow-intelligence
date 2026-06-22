"""Shadow - Chapter 2: Waging War (Trading Version)
Complete. Every principle. Every strategy. Every idea."""

def CHAPTER_2_RULES():
    return [
        # ═══════════════════════════════════════════════
        # THE COST OF TRADING
        # ═══════════════════════════════════════════════
        ("1. When you declare a trade, capital is mobilized at great cost", lambda e: "PRO" if e.get("capital_risk",5) < 5 else "CON" if e.get("capital_risk",5) > 7 else "NEUTRAL"),
        ("2. Spread, commissions, and slippage are the chariots and provisions of trading", lambda e: "CON" if e.get("spread_cost",0) > 2 else "NEUTRAL"),
        ("3. A hundred trades can be placed, but at what cost to your account?", lambda e: "CON" if e.get("fixture_congestion",0) > 5 and e.get("squad_depth",0) < 15 else "NEUTRAL"),
        ("4. The daily expenditure of overtrading drains your treasury", lambda e: "CON" if e.get("energy",50) < 40 and e.get("played",0) > 20 else "NEUTRAL"),
        ("5. The cost of trading exhausts your mental capital and focus", lambda e: "CON" if e.get("squad_value",0) < 200 and e.get("fixture_congestion",0) > 3 else "NEUTRAL"),
        ("6. Every entry has a cost — know it before you place the trade", lambda e: "PRO" if e.get("preparation",5) > 6 else "CON" if e.get("preparation",5) < 3 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE DANGER OF HOLDING LOSERS
        # ═══════════════════════════════════════════════
        ("7. There is no instance of a trader benefiting from holding losing positions", lambda e1,e2: "CON" if e1.get("fixture_congestion",0) > 5 else "PRO" if e2.get("fixture_congestion",0) > 5 else "NEUTRAL"),
        ("8. Protracted losses exhaust your capital and dull your edge", lambda e: "CON" if e.get("energy",50) < 40 and e.get("played",0) > 15 else "NEUTRAL"),
        ("9. Long losing streaks drain morale and cloud judgment", lambda e: "CON" if e.get("morale",5) < 5 and e.get("played",0) > 15 else "NEUTRAL"),
        ("10. The trader's edge wears down like a blade used too long", lambda e: "CON" if e.get("form","").count("L") >= 3 and e.get("played",0) > 10 else "NEUTRAL"),
        ("11. When your capital is depleted, other opportunities will pass you by", lambda e: "CON" if e.get("strength",5) < 5 and e.get("played",0) > 20 else "NEUTRAL"),
        ("12. Even the most disciplined trader cannot recover from a blown account", lambda e: "CON" if e.get("manager_quality",5) > 7 and e.get("energy",50) < 30 else "NEUTRAL"),
        ("13. The market does not forgive the trader who refuses to cut losses", lambda e: "CON" if e.get("discipline",5) < 4 and e.get("drawdown",0) > 20 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE ESSENCE OF SPEED IN EXECUTION
        # ═══════════════════════════════════════════════
        ("14. Rapidity is the essence of profitable trading", lambda e1,e2: "PRO" if e1.get("energy",50) > e2.get("energy",50)*1.3 else "CON" if e2.get("energy",50) > e1.get("energy",50)*1.3 else "NEUTRAL"),
        ("15. Take advantage of the market's unreadiness at key levels", lambda e1,e2: "PRO" if e1.get("preparation",5) > e2.get("preparation",5)+2 else "NEUTRAL"),
        ("16. Enter by unexpected routes — where the crowd is not looking", lambda e1,e2: "PRO" if e1.get("counter_attack",0) > e2.get("counter_attack",0) else "NEUTRAL"),
        ("17. Strike where the market has taken no precautions", lambda e1,e2: "PRO" if e2.get("clean_sheets",0) < 2 else "NEUTRAL"),
        ("18. Speed turns a small edge into a decisive profit before the crowd arrives", lambda e: "PRO" if e.get("energy",50) > 70 and e.get("form","").count("W") >= 2 else "NEUTRAL"),
        ("19. The swift completion of a trade saves capital, focus, and opportunity", lambda e: "PRO" if e.get("energy",50) > 60 and e.get("played",0) < 10 else "NEUTRAL"),
        ("20. Enter fast, exit faster when wrong, let winners run when right", lambda e: "PRO" if e.get("discipline",5) > 7 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # RESOURCE MANAGEMENT
        # ═══════════════════════════════════════════════
        ("21. A skilled trader does not require a second deposit", lambda e: "PRO" if e.get("squad_depth",0) > 20 else "NEUTRAL"),
        ("22. Their risk capital is not deployed more than necessary", lambda e: "PRO" if e.get("supply_line",5) > 6 else "NEUTRAL"),
        ("23. Use your own capital as the base", lambda e: "PRO" if e.get("home_away","") == "home" else "NEUTRAL"),
        ("24. But let the market's momentum carry your profits", lambda e1,e2: "PRO" if e1.get("goals_for",0) > e2.get("goals_for",0)*1.2 else "CON" if e2.get("goals_for",0) > e1.get("goals_for",0)*1.2 else "NEUTRAL"),
        ("25. One runner trade equals twenty small scalps", lambda e1,e2: "PRO" if e1.get("away_wins",0) > 0 and e2.get("goals_against",0) > e1.get("goals_against",0) else "NEUTRAL"),
        ("26. The cost of holding through high volatility ruins accounts", lambda e: "CON" if e.get("travel_distance",0) > 5000 else "PRO" if e.get("travel_distance",0) < 500 else "NEUTRAL"),
        ("27. Supply lines must be short — risk per trade must be controlled", lambda e: "CON" if e.get("travel_distance",0) > 3000 and e.get("supply_line",5) < 5 else "NEUTRAL"),
        ("28. Never risk more than you can afford to lose on any single trade", lambda e: "PRO" if e.get("capital_risk",5) < 4 else "CON" if e.get("capital_risk",5) > 6 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # MOTIVATION THROUGH PROFIT
        # ═══════════════════════════════════════════════
        ("29. Book profits regularly — this fuels confidence and compounds capital", lambda e: "PRO" if e.get("crowd_support",5) > 7 else "NEUTRAL"),
        ("30. In trading, reward yourself by taking partial profits at targets", lambda e: "PRO" if e.get("first_half",0) > e.get("second_half",0) else "NEUTRAL"),
        ("31. Treat your capital with care — it is your army", lambda e: "PRO" if e.get("team_harmony",5) > 6 else "NEUTRAL"),
        ("32. This is called: using winning trades to fund future opportunities", lambda e1,e2: "PRO" if e1.get("squad_value",0) > e2.get("squad_value",0) else "NEUTRAL"),
        ("33. Victory through compounding is more powerful than one big win", lambda e: "PRO" if e.get("team_harmony",5) > 7 else "NEUTRAL"),
        ("34. The spoils of a winning trade should fuel the next, not sit idle", lambda e: "PRO" if e.get("energy",50) > 60 and e.get("squad_value",0) > 300 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE ULTIMATE OBJECTIVE
        # ═══════════════════════════════════════════════
        ("35. In trading, let your great object be consistent profitability", lambda e1,e2: "PRO" if e1.get("goals_for",0) > e2.get("goals_for",0) and e1.get("goals_against",0) < e2.get("goals_against",0) else "CON" if e2.get("goals_for",0) > e1.get("goals_for",0) and e2.get("goals_against",0) < e1.get("goals_against",0) else "NEUTRAL"),
        ("36. Not one massive win that you give back to the market", lambda e: "CON" if e.get("fixture_congestion",0) > 5 else "NEUTRAL"),
        ("37. Profit must be decisive, consistent, and protected", lambda e: "PRO" if e.get("form","").count("W") >= 3 and e.get("energy",50) > 60 else "NEUTRAL"),
        ("38. The trader who understands risk is the guardian of their wealth", lambda e: "PRO" if e.get("manager_quality",5) > 7 and e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("39. Never let a trade linger in loss — hope is the enemy of profit", lambda e: "CON" if e.get("energy",50) < 50 and e.get("played",0) > 10 else "NEUTRAL"),
        ("40. The wise trader attacks the market's weakness, not its strength", lambda e1,e2: "PRO" if e1.get("counter_attack",0) > e2.get("counter_attack",0) and e1.get("intelligence",5) > e2.get("intelligence",5) else "NEUTRAL"),
        ("41. Every moment in a bad trade consumes your future opportunities", lambda e: "CON" if e.get("fixture_congestion",0) > 5 and e.get("energy",50) < 50 else "NEUTRAL"),
        ("42. The trader who finishes quickly preserves capital for the next setup", lambda e: "PRO" if e.get("energy",50) > 65 and e.get("played",0) < 8 else "NEUTRAL"),
    ]