"""Shadow - Chapter 3: Attack by Stratagem (Trading Version)
Complete. Every principle. Every strategy. Every idea."""

def CHAPTER_3_RULES():
    return [
        # ═══════════════════════════════════════════════
        # THE SUPREME ART OF TRADING
        # ═══════════════════════════════════════════════
        ("1. In the practical art of trading, the best thing is to take profits whole and intact", lambda e: "PRO" if e.get("profit_factor",0) > 1.5 else "NEUTRAL"),
        ("2. Supreme excellence consists in profiting without large drawdowns", lambda e: "PRO" if e.get("drawdown",0) < 10 and e.get("profit_factor",0) > 1.5 else "NEUTRAL"),
        ("3. The highest form of trading is to let winners run with trailing stops", lambda e: "PRO" if e.get("take_profit_pct",0) > 3 else "NEUTRAL"),
        ("4. Next best is cutting losses at predetermined levels without hesitation", lambda e: "PRO" if e.get("discipline",5) > 7 and e.get("stop_loss_set",False) else "NEUTRAL"),
        ("5. Next is entering on pullbacks in a strong trend", lambda e: "PRO" if e.get("trend_strength",0) > 0.6 and e.get("position_in_range",0) < 0.4 else "NEUTRAL"),
        ("6. The worst policy of all is averaging down on losing positions", lambda e: "CON" if e.get("lead_lost",0) > 0 else "NEUTRAL"),
        ("7. Averaging down exhausts capital and multiplies losses", lambda e: "CON" if e.get("energy",50) < 40 and e.get("squad_value",0) < 200 else "NEUTRAL"),
        ("8. The impatient trader who enters without confirmation loses capital", lambda e: "CON" if e.get("discipline",5) < 4 and e.get("manager_quality",5) < 5 else "NEUTRAL"),
        ("9. A large portion of their account is lost and the setup never materializes", lambda e: "CON" if e.get("drawdown",0) > 15 and e.get("form","").count("W") < 2 else "NEUTRAL"),
        ("10. Such are the disastrous effects of forcing trades", lambda e: "CON" if e.get("losses",0) > 3 and e.get("goals_for",0) < 5 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE SKILLFUL TRADER
        # ═══════════════════════════════════════════════
        ("11. The skillful trader profits without overtrading", lambda e: "PRO" if e.get("fixture_congestion",0) < 3 and e.get("profit_factor",0) > 1.2 else "NEUTRAL"),
        ("12. They capture trends without chasing entries at extremes", lambda e: "PRO" if e.get("position_in_range",0) < 0.4 else "NEUTRAL"),
        ("13. They compound their account without lengthy drawdown periods", lambda e: "PRO" if e.get("form","").count("W") >= 4 and e.get("energy",50) > 60 else "NEUTRAL"),
        ("14. With capital intact, they seize the next high-probability setup", lambda e: "PRO" if e.get("squad_depth",0) > 20 and e.get("strength",5) > 7 else "NEUTRAL"),
        ("15. Their triumph is complete without suffering a single catastrophic loss", lambda e: "PRO" if e.get("drawdown",0) < 5 and e.get("comeback_wins",0) > 0 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE ART OF POSITION SIZING
        # ═══════════════════════════════════════════════
        ("16. If the setup quality is ten to one, size up confidently", lambda e: "PRO" if e.get("setup_quality",5) > 8 else "NEUTRAL"),
        ("17. If five to one, trade normal position size", lambda e: "PRO" if e.get("setup_quality",5) > 6 else "NEUTRAL"),
        ("18. If the odds are equal, trade small or pass entirely", lambda e: "NEUTRAL" if 4 < e.get("setup_quality",5) < 6 else "NEUTRAL"),
        ("19. If the setup is weak, do not trade at all — preserve capital", lambda e: "CON" if e.get("setup_quality",5) < 3 else "NEUTRAL"),
        ("20. If the market is strongly against you, stay flat and wait", lambda e: "CON" if e.get("trend_strength",0) < 0.3 and e.get("trend","") == "bearish" else "NEUTRAL"),
        ("21. A small force cannot attack a large trend — do not fight the market", lambda e: "CON" if e.get("position_size",0) > 20 and e.get("trend_strength",0) < 0.4 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE THREE WAYS A TRADER BRINGS MISFORTUNE
        # ═══════════════════════════════════════════════
        ("22. A trader brings misfortune by entering when the setup is not confirmed", lambda e: "CON" if e.get("manager_quality",5) < 4 and e.get("discipline",5) > 6 else "NEUTRAL"),
        ("23. By exiting a winning trade too early out of fear", lambda e: "CON" if e.get("manager_quality",5) < 4 and e.get("morale",5) > 6 else "NEUTRAL"),
        ("24. This is called hobbling your own account", lambda e: "CON" if e.get("organization",5) < 4 else "NEUTRAL"),
        ("25. By interfering with your trading plan without understanding the market", lambda e: "CON" if e.get("intelligence",5) < 4 and e.get("discipline",5) > 5 else "NEUTRAL"),
        ("26. This causes doubt and inconsistency in your execution", lambda e: "CON" if e.get("team_harmony",5) < 5 and e.get("morale",5) < 5 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE FIVE ESSENTIALS FOR PROFITABLE TRADING
        # ═══════════════════════════════════════════════
        ("27. He will profit who knows when to trade and when to stay in cash", lambda e: "PRO" if e.get("intelligence",5) > 6 and e.get("patience",5) > 6 else "NEUTRAL"),
        ("28. He will profit who knows how to size positions correctly for the setup", lambda e: "PRO" if e.get("manager_quality",5) > 6 and e.get("position_size",0) < 15 else "NEUTRAL"),
        ("29. He will profit whose trading is animated by consistent discipline", lambda e: "PRO" if e.get("team_harmony",5) > 6 and e.get("discipline",5) > 6 else "NEUTRAL"),
        ("30. He will profit who, prepared, waits for the market to come to his level", lambda e: "PRO" if e.get("preparation",5) > 6 and e.get("patience",5) > 6 else "NEUTRAL"),
        ("31. He will profit who has a tested strategy and is not interfered with by emotions", lambda e: "PRO" if e.get("manager_quality",5) > 7 and e.get("organization",5) > 6 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # KNOW YOURSELF, KNOW THE MARKET
        # ═══════════════════════════════════════════════
        ("32. If you know the market and know yourself, you need not fear losses", lambda e1,e2: "PRO" if e1.get("intelligence",5) > e2.get("intelligence",5) and e1.get("strength",5) > e2.get("strength",5) else "CON" if e2.get("intelligence",5) > e1.get("intelligence",5) and e2.get("strength",5) > e1.get("strength",5) else "NEUTRAL"),
        ("33. If you know yourself but not the market, for every win you will also suffer a loss", lambda e: "CON" if e.get("intelligence",5) < 5 and e.get("preparation",5) > 5 else "NEUTRAL"),
        ("34. If you know neither the market nor yourself, you will lose everything", lambda e: "CON" if e.get("intelligence",5) < 3 and e.get("preparation",5) < 3 else "NEUTRAL"),
        ("35. Knowledge of market structure and self-discipline is the foundation of profit", lambda e: "PRO" if e.get("intelligence",5) > 6 and e.get("discipline",5) > 6 else "NEUTRAL"),
        ("36. The trader who studies both the chart and their own psychology will thrive", lambda e: "PRO" if e.get("intelligence",5) > 7 and e.get("manager_quality",5) > 7 else "NEUTRAL"),
        ("37. The trader who studies neither will not survive", lambda e: "CON" if e.get("intelligence",5) < 3 and e.get("manager_quality",5) < 3 else "NEUTRAL"),
    ]