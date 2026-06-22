"""Shadow - Chapter 1: Laying Plans (Trading Version)
Complete. Every principle. Every strategy. Every idea."""

def CHAPTER_1_RULES():
    return [
        # ═══════════════════════════════════════════════
        # OPENING: THE IMPORTANCE OF TRADING STRATEGY
        # ═══════════════════════════════════════════════
        ("1. The art of trading is of vital importance to your capital", lambda e: "PRO" if e.get("capital_risk",5) < 3 else "CON" if e.get("capital_risk",5) > 7 else "NEUTRAL"),
        ("2. It is a matter of financial life and death", lambda e: "PRO" if e.get("risk_management",5) > 6 else "CON" if e.get("risk_management",5) < 3 else "NEUTRAL"),
        ("3. A road either to wealth or to ruin", lambda e: "CON" if e.get("drawdown",0) > 25 else "NEUTRAL"),
        ("4. Trading is a subject of inquiry which can on no account be neglected", lambda e: "PRO" if e.get("preparation",5) > 6 else "CON" if e.get("preparation",5) < 3 else "NEUTRAL"),
        ("5. The unprepared trader will be destroyed by the prepared market", lambda e: "CON" if e.get("preparation",5) < 4 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE FIVE CONSTANT FACTORS OF TRADING
        # ═══════════════════════════════════════════════
        ("6. Trading is governed by five constant factors", lambda e1,e2: "PRO" if e1.get("five_score",5) > e2.get("five_score",5)+2 else "CON" if e2.get("five_score",5) > e1.get("five_score",5)+2 else "NEUTRAL"),
        ("7. These must be taken into account in every trade decision", lambda e: "PRO" if e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("8. When seeking to determine market conditions for entry", lambda e: "PRO" if e.get("preparation",5) > 5 else "NEUTRAL"),
        
        # (1) THE MORAL LAW = TREND ALIGNMENT
        ("9. The Moral Law causes the trader to be in complete accord with the trend", lambda e: "PRO" if e.get("trend","") == "bullish" else "CON" if e.get("trend","") == "bearish" else "NEUTRAL"),
        ("10. Follow the trend regardless of fear or doubt", lambda e: "PRO" if e.get("trend_strength",0) > 0.6 and e.get("morale",5) > 6 else "NEUTRAL"),
        ("11. Undismayed by any temporary pullback or drawdown", lambda e: "PRO" if e.get("comeback_wins",0) > 0 and e.get("trend","") == "bullish" else "NEUTRAL"),
        ("12. The Moral Law: unity of your strategy with market direction", lambda e: "PRO" if e.get("tf_alignment",0) > 0.6 else "CON" if e.get("tf_alignment",0) < 0.3 else "NEUTRAL"),
        ("13. Without trend alignment, the trader fights alone against the crowd", lambda e: "CON" if e.get("trend","") == "neutral" else "NEUTRAL"),
        
        # (2) HEAVEN = MARKET TIMING & CONDITIONS
        ("14. Heaven signifies the timing of entries and exits", lambda e: "PRO" if 45 < e.get("rsi",50) < 65 else "CON" if e.get("rsi",50) > 75 or e.get("rsi",50) < 25 else "NEUTRAL"),
        ("15. Heaven: night and day = bull and bear market cycles", lambda e: "PRO" if e.get("trend","") != "neutral" else "NEUTRAL"),
        ("16. Heaven: cold and heat = fear and greed extremes", lambda e: "CON" if e.get("rsi",50) > 80 or e.get("rsi",50) < 20 else "NEUTRAL"),
        ("17. Heaven: times and seasons = optimal trading sessions", lambda e: "PRO" if e.get("time_advantage",False) else "NEUTRAL"),
        ("18. Heaven includes favorable timing for entry", lambda e: "PRO" if e.get("entry_trigger",False) else "NEUTRAL"),
        ("19. The best trades come at the intersection of trend and timing", lambda e: "PRO" if e.get("trend_strength",0) > 0.5 and 40 < e.get("rsi",50) < 60 else "NEUTRAL"),
        ("20. Heaven determines when to trade and when to wait in cash", lambda e: "PRO" if e.get("patience",5) > 6 else "NEUTRAL"),
        
        # (3) EARTH = MARKET STRUCTURE & LEVELS
        ("21. Earth comprises the distance between support and resistance", lambda e: "PRO" if e.get("position_in_range",0) < 0.3 else "CON" if e.get("position_in_range",0) > 0.7 else "NEUTRAL"),
        ("22. Earth: danger and security = where you place your stop loss", lambda e: "PRO" if e.get("stop_loss_set",False) else "CON" if not e.get("stop_loss_set",False) else "NEUTRAL"),
        ("23. Earth: open ground = trending market, narrow passes = consolidation", lambda e: "PRO" if e.get("trend","") != "neutral" else "NEUTRAL"),
        ("24. Earth: the chances of profit and loss depend on entry location", lambda e: "PRO" if e.get("position_in_range",0) < 0.35 else "CON" if e.get("position_in_range",0) > 0.65 else "NEUTRAL"),
        ("25. Earth: terrain advantage = buying at support, selling at resistance", lambda e: "PRO" if e.get("at_support",False) else "NEUTRAL"),
        ("26. Earth includes the altitude of price - is it high or low?", lambda e: "PRO" if e.get("position_in_range",0) < 0.4 else "NEUTRAL"),
        ("27. Know the terrain or your capital will be lost in it", lambda e: "PRO" if e.get("earth_score",5) > 5 else "CON" if e.get("earth_score",5) < 3 else "NEUTRAL"),
        
        # (4) THE COMMANDER = TRADER'S DISCIPLINE & PSYCHOLOGY
        ("28. The Commander stands for the virtue of wisdom in trading", lambda e: "PRO" if e.get("manager_quality",5) > 6 else "CON" if e.get("manager_quality",5) < 4 else "NEUTRAL"),
        ("29. Wisdom: knowing when NOT to trade is supreme wisdom", lambda e: "PRO" if e.get("patience",5) > 7 else "NEUTRAL"),
        ("30. Sincerity: sticking to your trading plan without deviation", lambda e: "PRO" if e.get("discipline",5) > 7 else "CON" if e.get("discipline",5) < 4 else "NEUTRAL"),
        ("31. Benevolence: protecting your capital as a shepherd protects the flock", lambda e: "PRO" if e.get("capital_risk",5) < 4 else "CON" if e.get("capital_risk",5) > 6 else "NEUTRAL"),
        ("32. Courage: executing the trade when the signal appears despite fear", lambda e: "PRO" if e.get("entry_trigger",False) and e.get("comeback_wins",0) > 0 else "NEUTRAL"),
        ("33. Strictness: cutting losses immediately without hesitation", lambda e: "PRO" if e.get("discipline",5) > 7 else "CON" if e.get("discipline",5) < 4 else "NEUTRAL"),
        ("34. A trader must possess all five virtues to be consistently profitable", lambda e: "PRO" if e.get("commander_score",5) > 7 else "NEUTRAL"),
        ("35. Without these virtues, the trader is doomed to fail", lambda e: "CON" if e.get("commander_score",5) < 4 else "NEUTRAL"),
        
        # (5) METHOD AND DISCIPLINE = RISK MANAGEMENT
        ("36. Method: the proper sizing of positions", lambda e: "PRO" if e.get("position_size",0) < 10 else "CON" if e.get("position_size",0) > 20 else "NEUTRAL"),
        ("37. Method: the maintenance of adequate capital reserves", lambda e: "PRO" if e.get("resources",0) > 60 else "CON" if e.get("resources",0) < 30 else "NEUTRAL"),
        ("38. Method: the control of risk per trade", lambda e: "PRO" if e.get("capital_risk",5) < 5 else "CON" if e.get("capital_risk",5) > 7 else "NEUTRAL"),
        ("39. Method: the organization of your trading journal and records", lambda e: "PRO" if e.get("organization",5) > 6 else "NEUTRAL"),
        ("40. Method: efficiency in execution wins consistently", lambda e: "PRO" if e.get("method_score",5) > 6 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE FIVE HEADS
        # ═══════════════════════════════════════════════
        ("41. These five heads should be familiar to every trader", lambda e: "PRO" if e.get("five_score",5) > 5 else "NEUTRAL"),
        ("42. He who knows them will be profitable", lambda e1,e2: "PRO" if e1.get("intelligence",5) > e2.get("intelligence",5)+1 else "CON" if e2.get("intelligence",5) > e1.get("intelligence",5)+1 else "NEUTRAL"),
        ("43. He who knows them not will lose money", lambda e: "CON" if e.get("intelligence",5) < 4 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE SEVEN CONSIDERATIONS FOR TRADING
        # ═══════════════════════════════════════════════
        ("44. Let the five heads be the basis of comparison between assets", lambda e: "PRO" if e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("45. C1: Which asset has the stronger trend (Moral Law)?", lambda e1,e2: "PRO" if e1.get("trend_strength",0) > e2.get("trend_strength",0)+0.2 else "CON" if e2.get("trend_strength",0) > e1.get("trend_strength",0)+0.2 else "NEUTRAL"),
        ("46. C2: Which setup has better timing (Heaven)?", lambda e1,e2: "PRO" if 45 < e1.get("rsi",50) < 65 and (e2.get("rsi",50) > 70 or e2.get("rsi",50) < 30) else "CON" if 45 < e2.get("rsi",50) < 65 and (e1.get("rsi",50) > 70 or e1.get("rsi",50) < 30) else "NEUTRAL"),
        ("47. C3: Which has the better structure - support/resistance (Earth)?", lambda e1,e2: "PRO" if e1.get("position_in_range",0) < 0.4 and e2.get("position_in_range",0) > 0.6 else "CON" if e2.get("position_in_range",0) < 0.4 and e1.get("position_in_range",0) > 0.6 else "NEUTRAL"),
        ("48. C4: Which trader has more discipline (Commander)?", lambda e1,e2: "PRO" if e1.get("discipline",5) > e2.get("discipline",5)+1 else "CON" if e2.get("discipline",5) > e1.get("discipline",5)+1 else "NEUTRAL"),
        ("49. C5: Which asset has stronger momentum (Strength)?", lambda e1,e2: "PRO" if e1.get("momentum",0) > e2.get("momentum",0)+1 else "CON" if e2.get("momentum",0) > e1.get("momentum",0)+1 else "NEUTRAL"),
        ("50. C6: Which has more volume confirmation (Training)?", lambda e1,e2: "PRO" if e1.get("volume_avg",0) > e2.get("volume_avg",0)*1.3 else "CON" if e2.get("volume_avg",0) > e1.get("volume_avg",0)*1.3 else "NEUTRAL"),
        ("51. C7: Which offers better risk/reward (Reward/Punishment)?", lambda e1,e2: "PRO" if e1.get("rr_ratio",0) > e2.get("rr_ratio",0)+0.5 else "CON" if e2.get("rr_ratio",0) > e1.get("rr_ratio",0)+0.5 else "NEUTRAL"),
        ("52. By means of these seven I can forecast profitable trades", lambda e1,e2: "PRO" if e1.get("seven_score",5) > e2.get("seven_score",5)+2 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # HEEDING THE STRATEGY
        # ═══════════════════════════════════════════════
        ("53. The trader who follows this strategy will profit", lambda e: "PRO" if e.get("discipline",5) > 6 else "NEUTRAL"),
        ("54. The trader who ignores it will lose", lambda e: "CON" if e.get("discipline",5) < 4 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # ALL TRADING IS BASED ON DECEPTION
        # ═══════════════════════════════════════════════
        ("55. All markets are based on deception - the obvious move is a trap", lambda e: "PRO" if e.get("counter_attack",0) > 0 else "NEUTRAL"),
        ("56. When the breakout seems certain, the reversal is near", lambda e: "PRO" if e.get("rsi",50) > 75 else "NEUTRAL"),
        ("57. When the crash seems imminent, the bounce is coming", lambda e: "PRO" if e.get("rsi",50) < 25 else "NEUTRAL"),
        ("58. The market lures retail in, then takes their money", lambda e: "PRO" if e.get("lead_lost",0) > 0 else "NEUTRAL"),
        ("59. Appear weak when you are strong - buy when others fear", lambda e: "PRO" if e.get("rsi",50) < 35 and e.get("trend","") == "bullish" else "NEUTRAL"),
        ("60. Appear strong when you are weak - sell when others are greedy", lambda e: "PRO" if e.get("rsi",50) > 70 and e.get("trend","") == "bearish" else "NEUTRAL"),
        ("61. Hold out baits - the market offers obvious setups that fail", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("62. If the trend is secure, be prepared for the pullback", lambda e: "PRO" if e.get("trend","") == "bullish" and e.get("rsi",50) < 50 else "NEUTRAL"),
        ("63. If volatility is superior, step aside and wait", lambda e: "PRO" if e.get("volatility",0) > e.get("price",0)*0.03 else "NEUTRAL"),
        ("64. Attack where the market is unprepared - at key levels", lambda e: "PRO" if e.get("at_support",False) or e.get("at_resistance",False) else "NEUTRAL"),
        ("65. Appear where you are not expected - enter before the crowd", lambda e: "PRO" if e.get("intelligence",5) > 6 and e.get("position_in_range",0) < 0.3 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # CALCULATION
        # ═══════════════════════════════════════════════
        ("66. The profitable trader makes many calculations before each trade", lambda e: "PRO" if e.get("preparation",5) > 6 else "CON" if e.get("preparation",5) < 4 else "NEUTRAL"),
        ("67. The losing trader makes few calculations and trades on impulse", lambda e: "CON" if e.get("preparation",5) < 4 else "NEUTRAL"),
        ("68. Many calculations lead to consistent profits", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("69. Few calculations lead to blown accounts", lambda e: "CON" if e.get("intelligence",5) < 4 else "NEUTRAL"),
        ("70. How much more no calculation at all!", lambda e: "CON" if e.get("intelligence",5) < 3 else "NEUTRAL"),
        ("71. It is by attention to this point that I can foresee profitable trades", lambda e: "PRO" if e.get("intelligence",5) > 6 and e.get("preparation",5) > 6 else "NEUTRAL"),
    ]