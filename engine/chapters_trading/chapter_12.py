"""Shadow - Chapter 12: Attack by Fire (Trading Version)
Complete. Every principle. Every strategy. Every idea.
Using external forces. Volatility as a weapon. Market catalysts."""

def CHAPTER_12_RULES():
    return [
        # ═══════════════════════════════════════════════
        # THE FIVE WAYS TO USE FIRE IN TRADING
        # ═══════════════════════════════════════════════
        ("1. There are five ways of attacking with fire in the markets", lambda e: "PRO" if e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("2. The first is to burn the enemy's stores — trade against trapped traders who must exit", lambda e: "PRO" if e.get("at_resistance",False) and e.get("rsi",50) > 70 else "NEUTRAL"),
        ("3. The second is to burn their provisions — enter when stop losses are clustered and about to be triggered", lambda e: "PRO" if e.get("at_support",False) and e.get("rsi",50) < 30 else "NEUTRAL"),
        ("4. The third is to burn their baggage train — trade the liquidation cascade when overleveraged positions unwind", lambda e: "PRO" if e.get("momentum",0) > 3 and e.get("volume_avg",0) > 600000 else "NEUTRAL"),
        ("5. The fourth is to burn their arsenals — trade against a crowded narrative that is about to reverse", lambda e: "PRO" if e.get("rsi",50) > 75 or e.get("rsi",50) < 25 else "NEUTRAL"),
        ("6. The fifth is to hurl fire among them — use news events and economic data as catalysts", lambda e: "PRO" if e.get("volatility",0) > e.get("price",0)*0.02 and e.get("volume_avg",0) > 500000 else "NEUTRAL"),
        ("7. Fire must be used as a weapon when market conditions are right", lambda e: "PRO" if e.get("volatility",0) > e.get("price",0)*0.02 else "NEUTRAL"),
        ("8. There are appropriate seasons for trading volatility — high impact news and market opens", lambda e: "PRO" if e.get("time_advantage",False) else "NEUTRAL"),
        ("9. Dry weather and wind — low liquidity and high emotion — make fire spread fastest", lambda e: "PRO" if e.get("volume_avg",0) < 200000 and e.get("volatility",0) > e.get("price",0)*0.02 else "NEUTRAL"),
        ("10. In quiet markets, fire burns slowly — in emotional markets, it rages", lambda e: "PRO" if e.get("volatility",0) > e.get("price",0)*0.03 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # RESPONDING TO MARKET FIRE
        # ═══════════════════════════════════════════════
        ("11. When fire breaks out in the enemy's camp — when a breakout occurs — respond immediately with follow-through", lambda e: "PRO" if e.get("momentum",0) > 2 and e.get("entry_trigger",False) else "NEUTRAL"),
        ("12. If the enemy's soldiers are quiet after fire starts — price pauses after a spike — wait and do not attack yet", lambda e: "CON" if e.get("momentum",0) > 1 and e.get("volume_avg",0) < 300000 else "NEUTRAL"),
        ("13. When the fire reaches its height — when the move is at maximum velocity — attack if you are positioned", lambda e: "PRO" if e.get("momentum",0) > 3 and e.get("energy",50) > 70 else "NEUTRAL"),
        ("14. If you cannot, wait — do not force an entry during chaos", lambda e: "PRO" if e.get("patience",5) > 6 else "NEUTRAL"),
        ("15. Fire may be set from outside the enemy's camp — a news event can trigger a move without you being in it", lambda e: "PRO" if e.get("counter_attack",0) > 0 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("16. Attack when the fire has done its damage — enter after the stop hunt, not during it", lambda e: "PRO" if e.get("comeback_wins",0) > 1 and e.get("position_in_range",0) < 0.3 else "NEUTRAL"),
        ("17. Do not attack when the fire is against you — do not trade against a news-driven move", lambda e: "CON" if e.get("trend","") == "bearish" and e.get("volatility",0) > e.get("price",0)*0.03 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # EXTERNAL FORCES AS WEAPONS
        # ═══════════════════════════════════════════════
        ("18. Those who use fire as a weapon understand market catalysts", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("19. Those who use water as a weapon understand market flow and liquidity", lambda e: "PRO" if e.get("volume_avg",0) > 400000 else "NEUTRAL"),
        ("20. Water can isolate positions — low liquidity traps traders", lambda e: "CON" if e.get("volume_avg",0) < 150000 else "NEUTRAL"),
        ("21. Fire can destroy everything — a single news event can wipe out months of gains", lambda e: "CON" if e.get("volatility",0) > e.get("price",0)*0.04 else "NEUTRAL"),
        ("22. To capture profits but fail to protect them is a waste of effort", lambda e: "CON" if e.get("profit_factor",0) > 1.5 and e.get("drawdown",0) > 20 else "NEUTRAL"),
        ("23. This is called wasteful delay — giving back what the market gave you", lambda e: "CON" if e.get("energy",50) < 40 and e.get("fixture_congestion",0) > 3 else "NEUTRAL"),
        ("24. The disciplined trader lays plans well ahead of market events", lambda e: "PRO" if e.get("preparation",5) > 6 else "NEUTRAL"),
        ("25. The good trader cultivates their resources and never risks more than planned", lambda e: "PRO" if e.get("capital_risk",5) < 5 and e.get("squad_depth",0) > 20 else "NEUTRAL"),
        ("26. Move not unless you see a clear advantage in the setup", lambda e: "PRO" if e.get("setup_quality",5) > 6 else "NEUTRAL"),
        ("27. Use not your capital unless there is a genuine edge to be captured", lambda e: "PRO" if e.get("preparation",5) > 5 else "NEUTRAL"),
        ("28. Trade not unless the risk/reward justifies the entry", lambda e: "PRO" if e.get("rr_ratio",0) > 1.5 else "NEUTRAL"),
        ("29. No trader should risk capital merely to satisfy the urge to trade", lambda e: "CON" if e.get("discipline",5) < 4 and e.get("manager_quality",5) < 5 else "NEUTRAL"),
        ("30. No one should enter a trade simply out of boredom or revenge", lambda e: "CON" if e.get("discipline",5) < 4 and e.get("intelligence",5) < 5 else "NEUTRAL"),
        ("31. If it is to your advantage, execute the trade — if not, stay in cash", lambda e: "PRO" if e.get("setup_quality",5) > 6 else "CON" if e.get("setup_quality",5) < 3 else "NEUTRAL"),
        ("32. Anger may fade, but a blown account cannot be restored", lambda e: "CON" if e.get("drawdown",0) > 30 else "NEUTRAL"),
        ("33. The capital lost cannot be brought back by wishing", lambda e: "CON" if e.get("drawdown",0) > 25 else "NEUTRAL"),
        ("34. Therefore the disciplined trader is prudent and the good strategist is cautious", lambda e: "PRO" if e.get("intelligence",5) > 6 and e.get("manager_quality",5) > 6 else "NEUTRAL"),
        ("35. This is the way to keep your account at peace and your capital intact", lambda e: "PRO" if e.get("discipline",5) > 6 and e.get("capital_risk",5) < 5 else "NEUTRAL"),
    ]