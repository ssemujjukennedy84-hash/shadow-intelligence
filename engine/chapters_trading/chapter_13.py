"""Shadow - Chapter 13: Use of Spies (Trading Version)
Complete. Every principle. Every strategy. Every idea.
Intelligence. Data quality. Foreknowledge. The crown of trading wisdom."""

def CHAPTER_13_RULES():
    return [
        # ═══════════════════════════════════════════════
        # THE COST AND VALUE OF INTELLIGENCE
        # ═══════════════════════════════════════════════
        ("1. Trading with a large account across many markets entails great cost in time and focus", lambda e: "CON" if e.get("travel_distance",0) > 3000 and e.get("squad_value",0) < 300 else "NEUTRAL"),
        ("2. The daily expenditure of mental energy on poor data is enormous", lambda e: "CON" if e.get("fixture_congestion",0) > 5 and e.get("energy",50) < 50 else "NEUTRAL"),
        ("3. To remain ignorant of market conditions simply because one grudges the cost of good data", lambda e: "CON" if e.get("intelligence",5) < 4 else "NEUTRAL"),
        ("4. Is the height of foolishness in trading", lambda e: "CON" if e.get("intelligence",5) < 3 else "NEUTRAL"),
        ("5. Such a person is no trader at all — no protector of their own capital", lambda e: "CON" if e.get("manager_quality",5) < 4 and e.get("intelligence",5) < 4 else "NEUTRAL"),
        ("6. What enables the wise trader to strike and profit is foreknowledge of market conditions", lambda e: "PRO" if e.get("intelligence",5) > 6 and e.get("preparation",5) > 6 else "NEUTRAL"),
        ("7. This foreknowledge cannot be elicited from guesswork or hope", lambda e: "PRO" if e.get("source","") in ["YAHOO","API","REALTIME"] else "NEUTRAL"),
        ("8. It cannot be obtained by a single indicator or intuition alone", lambda e: "PRO" if e.get("intelligence",5) > 5 and e.get("news_count",0) > 3 else "NEUTRAL"),
        ("9. Knowledge of the market's true condition can only be obtained from reliable data and analysis", lambda e: "PRO" if e.get("data_freshness",0) < 24 else "CON" if e.get("data_freshness",0) > 72 else "NEUTRAL"),
        ("10. The trader who trades without data is like a general who marches blind", lambda e: "CON" if e.get("intelligence",5) < 4 and e.get("preparation",5) < 4 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE FIVE KINDS OF MARKET INTELLIGENCE
        # ═══════════════════════════════════════════════
        ("11. There are five kinds of intelligence that can be employed in trading", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("12. Local spies: the price action itself — the chart tells you everything if you can read it", lambda e: "PRO" if e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("13. Inward spies: order flow, volume profile, and market depth — what the institutions are doing", lambda e: "PRO" if e.get("volume_avg",0) > 500000 else "NEUTRAL"),
        ("14. Converted spies: news and economic data — information that was private becomes public", lambda e: "PRO" if e.get("news_count",0) > 2 else "NEUTRAL"),
        ("15. Doomed spies: backtested strategies that are shared publicly — they stop working once revealed", lambda e: "CON" if e.get("formation_changes",0) < 1 and e.get("played",0) > 30 else "NEUTRAL"),
        ("16. Surviving spies: real-time data feeds and level 2 data — information that returns from the front lines", lambda e: "PRO" if e.get("data_freshness",0) < 1 else "CON" if e.get("data_freshness",0) > 24 else "NEUTRAL"),
        ("17. When these five kinds of intelligence are all active, no market move will surprise you", lambda e: "PRO" if e.get("news_count",0) > 3 and e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("18. This is called the divine manipulation of information — the trader's most precious ability", lambda e: "PRO" if e.get("manager_quality",5) > 7 and e.get("intelligence",5) > 7 else "NEUTRAL"),
        ("19. The trader with superior information has superior results", lambda e: "PRO" if e.get("intelligence",5) > 7 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # HOW TO USE MARKET INTELLIGENCE
        # ═══════════════════════════════════════════════
        ("20. Intelligence must be treated with the utmost respect and attention", lambda e: "PRO" if e.get("preparation",5) > 6 else "NEUTRAL"),
        ("21. Good data deserves more investment than any indicator or course", lambda e: "PRO" if e.get("squad_value",0) > 400 else "NEUTRAL"),
        ("22. Without subtle interpretation, raw data cannot be used properly", lambda e: "PRO" if e.get("intelligence",5) > 7 else "NEUTRAL"),
        ("23. Without discipline and patience, even perfect data cannot save a trader", lambda e: "PRO" if e.get("discipline",5) > 6 and e.get("patience",5) > 6 else "NEUTRAL"),
        ("24. Without careful analysis, no truth can be obtained from market data", lambda e: "PRO" if e.get("manager_quality",5) > 7 else "NEUTRAL"),
        ("25. Be subtle! Be subtle! Use every piece of data for every kind of trading decision", lambda e: "PRO" if e.get("intelligence",5) > 7 and e.get("preparation",5) > 6 else "NEUTRAL"),
        ("26. If a trading signal is acted upon before it is confirmed, both the signal and the capital may be lost", lambda e: "CON" if e.get("entry_trigger",False) and e.get("discipline",5) < 5 else "NEUTRAL"),
        ("27. Patience in waiting for confirmation is the mark of the professional trader", lambda e: "PRO" if e.get("patience",5) > 7 else "NEUTRAL"),
        
        # ═══════════════════════════════════════════════
        # THE ULTIMATE INTELLIGENCE
        # ═══════════════════════════════════════════════
        ("28. Whether the objective is to scalp, day trade, or swing trade", lambda e: "PRO" if e.get("strength",5) > 6 else "NEUTRAL"),
        ("29. It is always necessary to begin by understanding the market's structure and key participants", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("30. The market's traps must be identified before they are sprung on you", lambda e: "PRO" if e.get("intelligence",5) > 5 and e.get("counter_attack",0) > 0 else "NEUTRAL"),
        ("31. False breakouts and stop hunts — these are the enemy's converted spies working against you", lambda e: "PRO" if e.get("comeback_wins",0) > 1 else "NEUTRAL"),
        ("32. It is through understanding market manipulation that we avoid being its victim", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("33. Every piece of market data must be questioned: is this genuine or a trap?", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("34. Only the disciplined trader with superior intelligence can consistently profit", lambda e: "PRO" if e.get("manager_quality",5) > 7 and e.get("intelligence",5) > 7 else "NEUTRAL"),
        ("35. Intelligence is the most important element in trading", lambda e: "PRO" if e.get("intelligence",5) > 7 else "NEUTRAL"),
        ("36. On it depends the trader's ability to enter, to hold, and to exit profitably", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("37. The trader who knows more will earn more", lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("38. The trader who knows less will lose to those who know more", lambda e: "CON" if e.get("intelligence",5) < 4 else "NEUTRAL"),
        ("39. This is the final teaching: knowledge is the foundation of all trading success", lambda e: "PRO" if e.get("intelligence",5) > 6 and e.get("preparation",5) > 6 else "NEUTRAL"),
    ]