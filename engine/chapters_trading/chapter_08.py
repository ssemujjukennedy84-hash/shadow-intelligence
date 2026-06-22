"""Shadow - Chapter 8: Variation in Tactics (Trading Version)
Complete. Every principle. Every strategy. Every idea.
Adaptability and the five dangerous faults of a trader."""

def CHAPTER_8_RULES():
    return [
        # ═══════════════════════════════════════════════
        # THE NEED FOR FLEXIBILITY
        # ═══════════════════════════════════════════════
        ("1. The trader receives their strategy, gathers capital, and focuses their mind", lambda e: "PRO" if e.get("manager_quality",5) > 5 and e.get("organization",5) > 5 else "NEUTRAL"),
        ("2. When the market is highly volatile, do not commit large size", lambda e: "CON" if e.get("volatility",0) > e.get("price",0)*0.03 else "NEUTRAL"),
        ("3. When trends intersect and align, trade with confidence", lambda e: "PRO" if e.get("tf_alignment",0) > 0.7 else "NEUTRAL"),
        ("4. Do not linger in trades that have invalidated their setup", lambda e: "CON" if e.get("lead_lost",0) > 0 else "NEUTRAL"),
        ("5. In ranging markets, you must use different tactics than in trending markets", lambda e: "PRO" if e.get("formation_changes",0) > 1 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("6. In a desperate drawdown, you must protect capital above all", lambda e: "PRO" if e.get("drawdown",0) > 15 and e.get("discipline",5) > 6 else "NEUTRAL"),
        ("7. There are setups which must not be traded", lambda e: "CON" if e.get("setup_quality",5) < 3 else "NEUTRAL"),
        ("8. There are market conditions which must not be challenged", lambda e: "CON" if e.get("trend_strength",0) < 0.3 and e.get("trend","") == "bearish" else "NEUTRAL"),
        ("9. There are levels which must not be fought against", lambda e: "CON" if e.get("at_resistance",False) and e.get("momentum",0) < 1 else "NEUTRAL"),
        ("10. There are drawdown limits which must not be exceeded", lambda e: "CON" if e.get("drawdown",0) > 20 else "NEUTRAL"),
        ("11. There are rules of your strategy which must not be broken", lambda e: "PRO" if e.get("discipline",5) > 7 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE TRADER WHO UNDERSTANDS VARIATION
        # ═══════════════════════════════════════════════
        ("12. The trader who thoroughly understands the advantages of varying tactics knows how to handle any market", lambda e: "PRO" if e.get("formation_changes",0) > 2 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("13. The trader who does not understand this may know the patterns well", lambda e: "CON" if e.get("formation_changes",0) < 1 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("14. Yet they will not be able to turn knowledge into consistent profit", lambda e: "CON" if e.get("intelligence",5) > 5 and e.get("form","").count("L") >= 2 else "NEUTRAL"),
        ("15. The student of trading who cannot vary their approach will fail to preserve capital", lambda e: "CON" if e.get("formation_changes",0) < 1 and e.get("squad_depth",0) > 15 else "NEUTRAL"),
        ("16. A strategy that never adapts is a strategy that will eventually break", lambda e: "CON" if e.get("formation_changes",0) < 1 and e.get("played",0) > 30 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE FIVE DANGEROUS FAULTS OF A TRADER
        # ═══════════════════════════════════════════════
        ("17. There are five dangerous faults which may destroy a trader", lambda e: "CON" if e.get("manager_quality",5) < 6 else "NEUTRAL"),
        ("18. RECKLESSNESS: overtrading and sizing too large, which leads to ruin", lambda e: "CON" if e.get("position_size",0) > 20 else "NEUTRAL"),
        ("19. COWARDICE: refusing to enter when the perfect setup appears, which leads to missed opportunity", lambda e: "CON" if e.get("entry_trigger",False) and e.get("discipline",5) < 5 else "NEUTRAL"),
        ("20. A HASTY TEMPER: entering trades out of anger or revenge after a loss", lambda e: "CON" if e.get("discipline",5) < 4 else "NEUTRAL"),
        ("21. A DELICACY OF HONOR: refusing to admit a trade is wrong and holding losers too long", lambda e: "CON" if e.get("lead_lost",0) > 1 else "NEUTRAL"),
        ("22. OVER-SOLICITUDE: worrying excessively about every tick, which leads to premature exits", lambda e: "CON" if e.get("take_profit_pct",0) < 1 and e.get("setup_quality",5) > 5 else "NEUTRAL"),
        ("23. These five faults are the most dangerous for a trader", lambda e: "CON" if e.get("discipline",5) < 5 and e.get("manager_quality",5) < 5 else "NEUTRAL"),
        ("24. When an account is blown, the cause will surely be found among these five", lambda e: "CON" if e.get("drawdown",0) > 30 else "NEUTRAL"),
        ("25. Let them be a subject of daily meditation for every trader", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # ADAPTING TO MARKET CIRCUMSTANCES
        # ═══════════════════════════════════════════════
        ("26. The wise trader considers both favorable and unfavorable scenarios before entry", lambda e: "PRO" if e.get("intelligence",5) > 6 and e.get("preparation",5) > 6 else "NEUTRAL"),
        ("27. In the midst of a losing streak, they see the opportunity to refine their strategy", lambda e: "PRO" if e.get("comeback_wins",0) > 1 else "NEUTRAL"),
        ("28. In the midst of a winning streak, they see the danger of overconfidence", lambda e: "PRO" if e.get("discipline",5) > 6 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("29. Reduce your exposure when the market is hostile", lambda e: "PRO" if e.get("position_size",0) < 8 and e.get("trend_strength",0) < 0.4 else "NEUTRAL"),
        ("30. Increase your exposure when the market is favorable", lambda e: "PRO" if e.get("position_size",0) > 5 and e.get("tf_alignment",0) > 0.7 else "NEUTRAL"),
        ("31. Keep the market constantly uncertain of your next move by not being predictable", lambda e: "PRO" if e.get("counter_attack",0) > 1 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("32. Hold out the allure of your limit orders and let the market come to you", lambda e: "PRO" if e.get("patience",5) > 7 else "NEUTRAL"),
        ("33. The trader who masters variation masters their own psychology", lambda e: "PRO" if e.get("formation_changes",0) > 2 and e.get("discipline",5) > 6 else "NEUTRAL"),
    ]