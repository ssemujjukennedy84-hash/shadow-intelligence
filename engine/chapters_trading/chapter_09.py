"""Shadow - Chapter 9: The Army on the March (Trading Version)
Complete. Every principle. Every strategy. Every idea.
Reading market signals. Recognizing traps. Interpreting every price movement."""

def CHAPTER_9_RULES():
    return [
        # ═══════════════════════════════════════════════
        # POSITIONING IN DIFFERENT MARKET TERRAINS
        # ═══════════════════════════════════════════════
        ("1. Camp in high places — position your entry at the best possible price level", lambda e: "PRO" if e.get("position_in_range",0) < 0.35 else "CON" if e.get("position_in_range",0) > 0.65 else "NEUTRAL"),
        ("2. Face the sun — trade in the direction of the dominant trend", lambda e: "PRO" if e.get("trend","") != "neutral" else "CON" if e.get("trend","") == "neutral" else "NEUTRAL"),
        ("3. Do not climb heights to fight — do not chase price that has already run far", lambda e: "CON" if e.get("position_in_range",0) > 0.8 else "NEUTRAL"),
        ("4. After crossing a volatile zone, get far away from it — let the market settle", lambda e: "PRO" if e.get("patience",5) > 6 and e.get("volatility",0) < e.get("price",0)*0.01 else "NEUTRAL"),
        ("5. When price breaks a level, do not meet it at the break — wait for the retest", lambda e: "PRO" if e.get("counter_attack",0) > 0 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("6. Let half the move confirm, then enter — do not anticipate", lambda e: "PRO" if e.get("entry_trigger",False) and e.get("discipline",5) > 6 else "NEUTRAL"),
        ("7. Pass quickly over uncertain ground — do not trade during news or low liquidity", lambda e: "CON" if e.get("volatility",0) > e.get("price",0)*0.03 else "NEUTRAL"),
        ("8. In trending markets, take up positions with clear entries and exits", lambda e: "PRO" if e.get("trend_strength",0) > 0.5 and e.get("preparation",5) > 5 else "NEUTRAL"),
        ("9. In ranging markets, trade the edges — buy support, sell resistance", lambda e: "PRO" if e.get("at_support",False) and e.get("trend","") == "neutral" else "NEUTRAL"),
        ("10. High volatility with no direction is a market to avoid entirely", lambda e: "CON" if e.get("volatility",0) > e.get("price",0)*0.03 and e.get("trend","") == "neutral" else "NEUTRAL"),
        ("11. Low volatility with clear structure is a market to engage", lambda e: "PRO" if e.get("volatility",0) < e.get("price",0)*0.01 and e.get("trend","") != "neutral" else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # READING THE ENEMY — MARKET SIGNALS
        # ═══════════════════════════════════════════════
        ("12. When the market is quiet at a key level, it gathers energy for an explosive move", lambda e: "PRO" if e.get("at_support",False) and e.get("volume_avg",0) < 250000 else "NEUTRAL"),
        ("13. When the enemy is close and remains quiet, he relies on the strength of his position — price at support with low volume is strong", lambda e: "PRO" if e.get("at_support",False) and e.get("volume_avg",0) < 300000 else "NEUTRAL"),
        ("14. When he is at a distance and tries to provoke battle, he wants you to advance — a sudden spike is a trap", lambda e: "CON" if e.get("momentum",0) > 2 and e.get("volume_avg",0) < 200000 else "NEUTRAL"),
        ("15. When price moves with low volume, the move is false — do not trust it", lambda e: "CON" if abs(e.get("change_pct",0)) > 2 and e.get("volume_avg",0) < 200000 else "NEUTRAL"),
        ("16. When price drifts on high volume, smart money is accumulating or distributing", lambda e: "PRO" if e.get("volume_avg",0) > 500000 and abs(e.get("change_pct",0)) < 1 else "NEUTRAL"),
        ("17. When the enemy's envoys speak humbly while preparations continue — price makes small moves while volume builds", lambda e: "PRO" if e.get("volume_avg",0) > 400000 and abs(e.get("change_pct",0)) < 0.5 else "NEUTRAL"),
        ("18. When their language is strong and they threaten — aggressive price action with declining volume signals bluff", lambda e: "CON" if e.get("momentum",0) > 2 and e.get("volume_avg",0) < 300000 else "NEUTRAL"),
        ("19. Humble words with increased preparations signal an imminent attack — quiet accumulation precedes a breakout", lambda e: "PRO" if e.get("volume_avg",0) > 500000 and e.get("change_pct",0) < 0.3 else "NEUTRAL"),
        ("20. Strong words without substance signal retreat — a sharp move without volume will reverse", lambda e: "CON" if e.get("momentum",0) > 2 and e.get("volume_avg",0) < 250000 else "NEUTRAL"),
        ("21. When the enemy sees an advantage but does not advance — price approaches a level but cannot break it", lambda e: "PRO" if e.get("at_resistance",False) and e.get("momentum",0) < 0.5 else "NEUTRAL"),
        ("22. He is fatigued — the trend is exhausted and ready to reverse", lambda e: "CON" if e.get("trend_strength",0) > 0.7 and e.get("rsi",50) > 70 else "NEUTRAL"),
        ("23. Birds rising in flight signals an ambush — unusual volume spikes warn of a trap", lambda e: "CON" if e.get("volume_avg",0) > 700000 and e.get("trend","") == "neutral" else "NEUTRAL"),
        ("24. Startled beasts indicate a sudden attack — a sudden spike on high volume is a genuine breakout", lambda e: "PRO" if e.get("momentum",0) > 3 and e.get("volume_avg",0) > 500000 else "NEUTRAL"),
        ("25. Dust rising in high columns signals chariots — heavy buying volume signals institutions entering", lambda e: "PRO" if e.get("volume_avg",0) > 600000 and e.get("trend","") == "bullish" else "NEUTRAL"),
        ("26. Dust low and widespread signals infantry — steady moderate volume signals retail participation", lambda e: "NEUTRAL"),
        ("27. When the enemy's soldiers whisper in small groups, they have lost confidence — small candles with long wicks show indecision", lambda e: "CON" if e.get("trend","") == "neutral" and e.get("volatility",0) > e.get("price",0)*0.02 else "NEUTRAL"),
        ("28. Too many punishments indicate extreme exhaustion — multiple stop hunts signal an imminent reversal", lambda e: "PRO" if e.get("comeback_wins",0) > 2 else "NEUTRAL"),
        ("29. When troops are disorderly, the general's authority is weak — when price is erratic, the trend is weak", lambda e: "CON" if e.get("trend_strength",0) < 0.3 and e.get("volatility",0) > e.get("price",0)*0.02 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # JUDGING THE ENEMY'S STRENGTH
        # ═══════════════════════════════════════════════
        ("30. If the enemy's troops are united in spirit, they are difficult to defeat — multi-timeframe alignment is hard to reverse", lambda e: "PRO" if e.get("tf_alignment",0) > 0.7 else "NEUTRAL"),
        ("31. If they are divided, they are vulnerable — conflicting timeframes signal a reversal", lambda e: "CON" if e.get("tf_alignment",0) < 0.4 else "NEUTRAL"),
        ("32. When you outnumber the enemy, you may surround him — when your capital is large relative to the position, you can hold through pullbacks", lambda e: "PRO" if e.get("squad_depth",0) > 25 else "NEUTRAL"),
        ("33. Even when you are strong, appear weak to lure the enemy — let the market think it has won before you enter", lambda e: "PRO" if e.get("patience",5) > 7 and e.get("position_in_range",0) < 0.3 else "NEUTRAL"),
        ("34. He who is not thoughtful and treats his opponents with contempt will surely be captured — the overconfident trader will lose", lambda e: "CON" if e.get("preparation",5) < 4 and e.get("intelligence",5) < 5 else "NEUTRAL"),
        ("35. If traders enter without confirming their setup, they will not be profitable", lambda e: "CON" if e.get("discipline",5) > 6 and e.get("setup_quality",5) < 4 else "NEUTRAL"),
        ("36. If confirmation is present but the trader hesitates, they will miss the opportunity", lambda e: "CON" if e.get("entry_trigger",False) and e.get("discipline",5) < 5 else "NEUTRAL"),
        ("37. Therefore setups must be confirmed, and confirmed setups must be executed without hesitation", lambda e: "PRO" if e.get("setup_quality",5) > 5 and e.get("discipline",5) > 5 else "NEUTRAL"),
        ("38. This is the path to consistent and profitable execution", lambda e: "PRO" if e.get("discipline",5) > 5 and e.get("morale",5) > 6 else "NEUTRAL"),
    ]