"""Shadow - Chapter 7: Maneuvering (Trading Version)
Complete. Every principle. Every strategy. Every idea.
The art of positioning and navigating market conditions."""

def CHAPTER_7_RULES():
    return [
        # ═══════════════════════════════════════════════
        # THE DIFFICULTY OF MARKET MANEUVERING
        # ═══════════════════════════════════════════════
        ("1. The trader receives their strategy from their discipline", lambda e: "PRO" if e.get("manager_quality",5) > 6 else "NEUTRAL"),
        ("2. Having gathered capital and concentrated focus, they must harmonize their approach with the market", lambda e: "PRO" if e.get("team_harmony",5) > 6 and e.get("organization",5) > 5 else "NEUTRAL"),
        ("3. After that comes tactical maneuvering — entries, stops, targets — and nothing is more difficult", lambda e: "PRO" if e.get("formation_changes",0) > 1 else "NEUTRAL"),
        ("4. The difficulty of maneuvering consists in turning a losing position into a lesson", lambda e: "PRO" if e.get("counter_attack",0) > 0 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("5. And turning market uncertainty into calculated risk", lambda e: "PRO" if e.get("comeback_wins",0) > 1 else "NEUTRAL"),
        ("6. To wait for a deep pullback while others chase the breakout", lambda e: "PRO" if e.get("patience",5) > 7 and e.get("position_in_range",0) < 0.3 else "NEUTRAL"),
        ("7. And though entering later, to capture the larger move by buying at better prices", lambda e: "PRO" if e.get("at_support",False) and e.get("trend","") == "bullish" else "NEUTRAL"),
        ("8. This shows knowledge of the art of timing and patience", lambda e: "PRO" if e.get("intelligence",5) > 6 and e.get("patience",5) > 6 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE DANGERS OF POOR EXECUTION
        # ═══════════════════════════════════════════════
        ("9. Trading with a plan is profitable — trading without one is most dangerous", lambda e: "CON" if e.get("discipline",5) < 5 else "PRO" if e.get("discipline",5) > 7 else "NEUTRAL"),
        ("10. An entire account can be robbed of its capital if the trader is not careful", lambda e: "CON" if e.get("morale",5) < 5 and e.get("manager_quality",5) < 5 else "NEUTRAL"),
        ("11. The strongest conviction will be exhausted by a series of bad entries", lambda e: "CON" if e.get("energy",50) < 40 and e.get("squad_depth",0) < 18 else "NEUTRAL"),
        ("12. If you chase a move fifty pips away, only half your edge will remain", lambda e: "CON" if e.get("position_in_range",0) > 0.7 else "NEUTRAL"),
        ("13. If you enter at a fair price, most of your edge is preserved", lambda e: "PRO" if e.get("position_in_range",0) < 0.5 else "NEUTRAL"),
        ("14. An account without proper risk management is lost", lambda e: "CON" if e.get("capital_risk",5) > 6 else "NEUTRAL"),
        ("15. Without stop losses it is lost", lambda e: "CON" if not e.get("stop_loss_set",False) else "NEUTRAL"),
        ("16. Without a trading plan it is lost", lambda e: "CON" if e.get("preparation",5) < 4 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # KNOWLEDGE OF THE MARKET
        # ═══════════════════════════════════════════════
        ("17. We cannot trade correlated assets without understanding their relationships", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("18. We are not fit to enter a trade unless we understand the market structure", lambda e: "PRO" if e.get("intelligence",5) > 5 and e.get("earth_score",5) > 5 else "NEUTRAL"),
        ("19. Its support and resistance, its volatility patterns, its typical behavior", lambda e: "PRO" if e.get("preparation",5) > 6 else "NEUTRAL"),
        ("20. We cannot turn market conditions to our advantage without understanding them first", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("21. Knowledge of the asset you trade is worth more than any indicator", lambda e: "PRO" if e.get("intelligence",5) > 7 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # DECEPTION IN MANEUVERING
        # ═══════════════════════════════════════════════
        ("22. In trading, practice patience and you will find the best entries", lambda e: "PRO" if e.get("patience",5) > 6 else "NEUTRAL"),
        ("23. Enter only if there is a real edge to be captured", lambda e: "PRO" if e.get("setup_quality",5) > 6 else "NEUTRAL"),
        ("24. Whether to scale in or enter fully must be decided by market conditions", lambda e: "PRO" if e.get("formation_changes",0) > 1 else "NEUTRAL"),
        ("25. Let your entry be as swift as the wind", lambda e: "PRO" if e.get("energy",50) > 60 and e.get("entry_trigger",False) else "NEUTRAL"),
        ("26. Your stop loss as immovable as a mountain", lambda e: "PRO" if e.get("stop_loss_set",False) and e.get("discipline",5) > 7 else "NEUTRAL"),
        ("27. Your profit-taking like fire consuming the trend", lambda e: "PRO" if e.get("take_profit_pct",0) > 2 and e.get("energy",50) > 60 else "NEUTRAL"),
        ("28. Your patience in waiting as deep as the ocean", lambda e: "PRO" if e.get("patience",5) > 8 else "NEUTRAL"),
        ("29. Your execution like a thunderbolt — instant and decisive", lambda e: "PRO" if e.get("momentum",0) > 1 and e.get("entry_trigger",False) else "NEUTRAL"),
        ("30. When you capture profit, let it compound for future trades", lambda e: "PRO" if e.get("profit_factor",0) > 1 else "NEUTRAL"),
        ("31. When you enter new territory, do so with reduced size", lambda e: "PRO" if e.get("position_size",0) < 10 and e.get("played",0) < 20 else "NEUTRAL"),
        ("32. Ponder and deliberate before every trade", lambda e: "PRO" if e.get("preparation",5) > 6 else "NEUTRAL"),
        ("33. He will profit who has learned the art of timing entries", lambda e: "PRO" if e.get("position_in_range",0) < 0.4 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("34. Such is the art of maneuvering in the markets", lambda e: "PRO" if e.get("formation_changes",0) > 1 and e.get("intelligence",5) > 5 else "NEUTRAL"),
    ]"""Shadow - Chapter 7: Maneuvering (Trading Version)
Complete. Every principle. Every strategy. Every idea.
The art of positioning and navigating market conditions."""

def CHAPTER_7_RULES():
    return [
        # ═══════════════════════════════════════════════
        # THE DIFFICULTY OF MARKET MANEUVERING
        # ═══════════════════════════════════════════════
        ("1. The trader receives their strategy from their discipline", lambda e: "PRO" if e.get("manager_quality",5) > 6 else "NEUTRAL"),
        ("2. Having gathered capital and concentrated focus, they must harmonize their approach with the market", lambda e: "PRO" if e.get("team_harmony",5) > 6 and e.get("organization",5) > 5 else "NEUTRAL"),
        ("3. After that comes tactical maneuvering — entries, stops, targets — and nothing is more difficult", lambda e: "PRO" if e.get("formation_changes",0) > 1 else "NEUTRAL"),
        ("4. The difficulty of maneuvering consists in turning a losing position into a lesson", lambda e: "PRO" if e.get("counter_attack",0) > 0 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("5. And turning market uncertainty into calculated risk", lambda e: "PRO" if e.get("comeback_wins",0) > 1 else "NEUTRAL"),
        ("6. To wait for a deep pullback while others chase the breakout", lambda e: "PRO" if e.get("patience",5) > 7 and e.get("position_in_range",0) < 0.3 else "NEUTRAL"),
        ("7. And though entering later, to capture the larger move by buying at better prices", lambda e: "PRO" if e.get("at_support",False) and e.get("trend","") == "bullish" else "NEUTRAL"),
        ("8. This shows knowledge of the art of timing and patience", lambda e: "PRO" if e.get("intelligence",5) > 6 and e.get("patience",5) > 6 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE DANGERS OF POOR EXECUTION
        # ═══════════════════════════════════════════════
        ("9. Trading with a plan is profitable — trading without one is most dangerous", lambda e: "CON" if e.get("discipline",5) < 5 else "PRO" if e.get("discipline",5) > 7 else "NEUTRAL"),
        ("10. An entire account can be robbed of its capital if the trader is not careful", lambda e: "CON" if e.get("morale",5) < 5 and e.get("manager_quality",5) < 5 else "NEUTRAL"),
        ("11. The strongest conviction will be exhausted by a series of bad entries", lambda e: "CON" if e.get("energy",50) < 40 and e.get("squad_depth",0) < 18 else "NEUTRAL"),
        ("12. If you chase a move fifty pips away, only half your edge will remain", lambda e: "CON" if e.get("position_in_range",0) > 0.7 else "NEUTRAL"),
        ("13. If you enter at a fair price, most of your edge is preserved", lambda e: "PRO" if e.get("position_in_range",0) < 0.5 else "NEUTRAL"),
        ("14. An account without proper risk management is lost", lambda e: "CON" if e.get("capital_risk",5) > 6 else "NEUTRAL"),
        ("15. Without stop losses it is lost", lambda e: "CON" if not e.get("stop_loss_set",False) else "NEUTRAL"),
        ("16. Without a trading plan it is lost", lambda e: "CON" if e.get("preparation",5) < 4 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # KNOWLEDGE OF THE MARKET
        # ═══════════════════════════════════════════════
        ("17. We cannot trade correlated assets without understanding their relationships", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("18. We are not fit to enter a trade unless we understand the market structure", lambda e: "PRO" if e.get("intelligence",5) > 5 and e.get("earth_score",5) > 5 else "NEUTRAL"),
        ("19. Its support and resistance, its volatility patterns, its typical behavior", lambda e: "PRO" if e.get("preparation",5) > 6 else "NEUTRAL"),
        ("20. We cannot turn market conditions to our advantage without understanding them first", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("21. Knowledge of the asset you trade is worth more than any indicator", lambda e: "PRO" if e.get("intelligence",5) > 7 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # DECEPTION IN MANEUVERING
        # ═══════════════════════════════════════════════
        ("22. In trading, practice patience and you will find the best entries", lambda e: "PRO" if e.get("patience",5) > 6 else "NEUTRAL"),
        ("23. Enter only if there is a real edge to be captured", lambda e: "PRO" if e.get("setup_quality",5) > 6 else "NEUTRAL"),
        ("24. Whether to scale in or enter fully must be decided by market conditions", lambda e: "PRO" if e.get("formation_changes",0) > 1 else "NEUTRAL"),
        ("25. Let your entry be as swift as the wind", lambda e: "PRO" if e.get("energy",50) > 60 and e.get("entry_trigger",False) else "NEUTRAL"),
        ("26. Your stop loss as immovable as a mountain", lambda e: "PRO" if e.get("stop_loss_set",False) and e.get("discipline",5) > 7 else "NEUTRAL"),
        ("27. Your profit-taking like fire consuming the trend", lambda e: "PRO" if e.get("take_profit_pct",0) > 2 and e.get("energy",50) > 60 else "NEUTRAL"),
        ("28. Your patience in waiting as deep as the ocean", lambda e: "PRO" if e.get("patience",5) > 8 else "NEUTRAL"),
        ("29. Your execution like a thunderbolt — instant and decisive", lambda e: "PRO" if e.get("momentum",0) > 1 and e.get("entry_trigger",False) else "NEUTRAL"),
        ("30. When you capture profit, let it compound for future trades", lambda e: "PRO" if e.get("profit_factor",0) > 1 else "NEUTRAL"),
        ("31. When you enter new territory, do so with reduced size", lambda e: "PRO" if e.get("position_size",0) < 10 and e.get("played",0) < 20 else "NEUTRAL"),
        ("32. Ponder and deliberate before every trade", lambda e: "PRO" if e.get("preparation",5) > 6 else "NEUTRAL"),
        ("33. He will profit who has learned the art of timing entries", lambda e: "PRO" if e.get("position_in_range",0) < 0.4 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("34. Such is the art of maneuvering in the markets", lambda e: "PRO" if e.get("formation_changes",0) > 1 and e.get("intelligence",5) > 5 else "NEUTRAL"),
    ]