"""Shadow - Chapter 13: Use of Spies"""

def CHAPTER_13_RULES():
    return [
        # ── THE COST AND VALUE OF INTELLIGENCE ──
        ("1. Raising an army of a hundred thousand men and marching them great distances entails heavy cost", 
         lambda e: "CON" if e.get("travel_distance",0) > 3000 and e.get("squad_value",0) < 300 else "NEUTRAL"),
        ("2. The daily expenditure is enormous and the people are drained of resources", 
         lambda e: "CON" if e.get("fixture_congestion",0) > 5 and e.get("energy",50) < 50 else "NEUTRAL"),
        ("3. To remain ignorant of the enemy's condition simply because one grudges the cost of intelligence", 
         lambda e: "CON" if e.get("intelligence",5) < 4 else "NEUTRAL"),
        ("4. Is the height of inhumanity", 
         lambda e: "CON" if e.get("intelligence",5) < 3 else "NEUTRAL"),
        ("5. Such a person is no general of the people, no present help to his sovereign", 
         lambda e: "CON" if e.get("manager_quality",5) < 4 and e.get("intelligence",5) < 4 else "NEUTRAL"),
        ("6. What enables the wise sovereign and the good general to strike and conquer is foreknowledge", 
         lambda e1,e2: "PRO" if e1.get("intelligence",5) > e2.get("intelligence",5)+2 else "CON" if e2.get("intelligence",5) > e1.get("intelligence",5)+2 else "NEUTRAL"),
        ("7. This foreknowledge cannot be elicited from spirits nor from gods", 
         lambda e: "PRO" if e.get("source","") in ["API_FOOTBALL","YAHOO","WORLD_CUP","OFFICIAL"] else "NEUTRAL"),
        ("8. It cannot be obtained by calculation or deduction alone", 
         lambda e: "PRO" if e.get("intelligence",5) > 5 and e.get("news_count",0) > 3 else "NEUTRAL"),
        ("9. Knowledge of the enemy's dispositions can only be obtained from other men", 
         lambda e: "PRO" if len(e.get("injury_news",[]) or []) > 0 else "NEUTRAL"),
        
        # ── THE FIVE KINDS OF SPIES ──
        ("10. There are five kinds of spies that can be employed", 
         lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("11. Local spies: inhabitants of the enemy's district", 
         lambda e: "PRO" if e.get("home_away","") == "home" else "NEUTRAL"),
        ("12. Inward spies: officials of the enemy government", 
         lambda e1,e2: "PRO" if e2.get("suspension",0) > 0 or e2.get("injuries",0) > 2 else "NEUTRAL"),
        ("13. Converted spies: enemy spies turned to our service", 
         lambda e: "PRO" if e.get("h2h_advantage",0) > 0 else "NEUTRAL"),
        ("14. Doomed spies: those we deliberately deceive with false information", 
         lambda e: "PRO" if e.get("counter_attack",0) > 1 else "NEUTRAL"),
        ("15. Surviving spies: those who bring back news from the enemy's camp", 
         lambda e: "PRO" if e.get("data_freshness",0) < 24 else "CON" if e.get("data_freshness",0) > 72 else "NEUTRAL"),
        ("16. When these five kinds of spies are all active, no one knows the route", 
         lambda e: "PRO" if e.get("news_count",0) > 3 and e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("17. This is called the divine manipulation of threads — the sovereign's most precious faculty", 
         lambda e: "PRO" if e.get("manager_quality",5) > 7 and e.get("intelligence",5) > 7 else "NEUTRAL"),
        
        # ── HOW TO USE SPIES ──
        ("18. Spies must be treated with the utmost kindness and generosity", 
         lambda e: "PRO" if e.get("team_harmony",5) > 6 else "NEUTRAL"),
        ("19. They must be rewarded more liberally than any other soldiers", 
         lambda e: "PRO" if e.get("squad_value",0) > 400 else "NEUTRAL"),
        ("20. Without subtle ingenuity, the spy cannot be used properly", 
         lambda e: "PRO" if e.get("intelligence",5) > 7 else "NEUTRAL"),
        ("21. Without humanity and justice, the spy cannot be managed", 
         lambda e: "PRO" if e.get("team_harmony",5) > 6 and e.get("discipline",5) > 5 else "NEUTRAL"),
        ("22. Without delicate handling, no truth can be obtained from spies", 
         lambda e: "PRO" if e.get("manager_quality",5) > 7 else "NEUTRAL"),
        ("23. Be subtle! Be subtle! And use your spies for every kind of business", 
         lambda e: "PRO" if e.get("intelligence",5) > 7 and e.get("counter_attack",0) > 0 else "NEUTRAL"),
        ("24. If a secret piece of news is divulged by a spy before the time is ripe, the spy and those who heard must die", 
         lambda e: "NEUTRAL"),
        
        # ── THE ULTIMATE INTELLIGENCE ──
        ("25. Whether the object be to crush an army, to storm a city, or to assassinate an individual", 
         lambda e: "PRO" if e.get("strength",5) > 6 else "NEUTRAL"),
        ("26. It is always necessary to begin by finding out the names of the attendants, the aides-de-camp, and the gatekeepers", 
         lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("27. The enemy's spies who have come to spy on us must be sought out", 
         lambda e: "PRO" if e.get("counter_attack",0) > 0 else "NEUTRAL"),
        ("28. Tempted with bribes, led away, and comfortably housed — thus they become converted spies", 
         lambda e: "PRO" if e.get("squad_value",0) > 300 else "NEUTRAL"),
        ("29. It is through converted spies that we gain knowledge of the enemy", 
         lambda e1,e2: "PRO" if e1.get("h2h_advantage",0) > 0 else "NEUTRAL"),
        ("30. It is essential that converted spies be treated with the utmost liberality", 
         lambda e: "PRO" if e.get("team_harmony",5) > 6 else "NEUTRAL"),
        ("31. Of old, the rise of the Shang dynasty was due to a spy who served the Hsia", 
         lambda e: "PRO" if e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("32. The rise of the Chou dynasty was due to a spy who served the Yin", 
         lambda e: "PRO" if e.get("h2h_advantage",0) > 1 else "NEUTRAL"),
        ("33. Only the enlightened sovereign and the worthy general can use the highest intelligence", 
         lambda e: "PRO" if e.get("manager_quality",5) > 7 and e.get("intelligence",5) > 7 else "NEUTRAL"),
        ("34. Spies are the most important element in war", 
         lambda e1,e2: "PRO" if e1.get("intelligence",5) > e2.get("intelligence",5)+1 else "CON" if e2.get("intelligence",5) > e1.get("intelligence",5)+1 else "NEUTRAL"),
        ("35. On them depends an army's ability to move and to strike", 
         lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
    ]


if __name__ == "__main__":
    rules = CHAPTER_13_RULES()
    print(f"Chapter 13: {len(rules)} principles loaded")