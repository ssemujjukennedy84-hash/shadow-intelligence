"""Shadow - Chapter 4: Tactical Dispositions (Trading Version)
Complete. Every principle. Every strategy. Every idea."""

def CHAPTER_4_RULES():
    return [
        # ═══════════════════════════════════════════════
        # INVINCIBILITY THROUGH DEFENSE
        # ═══════════════════════════════════════════════
        ("1. The good traders of old first put themselves beyond the possibility of ruin", lambda e: "PRO" if e.get("stop_loss_set",False) else "CON" if not e.get("stop_loss_set",False) else "NEUTRAL"),
        ("2. Then waited for an opportunity to profit", lambda e: "PRO" if e.get("patience",5) > 6 and e.get("entry_trigger",False) else "NEUTRAL"),
        ("3. To secure yourself against loss lies in your own hands", lambda e: "PRO" if e.get("discipline",5) > 6 and e.get("preparation",5) > 6 else "NEUTRAL"),
        ("4. But the opportunity to profit is provided by the market itself", lambda e: "PRO" if e.get("setup_quality",5) > 5 else "NEUTRAL"),
        ("5. The good trader is able to secure against large losses", lambda e: "PRO" if e.get("drawdown",0) < 10 else "CON" if e.get("drawdown",0) > 20 else "NEUTRAL"),
        ("6. But cannot make certain of profits on any single trade", lambda e: "NEUTRAL"),
        ("7. Therefore the wise trader risks small and aims for larger rewards", lambda e: "PRO" if e.get("rr_ratio",0) > 2 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # DEFENSE AND ATTACK IN TRADING
        # ═══════════════════════════════════════════════
        ("8. Invincibility lies in defense — protect your capital first", lambda e: "PRO" if e.get("capital_risk",5) < 4 else "CON" if e.get("capital_risk",5) > 6 else "NEUTRAL"),
        ("9. The possibility of profit lies in attack — when the setup is clear", lambda e: "PRO" if e.get("setup_quality",5) > 6 and e.get("entry_trigger",False) else "NEUTRAL"),
        ("10. When you defend, it is because market conditions are unfavorable", lambda e: "CON" if e.get("trend_strength",0) < 0.4 else "NEUTRAL"),
        ("11. When you attack, it is because the probability is in your favor", lambda e: "PRO" if e.get("trend_strength",0) > 0.6 and e.get("setup_quality",5) > 6 else "NEUTRAL"),
        ("12. The trader skilled in defense stays in cash during high volatility", lambda e: "PRO" if e.get("volatility",0) > e.get("price",0)*0.02 else "NEUTRAL"),
        ("13. The trader skilled in attack strikes when momentum confirms", lambda e: "PRO" if e.get("momentum",0) > 1 and e.get("energy",50) > 70 else "NEUTRAL"),
        ("14. Defense is holding your position size small in uncertain markets", lambda e: "PRO" if e.get("position_size",0) < 5 and e.get("trend","") == "neutral" else "NEUTRAL"),
        ("15. Attack is sizing up when all timeframes align", lambda e: "PRO" if e.get("tf_alignment",0) > 0.7 and e.get("position_size",0) > 5 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # SEEING WHAT OTHERS CANNOT
        # ═══════════════════════════════════════════════
        ("16. To see a setup only when it is obvious to everyone is not the mark of a great trader", lambda e: "PRO" if e.get("intelligence",5) > 7 else "NEUTRAL"),
        ("17. Entering before the crowd requires seeing what they cannot", lambda e: "PRO" if e.get("intelligence",5) > 6 and e.get("position_in_range",0) < 0.3 else "NEUTRAL"),
        ("18. What the ancients called a clever trader is one who not only profits but profits with ease", lambda e: "PRO" if e.get("form","").count("W") >= 4 and e.get("drawdown",0) < 10 else "NEUTRAL"),
        ("19. Their wins bring them neither excessive excitement nor overconfidence", lambda e: "PRO" if e.get("discipline",5) > 7 and e.get("intelligence",5) > 7 else "NEUTRAL"),
        ("20. They profit by making few mistakes, not by being right every time", lambda e: "PRO" if e.get("discipline",5) > 7 and e.get("losses",0) < 3 else "NEUTRAL"),
        ("21. Making few mistakes is what establishes consistent profitability", lambda e: "PRO" if e.get("preparation",5) > 6 and e.get("discipline",5) > 6 else "NEUTRAL"),
        ("22. A 60% win rate with 2:1 risk/reward is superior to 90% with 1:2", lambda e: "PRO" if e.get("rr_ratio",0) > 1.5 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE STRATEGIC POSITION
        # ═══════════════════════════════════════════════
        ("23. The victorious trader first ensures conditions are right, then enters", lambda e: "PRO" if e.get("intelligence",5) > 6 and e.get("preparation",5) > 6 else "NEUTRAL"),
        ("24. The defeated trader enters first, then hopes conditions improve", lambda e: "CON" if e.get("preparation",5) < 5 and e.get("energy",50) > 60 else "NEUTRAL"),
        ("25. The skilled trader cultivates discipline and preserves their method", lambda e: "PRO" if e.get("discipline",5) > 6 and e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("26. Thus they are the master of their own trading fate", lambda e: "PRO" if e.get("manager_quality",5) > 7 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE FIVE ELEMENTS OF TRADE MANAGEMENT
        # ═══════════════════════════════════════════════
        ("27. Measurement: knowing your risk before every trade", lambda e: "PRO" if e.get("capital_risk",5) < 5 else "NEUTRAL"),
        ("28. Estimation: calculating position size based on account size", lambda e: "PRO" if e.get("position_size",0) < 15 else "NEUTRAL"),
        ("29. Calculation: determining the probability of success", lambda e: "PRO" if e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("30. Balancing: weighing risk against potential reward", lambda e: "PRO" if e.get("rr_ratio",0) > 1.5 else "NEUTRAL"),
        ("31. Victory: the trade that follows all these steps", lambda e: "PRO" if e.get("preparation",5) > 6 and e.get("setup_quality",5) > 6 else "NEUTRAL"),
        ("32. A winning trade is like a heavy weight placed against a feather", lambda e: "PRO" if e.get("momentum",0) > 2 and e.get("trend_strength",0) > 0.7 else "NEUTRAL"),
        ("33. The onrush of a profitable trade is like pent-up waters bursting through a dam", lambda e: "PRO" if e.get("momentum",0) > 2 and e.get("energy",50) > 70 else "NEUTRAL"),
    ]