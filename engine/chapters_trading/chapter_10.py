"""Shadow - Chapter 10: Terrain (Trading Version)
Complete. Every principle. Every strategy. Every idea.
Market structure. Support and resistance. The ground you trade on."""

def CHAPTER_10_RULES():
    return [
        # ═══════════════════════════════════════════════
        # THE SIX KINDS OF MARKET TERRAIN
        # ═══════════════════════════════════════════════
        ("1. Market structure may be classified: trending, ranging, volatile, quiet, breakout, and breakdown", lambda e: "PRO" if e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("2. Accessible ground (trending market): both buyers and sellers can move freely — trade with the trend", lambda e: "PRO" if e.get("trend_strength",0) > 0.5 else "NEUTRAL"),
        ("3. In a trending market, be first to enter on pullbacks and ride the wave", lambda e: "PRO" if e.get("position_in_range",0) < 0.4 and e.get("trend","") == "bullish" else "NEUTRAL"),
        ("4. Entangling ground (ranging market): easy to enter, hard to exit with profit — trade only the edges", lambda e: "PRO" if e.get("at_support",False) and e.get("trend","") == "neutral" else "CON" if e.get("at_resistance",False) and e.get("trend","") == "neutral" else "NEUTRAL"),
        ("5. If the market is ranging and you are not at an edge, do not enter", lambda e: "CON" if e.get("trend","") == "neutral" and 0.3 < e.get("position_in_range",0) < 0.7 else "NEUTRAL"),
        ("6. Temporizing ground (consolidation): neither side should move first — wait for the breakout", lambda e: "PRO" if e.get("patience",5) > 6 and e.get("volatility",0) < e.get("price",0)*0.01 else "NEUTRAL"),
        ("7. Narrow passes (key levels): occupy support first and defend it — if resistance holds, do not buy", lambda e: "PRO" if e.get("at_support",False) else "CON" if e.get("at_resistance",False) else "NEUTRAL"),
        ("8. Steep heights (overbought/oversold): occupy the value zone and wait — do not chase extremes", lambda e: "PRO" if e.get("position_in_range",0) < 0.3 and e.get("rsi",50) < 40 else "CON" if e.get("position_in_range",0) > 0.7 and e.get("rsi",50) > 60 else "NEUTRAL"),
        ("9. Great distance from value (extended price): if momentum is equal, do not chase — wait for mean reversion", lambda e: "CON" if e.get("position_in_range",0) > 0.75 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE SIX WAYS TO COURT LOSSES
        # ═══════════════════════════════════════════════
        ("10. Flight: when your capital is sufficient but your discipline is weak — you exit winning trades too early", lambda e: "CON" if e.get("manager_quality",5) < 4 and e.get("squad_depth",0) > 15 else "NEUTRAL"),
        ("11. Insubordination: when your strategy is sound but your emotions override it", lambda e: "CON" if e.get("discipline",5) < 4 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("12. Collapse: when your analysis is correct but your execution is poor", lambda e: "CON" if e.get("discipline",5) > 7 and e.get("setup_quality",5) < 4 else "NEUTRAL"),
        ("13. Ruin: when frustration leads to revenge trading after a loss", lambda e: "CON" if e.get("manager_quality",5) < 5 and e.get("discipline",5) < 5 else "NEUTRAL"),
        ("14. Disorganization: when the trader has no plan and trades randomly", lambda e: "CON" if e.get("manager_quality",5) < 4 and e.get("organization",5) < 4 else "NEUTRAL"),
        ("15. Rout: when the trader fails to assess the market's true strength and is run over", lambda e: "CON" if e.get("intelligence",5) < 4 and e.get("preparation",5) < 4 else "NEUTRAL"),
        ("16. These six are the ways to court trading losses — the trader must study them carefully", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE TRADER AND MARKET STRUCTURE
        # ═══════════════════════════════════════════════
        ("17. Market structure is the trader's best ally — know it intimately", lambda e: "PRO" if e.get("earth_score",5) > 6 else "NEUTRAL"),
        ("18. Understanding the market's structure, controlling risk, and calculating probabilities — this is the mark of a great trader", lambda e: "PRO" if e.get("manager_quality",5) > 7 and e.get("intelligence",5) > 7 else "NEUTRAL"),
        ("19. He who knows structure and trades accordingly will profit", lambda e: "PRO" if e.get("intelligence",5) > 6 and e.get("preparation",5) > 6 else "NEUTRAL"),
        ("20. He who knows it not, nor trades accordingly, will surely lose", lambda e: "CON" if e.get("intelligence",5) < 4 else "NEUTRAL"),
        ("21. If the setup is certain to profit, you must trade — even against your fear", lambda e: "PRO" if e.get("setup_quality",5) > 7 and e.get("manager_quality",5) > 7 else "NEUTRAL"),
        ("22. If the setup is not likely to profit, you must not trade — even if you feel greedy", lambda e: "CON" if e.get("setup_quality",5) < 3 else "NEUTRAL"),
        ("23. The trader who enters without seeking glory and exits without fearing loss", lambda e: "PRO" if e.get("manager_quality",5) > 7 and e.get("discipline",5) > 6 else "NEUTRAL"),
        ("24. Whose only thought is to protect capital and follow their plan", lambda e: "PRO" if e.get("team_harmony",5) > 6 and e.get("discipline",5) > 6 else "NEUTRAL"),
        ("25. They are the jewel of the trading profession", lambda e: "PRO" if e.get("manager_quality",5) > 8 else "NEUTRAL"),
        ("26. Regard your capital as your children and you will protect it fiercely", lambda e: "PRO" if e.get("capital_risk",5) < 4 else "NEUTRAL"),
        ("27. Look upon your account as your own lifeblood and you will trade with care", lambda e: "PRO" if e.get("risk_management",5) > 7 else "NEUTRAL"),
        ("28. If you are lenient with your rules but unable to enforce them", lambda e: "CON" if e.get("discipline",5) < 4 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("29. Your trading will be like spoiled children — useless for consistent profit", lambda e: "CON" if e.get("discipline",5) < 3 else "NEUTRAL"),
        ("30. If you know the setup can work but do not know the market is at resistance", lambda e: "CON" if e.get("preparation",5) > 6 and e.get("intelligence",5) < 4 else "NEUTRAL"),
        ("31. If you know the market is at support but do not know your capital cannot withstand the drawdown", lambda e: "CON" if e.get("intelligence",5) > 5 and e.get("capital_risk",5) > 6 else "NEUTRAL"),
        ("32. If you know both the market and yourself, profit will be assured", lambda e: "PRO" if e.get("intelligence",5) > 6 and e.get("discipline",5) > 6 else "NEUTRAL"),
        ("33. Know the market structure, know your own psychology, and your success will not be threatened", lambda e: "PRO" if e.get("intelligence",5) > 7 and e.get("manager_quality",5) > 7 else "NEUTRAL"),
        ("34. Know the trend, know the levels, and your victory will be complete", lambda e: "PRO" if e.get("trend_strength",0) > 0.5 and e.get("earth_score",5) > 6 else "NEUTRAL"),
    ]