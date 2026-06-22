"""Shadow - Chapter 11: The Nine Situations (Trading Version)
Complete. Every principle. Every strategy. Every idea.
Nine market situations. Each with its own strategic response."""

def CHAPTER_11_RULES():
    return [
        # ═══════════════════════════════════════════════
        # THE NINE MARKET SITUATIONS
        # ═══════════════════════════════════════════════
        ("1. Trading recognizes nine varieties of market conditions", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        
        # 1. DISPERSIVE GROUND — Your own territory (familiar setup)
        ("2. Dispersive ground: when trading a setup you know well, in your comfort zone", lambda e: "PRO" if e.get("home_away","") == "home" and e.get("played",0) > 10 else "NEUTRAL"),
        ("3. On dispersive ground, do not become complacent — the familiar can still hurt you", lambda e: "CON" if e.get("preparation",5) < 5 and e.get("played",0) > 20 else "NEUTRAL"),
        ("4. On dispersive ground, unify your focus and respect every trade as if it were your first", lambda e: "PRO" if e.get("discipline",5) > 6 else "NEUTRAL"),
        ("5. Overconfidence in familiar setups leads to the largest losses", lambda e: "CON" if e.get("discipline",5) < 5 and e.get("played",0) > 15 else "NEUTRAL"),
        
        # 2. FRONTIER GROUND — New asset or strategy
        ("6. Frontier ground: when trading a new asset or testing a new strategy", lambda e: "PRO" if e.get("played",0) < 10 else "NEUTRAL"),
        ("7. On frontier ground, trade small — do not commit fully until proven", lambda e: "PRO" if e.get("position_size",0) < 8 else "NEUTRAL"),
        ("8. Test the waters before swimming deep", lambda e: "PRO" if e.get("preparation",5) > 6 and e.get("position_size",0) < 10 else "NEUTRAL"),
        
        # 3. CONTENTIOUS GROUND — Key support/resistance level
        ("9. Contentious ground: price at a major support or resistance level that both sides fight for", lambda e: "PRO" if e.get("at_support",False) or e.get("at_resistance",False) else "NEUTRAL"),
        ("10. On contentious ground, do not attack if the level has held repeatedly", lambda e: "CON" if e.get("at_resistance",False) and e.get("comeback_wins",0) > 2 else "NEUTRAL"),
        ("11. Race to position yourself before the breakout — but only with confirmation", lambda e: "PRO" if e.get("entry_trigger",False) and e.get("at_support",False) else "NEUTRAL"),
        ("12. The one who controls the key level controls the move", lambda e: "PRO" if e.get("position_in_range",0) < 0.3 else "NEUTRAL"),
        
        # 4. OPEN GROUND — Clear trending market
        ("13. Open ground: a clean trending market where both sides can see the direction", lambda e: "PRO" if e.get("trend_strength",0) > 0.6 else "NEUTRAL"),
        ("14. On open ground, do not try to fade the trend — ride it", lambda e: "PRO" if e.get("trend","") == "bullish" else "CON" if e.get("trend","") == "bearish" else "NEUTRAL"),
        ("15. Let the trend be your guide and it will carry you to profit", lambda e: "PRO" if e.get("trend_strength",0) > 0.7 else "NEUTRAL"),
        
        # 5. INTERSECTING GROUND — Multiple timeframes converging
        ("16. Intersecting ground: when multiple timeframes align at a single level", lambda e: "PRO" if e.get("tf_alignment",0) > 0.7 else "NEUTRAL"),
        ("17. On intersecting ground, trade with confidence — the odds are heavily in your favor", lambda e: "PRO" if e.get("tf_alignment",0) > 0.8 and e.get("setup_quality",5) > 7 else "NEUTRAL"),
        ("18. Multi-timeframe alignment is the strongest signal in trading", lambda e: "PRO" if e.get("tf_alignment",0) > 0.7 else "NEUTRAL"),
        
        # 6. SERIOUS GROUND — Deep in a trade
        ("19. Serious ground: when your position is deep in profit and you must manage it", lambda e: "PRO" if e.get("take_profit_pct",0) > 2 else "NEUTRAL"),
        ("20. On serious ground, trail your stop loss — protect what you have gained", lambda e: "PRO" if e.get("discipline",5) > 6 and e.get("stop_loss_set",False) else "NEUTRAL"),
        ("21. Do not give back profits you have already captured", lambda e: "CON" if e.get("drawdown",0) > 15 else "NEUTRAL"),
        ("22. Keep the position alive as long as the trend supports it", lambda e: "PRO" if e.get("trend_strength",0) > 0.5 and e.get("take_profit_pct",0) > 1 else "NEUTRAL"),
        
        # 7. DIFFICULT GROUND — High volatility, unclear direction
        ("23. Difficult ground: choppy markets with no clear direction and wide spreads", lambda e: "CON" if e.get("volatility",0) > e.get("price",0)*0.02 and e.get("trend","") == "neutral" else "NEUTRAL"),
        ("24. On difficult ground, keep your positions small and your stops tight", lambda e: "PRO" if e.get("position_size",0) < 5 and e.get("volatility",0) > e.get("price",0)*0.02 else "NEUTRAL"),
        ("25. Do not linger in difficult ground — exit quickly if wrong", lambda e: "PRO" if e.get("discipline",5) > 7 else "NEUTRAL"),
        ("26. Difficult ground is where most traders lose their capital", lambda e: "CON" if e.get("trend","") == "neutral" and e.get("position_size",0) > 10 else "NEUTRAL"),
        
        # 8. FATAL GROUND — Drawdown approaching maximum
        ("27. Fatal ground: when your drawdown approaches your maximum allowed loss", lambda e: "PRO" if e.get("drawdown",0) > 15 else "NEUTRAL"),
        ("28. On fatal ground, cut all positions immediately — survive to trade another day", lambda e: "PRO" if e.get("discipline",5) > 7 and e.get("drawdown",0) > 15 else "NEUTRAL"),
        ("29. There is no shame in protecting what remains of your capital", lambda e: "PRO" if e.get("discipline",5) > 6 else "NEUTRAL"),
        ("30. On fatal ground, make it clear to yourself: there is no retreat from risk management", lambda e: "PRO" if e.get("stop_loss_set",False) else "NEUTRAL"),
        
        # 9. DESPERATE GROUND — Last stand
        ("31. Desperate ground: when you have no choice but to survive", lambda e: "PRO" if e.get("drawdown",0) > 25 else "NEUTRAL"),
        ("32. On desperate ground, stop trading entirely — review, recover, rebuild", lambda e: "PRO" if e.get("discipline",5) > 7 else "NEUTRAL"),
        ("33. Soldiers in desperate straits fight to the death — protect your remaining capital at all costs", lambda e: "PRO" if e.get("drawdown",0) > 25 and e.get("discipline",5) > 6 else "NEUTRAL"),
        ("34. The trader who survives desperate ground emerges stronger", lambda e: "PRO" if e.get("comeback_wins",0) > 1 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE SKILLFUL TRADER IN ALL SITUATIONS
        # ═══════════════════════════════════════════════
        ("35. The skillful trader leads the market like a sheep on a string — by placing orders at key levels", lambda e: "PRO" if e.get("intelligence",5) > 6 and e.get("patience",5) > 6 else "NEUTRAL"),
        ("36. They make the market come to them by offering limit orders at support", lambda e: "PRO" if e.get("at_support",False) and e.get("patience",5) > 6 else "NEUTRAL"),
        ("37. They prevent losses by placing stops at logical levels", lambda e: "PRO" if e.get("stop_loss_set",False) else "NEUTRAL"),
        ("38. Speed is the essence of trading — enter and exit without hesitation", lambda e: "PRO" if e.get("energy",50) > 60 and e.get("entry_trigger",False) else "NEUTRAL"),
        ("39. At first, be like a maiden — patient, waiting for the perfect setup", lambda e: "PRO" if e.get("patience",5) > 7 else "NEUTRAL"),
        ("40. Then be like a hare — swift in execution when the signal appears", lambda e: "PRO" if e.get("energy",50) > 70 and e.get("entry_trigger",False) else "NEUTRAL"),
        ("41. The trader must be calm and composed under pressure", lambda e: "PRO" if e.get("manager_quality",5) > 7 else "NEUTRAL"),
        ("42. Keep your plans private — do not let the market know your stops", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("43. Drive your trades by logic, not by emotion", lambda e: "PRO" if e.get("discipline",5) > 6 else "NEUTRAL"),
        ("44. By changing strategies as the market changes, you keep losses small", lambda e: "PRO" if e.get("formation_changes",0) > 1 else "NEUTRAL"),
        ("45. The trader who masters all nine situations will survive any market", lambda e: "PRO" if e.get("intelligence",5) > 7 and e.get("discipline",5) > 7 else "NEUTRAL"),
    ]