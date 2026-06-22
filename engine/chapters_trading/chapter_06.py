"""Shadow - Chapter 6: Weak Points and Strong (Trading Version)
Complete. Every principle. Every strategy. Every idea.
This chapter is the heart of finding edge in the market."""

def CHAPTER_6_RULES():
    return [
        # ═══════════════════════════════════════════════
        # SEIZING THE INITIATIVE
        # ═══════════════════════════════════════════════
        ("1. Whoever is first to identify the trend and awaits the pullback will be fresh for the entry", lambda e1,e2: "PRO" if e1.get("rest_days",7) > e2.get("rest_days",7)+1 else "CON" if e2.get("rest_days",7) > e1.get("rest_days",7)+1 else "NEUTRAL"),
        ("2. Whoever chases the move after it has already run will arrive exhausted and late", lambda e1,e2: "CON" if e1.get("position_in_range",0) > 0.8 else "PRO" if e2.get("position_in_range",0) > 0.8 else "NEUTRAL"),
        ("3. The clever trader imposes their will on the market by waiting for their price", lambda e: "PRO" if e.get("patience",5) > 7 and e.get("discipline",5) > 6 else "NEUTRAL"),
        ("4. They do not allow the market's noise to impose on their strategy", lambda e: "PRO" if e.get("discipline",5) > 6 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("5. By placing limit orders at key levels, they cause the market to come to them", lambda e: "PRO" if e.get("at_support",False) and e.get("preparation",5) > 6 else "NEUTRAL"),
        ("6. By setting stop losses, they make it impossible for the market to inflict catastrophic damage", lambda e: "PRO" if e.get("stop_loss_set",False) else "NEUTRAL"),
        ("7. The trader who controls their entry and exit controls their destiny", lambda e: "PRO" if e.get("discipline",5) > 7 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # ATTACKING WHERE THE MARKET IS WEAK
        # ═══════════════════════════════════════════════
        ("8. Appear at support levels where the market must bounce or break", lambda e: "PRO" if e.get("at_support",False) and e.get("rsi",50) < 40 else "NEUTRAL"),
        ("9. March swiftly to where the crowd is not positioned", lambda e: "PRO" if e.get("intelligence",5) > 6 and e.get("position_in_range",0) < 0.3 else "NEUTRAL"),
        ("10. You can be sure of profit if you only enter where the market shows clear weakness at resistance", lambda e: "PRO" if e.get("at_resistance",False) and e.get("rsi",50) > 70 else "NEUTRAL"),
        ("11. You can ensure safety if you only buy at strong support with confirmation", lambda e: "PRO" if e.get("at_support",False) and e.get("trend","") == "bullish" and e.get("rsi",50) < 40 else "NEUTRAL"),
        ("12. The trader skilled in entries makes the market not know where they will strike next", lambda e: "PRO" if e.get("formation_changes",0) > 1 and e.get("counter_attack",0) > 0 else "NEUTRAL"),
        ("13. The trader whose stops are well-placed makes the market unable to hurt them", lambda e: "PRO" if e.get("stop_loss_set",False) and e.get("capital_risk",5) < 4 else "NEUTRAL"),
        ("14. Strike where the volume is thin and the move will be explosive", lambda e: "PRO" if e.get("volume_avg",0) < 200000 and e.get("at_support",False) else "NEUTRAL"),
        ("15. Avoid where the volume is heavy and the move will be sluggish", lambda e: "CON" if e.get("volume_avg",0) > 800000 and e.get("position_in_range",0) > 0.5 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE ART OF CONCEALMENT
        # ═══════════════════════════════════════════════
        ("16. By understanding market structure while remaining patient", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("17. We can keep our capital concentrated while the market is dispersed", lambda e: "PRO" if e.get("position_size",0) < 10 and e.get("tf_alignment",0) > 0.6 else "NEUTRAL"),
        ("18. We form a single decisive entry while the market offers many false signals", lambda e: "PRO" if e.get("setup_quality",5) > 7 else "NEUTRAL"),
        ("19. The exact level where we intend to enter must be predetermined", lambda e: "PRO" if e.get("preparation",5) > 6 else "NEUTRAL"),
        ("20. The market must not shake us out before our target is reached", lambda e: "PRO" if e.get("discipline",5) > 6 else "NEUTRAL"),
        ("21. If the market knows where your stop is, it will hunt for it", lambda e: "PRO" if e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("22. Place stops beyond obvious levels where the crowd places theirs", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # NUMERICAL SUPERIORITY AT THE POINT OF ENTRY
        # ═══════════════════════════════════════════════
        ("23. If the market knows not where the support truly lies, it must test everywhere", lambda e: "PRO" if e.get("formation_changes",0) > 1 else "NEUTRAL"),
        ("24. And its energy being spread thin, we can concentrate our capital at the true level", lambda e: "PRO" if e.get("position_size",0) < 10 and e.get("at_support",False) else "NEUTRAL"),
        ("25. A small account can defeat a large move by entering at the perfect moment", lambda e: "PRO" if e.get("setup_quality",5) > 7 and e.get("position_in_range",0) < 0.3 else "NEUTRAL"),
        ("26. The appearance of weakness at a key level draws in the crowd — then reverses", lambda e: "PRO" if e.get("counter_attack",0) > 0 else "NEUTRAL"),
        ("27. What is a weak point today may be a strong point tomorrow", lambda e: "NEUTRAL"),
        ("28. The trader must constantly reassess where support and resistance truly lie", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # ADAPTING TO MARKET CONDITIONS
        # ═══════════════════════════════════════════════
        ("29. An asset may trend greatly if it moves through levels where selling is exhausted", lambda e: "PRO" if e.get("trend_strength",0) > 0.6 and e.get("volume_avg",0) < 300000 else "NEUTRAL"),
        ("30. Market structure is like water — it shapes its course according to the terrain", lambda e: "PRO" if e.get("formation_changes",0) > 1 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("31. The trader achieves victory in relation to the market conditions they face", lambda e: "PRO" if e.get("manager_quality",5) > 6 else "NEUTRAL"),
        ("32. Water retains no constant shape — so in trading there are no constant setups", lambda e: "PRO" if e.get("formation_changes",0) > 1 else "NEUTRAL"),
        ("33. What worked yesterday may fail today — adapt or lose", lambda e: "PRO" if e.get("intelligence",5) > 6 and e.get("formation_changes",0) > 0 else "NEUTRAL"),
        ("34. He who can modify entries based on market conditions will survive", lambda e: "PRO" if e.get("intelligence",5) > 6 and e.get("formation_changes",0) > 1 else "NEUTRAL"),
        ("35. He who rigidly follows one setup in all conditions will eventually fail", lambda e: "CON" if e.get("formation_changes",0) < 1 and e.get("played",0) > 20 else "NEUTRAL"),
        ("36. The market has no constant form — the trader must have no constant bias", lambda e: "PRO" if e.get("intelligence",5) > 7 else "NEUTRAL"),
    ]