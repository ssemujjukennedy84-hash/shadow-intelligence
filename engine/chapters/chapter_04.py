"""Shadow - Chapter 4: Tactical Dispositions"""

def CHAPTER_4_RULES():
    return [
        # ── INVINCIBILITY ──
        ("1. The good fighters of old first put themselves beyond the possibility of defeat", 
         lambda e: "PRO" if e.get("goals_against",0)/max(e.get("played",1),1) < 1 else "NEUTRAL"),
        ("2. Then waited for an opportunity of defeating the enemy", 
         lambda e1,e2: "PRO" if e1.get("counter_attack",0) > e2.get("counter_attack",0) else "NEUTRAL"),
        ("3. To secure ourselves against defeat lies in our own hands", 
         lambda e: "PRO" if e.get("discipline",5) > 6 and e.get("preparation",5) > 6 else "NEUTRAL"),
        ("4. But the opportunity of defeating the enemy is provided by the enemy himself", 
         lambda e1,e2: "PRO" if e2.get("losses",0) > e1.get("losses",0) else "NEUTRAL"),
        ("5. The good fighter is able to secure himself against defeat", 
         lambda e: "PRO" if e.get("clean_sheets",0)/max(e.get("played",1),1) > 0.4 else "NEUTRAL"),
        ("6. But cannot make certain of defeating the enemy", 
         lambda e: "NEUTRAL"),
        
        # ── DEFENSE AND ATTACK ──
        ("7. Invincibility lies in the defense", 
         lambda e1,e2: "PRO" if e1.get("goals_against",0)/max(e1.get("played",1),1) < e2.get("goals_against",0)/max(e2.get("played",1),1) else "CON" if e2.get("goals_against",0)/max(e2.get("played",1),1) < e1.get("goals_against",0)/max(e1.get("played",1),1) else "NEUTRAL"),
        ("8. The possibility of victory lies in the attack", 
         lambda e1,e2: "PRO" if e1.get("goals_for",0) > e2.get("goals_for",0)*1.2 else "NEUTRAL"),
        ("9. When you defend, it is because your strength is inadequate", 
         lambda e1,e2: "CON" if e2.get("strength",5) > e1.get("strength",5)*1.3 else "NEUTRAL"),
        ("10. When you attack, it is because your strength is abundant", 
         lambda e1,e2: "PRO" if e1.get("strength",5) > e2.get("strength",5)*1.3 else "NEUTRAL"),
        ("11. The general who is skilled in defense hides in the most secret recesses", 
         lambda e: "PRO" if e.get("clean_sheets",0) > 5 and e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("12. He who is skilled in attack flashes forth from the topmost heights of heaven", 
         lambda e: "PRO" if e.get("goals_for",0)/max(e.get("played",1),1) > 2 and e.get("energy",50) > 70 else "NEUTRAL"),
        
        # ── SEEING THE UNSEEN ──
        ("13. To see victory only when it is within the ken of the common herd is not the acme of excellence", 
         lambda e: "PRO" if e.get("intelligence",5) > 7 else "NEUTRAL"),
        ("14. To lift an autumn hair is no sign of great strength", 
         lambda e: "NEUTRAL"),
        ("15. To see the sun and moon is no sign of sharp sight", 
         lambda e: "NEUTRAL"),
        ("16. To hear the noise of thunder is no sign of a quick ear", 
         lambda e: "NEUTRAL"),
        ("17. What the ancients called a clever fighter is one who not only wins but excels in winning with ease", 
         lambda e: "PRO" if e.get("form","").count("W") >= 4 and e.get("goals_against",0) < 5 else "NEUTRAL"),
        ("18. His victories bring him neither reputation for wisdom nor credit for courage", 
         lambda e: "PRO" if e.get("strength",5) > 7 and e.get("intelligence",5) > 7 else "NEUTRAL"),
        ("19. He wins his battles by making no mistakes", 
         lambda e: "PRO" if e.get("discipline",5) > 7 and e.get("losses",0) < 3 else "NEUTRAL"),
        ("20. Making no mistakes is what establishes the certainty of victory", 
         lambda e1,e2: "PRO" if e1.get("losses",0) < e2.get("losses",0)+2 else "NEUTRAL"),
        
        # ── THE STRATEGIC POSITION ──
        ("21. The victorious army first realizes the conditions for victory, then seeks battle", 
         lambda e1,e2: "PRO" if e1.get("intelligence",5) > e2.get("intelligence",5) and e1.get("preparation",5) > e2.get("preparation",5) else "NEUTRAL"),
        ("22. The defeated army fights first, then seeks victory", 
         lambda e: "CON" if e.get("preparation",5) < 5 and e.get("energy",50) > 60 else "NEUTRAL"),
        ("23. The skilled warrior cultivates the Way and preserves the Method", 
         lambda e: "PRO" if e.get("discipline",5) > 6 and e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("24. Thus he is the arbiter of other men's fates", 
         lambda e: "PRO" if e.get("manager_quality",5) > 7 else "NEUTRAL"),
        
        # ── THE FIVE ELEMENTS OF MEASUREMENT ──
        ("25. Measurement owes its existence to Earth", 
         lambda e: "PRO" if e.get("pitch_condition","good") == "good" else "NEUTRAL"),
        ("26. Estimation of quantity to Measurement", 
         lambda e: "PRO" if e.get("squad_depth",0) > 15 else "NEUTRAL"),
        ("27. Calculation to Estimation of quantity", 
         lambda e: "PRO" if e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("28. Balancing of chances to Calculation", 
         lambda e1,e2: "PRO" if e1.get("preparation",5) > e2.get("preparation",5)+1 else "NEUTRAL"),
        ("29. Victory to Balancing of chances", 
         lambda e1,e2: "PRO" if e1.get("strength",5) > e2.get("strength",5)*1.2 and e1.get("intelligence",5) > 5 else "NEUTRAL"),
        ("30. A victorious army is like a pound weight placed in the scale against a single grain", 
         lambda e1,e2: "PRO" if e1.get("strength",5) > e2.get("strength",5)*2 else "NEUTRAL"),
        ("31. The onrush of a conquering force is like the bursting of pent-up waters", 
         lambda e: "PRO" if e.get("momentum",0) > 2 and e.get("energy",50) > 70 else "NEUTRAL"),
    ]


if __name__ == "__main__":
    rules = CHAPTER_4_RULES()
    print(f"Chapter 4: {len(rules)} principles loaded")