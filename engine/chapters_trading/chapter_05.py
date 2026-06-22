"""Shadow - Chapter 5: Energy (Trading Version)
Complete. Every principle. Every strategy. Every idea."""

def CHAPTER_5_RULES():
    return [
        # ═══════════════════════════════════════════════
        # THE CONTROL OF CAPITAL
        # ═══════════════════════════════════════════════
        ("1. Managing a large account is the same principle as managing a small one", lambda e: "PRO" if e.get("organization",5) > 6 else "NEUTRAL"),
        ("2. It is merely a question of proper position sizing", lambda e: "PRO" if e.get("position_size",0) < 15 else "NEUTRAL"),
        ("3. Trading with full capital is no different from trading with partial capital", lambda e: "PRO" if e.get("manager_quality",5) > 6 else "NEUTRAL"),
        ("4. It is merely a question of discipline and signals", lambda e: "PRO" if e.get("discipline",5) > 6 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # DIRECT AND INDIRECT TRADING
        # ═══════════════════════════════════════════════
        ("5. In all trading, the direct method is trend following", lambda e: "PRO" if e.get("trend","") == "bullish" else "NEUTRAL"),
        ("6. But indirect methods — pullbacks, reversals — will secure larger profits", lambda e: "PRO" if e.get("counter_attack",0) > 0 and e.get("at_support",False) else "NEUTRAL"),
        ("7. Indirect entries, efficiently timed, are as inexhaustible as market cycles", lambda e: "PRO" if e.get("formation_changes",0) > 1 and e.get("counter_attack",0) > 0 else "NEUTRAL"),
        ("8. The direct and the indirect lead on to each other — trend and pullback", lambda e: "PRO" if e.get("trend_strength",0) > 0.5 and e.get("position_in_range",0) < 0.5 else "NEUTRAL"),
        ("9. It is like moving in a circle — trend, pullback, continuation", lambda e: "PRO" if e.get("formations",0) > 1 else "NEUTRAL"),
        ("10. Who can exhaust the combinations of entry strategies?", lambda e: "PRO" if e.get("intelligence",5) > 7 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # ENERGY AND MOMENTUM
        # ═══════════════════════════════════════════════
        ("11. The onset of a breakout is like the rush of a torrent", lambda e: "PRO" if e.get("momentum",0) > 2 and e.get("energy",50) > 70 else "NEUTRAL"),
        ("12. The energy of a trending market is as the momentum of a round stone rolled down a mountain", lambda e1,e2: "PRO" if e1.get("momentum",0) > e2.get("momentum",0)+1 else "CON" if e2.get("momentum",0) > e1.get("momentum",0)+1 else "NEUTRAL"),
        ("13. Energy is the force that drives price — it must be recognized and followed", lambda e: "PRO" if e.get("energy",50) > 60 and e.get("trend","") == "bullish" else "NEUTRAL"),
        ("14. The quality of a trade entry is like the well-timed strike of a falcon", lambda e: "PRO" if e.get("rsi",50) > 50 and e.get("rsi",50) < 70 else "NEUTRAL"),
        ("15. The falcon strikes at exactly the right moment — not too early, not too late", lambda e: "PRO" if e.get("momentum",0) > 1 and e.get("energy",50) > 65 and e.get("entry_trigger",False) else "NEUTRAL"),
        ("16. Timing is releasing your capital at the precise moment of maximum probability", lambda e: "PRO" if 45 < e.get("rsi",50) < 65 and e.get("momentum",0) > 0 else "NEUTRAL"),
        ("17. Enter too early and you suffer drawdown; too late and you chase", lambda e: "CON" if e.get("position_in_range",0) > 0.7 else "PRO" if e.get("position_in_range",0) < 0.3 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE USE OF COMBINED FORCES
        # ═══════════════════════════════════════════════
        ("18. The clever trader looks to the effect of combined confirmations", lambda e: "PRO" if e.get("tf_alignment",0) > 0.6 else "NEUTRAL"),
        ("19. Volume confirming price, RSI confirming momentum, structure confirming direction", lambda e: "PRO" if e.get("volume_avg",0) > 300000 and e.get("trend_strength",0) > 0.5 else "NEUTRAL"),
        ("20. They do not rely on a single indicator alone", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("21. When combined forces align, the trade becomes like rolling logs down a mountain", lambda e: "PRO" if e.get("tf_alignment",0) > 0.7 and e.get("energy",50) > 60 else "NEUTRAL"),
        ("22. The weight of multiple confirmations is unstoppable once set in motion", lambda e: "PRO" if e.get("trend_strength",0) > 0.7 and e.get("momentum",0) > 1 else "NEUTRAL"),
        ("23. Multi-timeframe alignment is the combined energy of the market", lambda e: "PRO" if e.get("tf_alignment",0) > 0.7 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE TRADER'S MASTERY OF ENERGY
        # ═══════════════════════════════════════════════
        ("24. Thus the energy of one skilled in trading is overwhelming when deployed correctly", lambda e: "PRO" if e.get("energy",50) > 70 and e.get("form","").count("W") >= 3 else "NEUTRAL"),
        ("25. They select their setups carefully and combine confirmations", lambda e: "PRO" if e.get("manager_quality",5) > 6 and e.get("setup_quality",5) > 6 else "NEUTRAL"),
        ("26. He who can modify his strategy in relation to market conditions may be called consistently profitable", lambda e: "PRO" if e.get("formation_changes",0) > 1 and e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("27. The trader must read the flow of price and release capital at the decisive moment", lambda e: "PRO" if e.get("momentum",0) > 0 and e.get("energy",50) > 60 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("28. Hesitation at the moment of truth turns profit into loss", lambda e: "CON" if e.get("entry_trigger",False) and e.get("discipline",5) < 5 else "NEUTRAL"),
        ("29. Decisive action when the signal appears is the mark of the master trader", lambda e: "PRO" if e.get("entry_trigger",False) and e.get("discipline",5) > 7 else "NEUTRAL"),
    ]