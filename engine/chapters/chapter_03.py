"""Shadow - Chapter 3: Attack by Stratagem"""

def CHAPTER_3_RULES():
    return [
        # ── THE SUPREME ART OF WAR ──
        ("1. In the practical art of war, the best thing is to take the enemy's country whole and intact", 
         lambda e1,e2: "PRO" if e1.get("strength",5) > e2.get("strength",5)*1.5 else "NEUTRAL"),
        ("2. Supreme excellence consists in breaking the enemy's resistance without fighting", 
         lambda e1,e2: "PRO" if e1.get("strength",5) > e2.get("strength",5)*1.5 and e2.get("morale",5) < 5 else "NEUTRAL"),
        ("3. The highest form of generalship is to balk the enemy's plans", 
         lambda e1,e2: "PRO" if e1.get("intelligence",5) > e2.get("intelligence",5)+2 else "CON" if e2.get("intelligence",5) > e1.get("intelligence",5)+2 else "NEUTRAL"),
        ("4. The next best is to prevent the junction of the enemy's forces", 
         lambda e1,e2: "PRO" if e1.get("clean_sheets",0) > e2.get("clean_sheets",0)+2 else "NEUTRAL"),
        ("5. The next is to attack the enemy's army in the field", 
         lambda e1,e2: "PRO" if e1.get("goals_for",0) > e2.get("goals_for",0)*1.2 else "NEUTRAL"),
        ("6. The worst policy of all is to besiege walled cities", 
         lambda e1,e2: "CON" if e2.get("clean_sheets",0) > e1.get("clean_sheets",0)+2 else "NEUTRAL"),
        
        # ── THE COST OF SIEGE ──
        ("7. The preparation of siege weapons takes months and exhausts resources", 
         lambda e: "CON" if e.get("energy",50) < 40 and e.get("squad_value",0) < 200 else "NEUTRAL"),
        ("8. The general, unable to control his impatience, orders his troops to swarm the walls", 
         lambda e: "CON" if e.get("discipline",5) < 4 and e.get("manager_quality",5) < 5 else "NEUTRAL"),
        ("9. A third of his men are killed and the city remains untaken", 
         lambda e: "CON" if e.get("injuries",0) > 3 and e.get("away_wins",0) < 2 else "NEUTRAL"),
        ("10. Such are the disastrous effects of a siege", 
         lambda e: "CON" if e.get("losses",0) > 3 and e.get("goals_for",0) < 5 else "NEUTRAL"),
        
        # ── THE SKILLFUL LEADER ──
        ("11. The skillful leader subdues the enemy's troops without any fighting", 
         lambda e1,e2: "PRO" if e1.get("strength",5) > e2.get("strength",5)*1.5 and e1.get("intelligence",5) > 7 else "NEUTRAL"),
        ("12. He captures their cities without laying siege to them", 
         lambda e: "PRO" if e.get("away_wins",0) > 3 else "NEUTRAL"),
        ("13. He overthrows their kingdom without lengthy operations in the field", 
         lambda e: "PRO" if e.get("form","").count("W") >= 4 and e.get("energy",50) > 60 else "NEUTRAL"),
        ("14. With his forces intact, he disputes the mastery of the empire", 
         lambda e: "PRO" if e.get("squad_depth",0) > 20 and e.get("strength",5) > 7 else "NEUTRAL"),
        ("15. His triumph is complete without losing a single man", 
         lambda e: "PRO" if e.get("clean_sheets",0) > 5 and e.get("injuries",0) < 2 else "NEUTRAL"),
        
        # ── THE ART OF USING TROOPS ──
        ("16. It is the rule in war: if our forces are ten to the enemy's one, surround him", 
         lambda e1,e2: "PRO" if e1.get("strength",5) > e2.get("strength",5)*2 else "NEUTRAL"),
        ("17. If five to one, attack him", 
         lambda e1,e2: "PRO" if e1.get("strength",5) > e2.get("strength",5)*1.8 else "NEUTRAL"),
        ("18. If twice as numerous, divide our army", 
         lambda e1,e2: "PRO" if e1.get("strength",5) > e2.get("strength",5)*1.4 else "NEUTRAL"),
        ("19. If equally matched, we can offer battle", 
         lambda e1,e2: "PRO" if abs(e1.get("strength",5)-e2.get("strength",5)) < 1 and e1.get("morale",5) > e2.get("morale",5) else "NEUTRAL"),
        ("20. If slightly inferior in numbers, we can avoid the enemy", 
         lambda e1,e2: "CON" if e2.get("strength",5) > e1.get("strength",5)*1.1 else "NEUTRAL"),
        ("21. If quite unequal in every way, we can flee from him", 
         lambda e1,e2: "CON" if e2.get("strength",5) > e1.get("strength",5)*1.5 else "NEUTRAL"),
        
        # ── THE THREE WAYS A RULER CAN BRING MISFORTUNE ──
        ("22. A ruler can bring misfortune by ordering the army to advance when it cannot", 
         lambda e: "CON" if e.get("manager_quality",5) < 4 and e.get("discipline",5) > 6 else "NEUTRAL"),
        ("23. By ordering a retreat when the army cannot retreat", 
         lambda e: "CON" if e.get("manager_quality",5) < 4 and e.get("morale",5) > 6 else "NEUTRAL"),
        ("24. This is called hobbling the army", 
         lambda e: "CON" if e.get("organization",5) < 4 else "NEUTRAL"),
        ("25. By interfering with military administration without understanding the difficulties", 
         lambda e: "CON" if e.get("intelligence",5) < 4 and e.get("discipline",5) > 5 else "NEUTRAL"),
        ("26. This causes restlessness and distrust among the soldiers", 
         lambda e: "CON" if e.get("team_harmony",5) < 5 and e.get("morale",5) < 5 else "NEUTRAL"),
        
        # ── THE FIVE ESSENTIALS FOR VICTORY ──
        ("27. He will win who knows when to fight and when not to fight", 
         lambda e1,e2: "PRO" if e1.get("intelligence",5) > e2.get("intelligence",5)+1 else "CON" if e2.get("intelligence",5) > e1.get("intelligence",5)+1 else "NEUTRAL"),
        ("28. He will win who knows how to handle both superior and inferior forces", 
         lambda e: "PRO" if e.get("manager_quality",5) > 6 and e.get("squad_depth",0) > 20 else "NEUTRAL"),
        ("29. He will win whose army is animated by the same spirit throughout", 
         lambda e1,e2: "PRO" if e1.get("team_harmony",5) > e2.get("team_harmony",5)+1 else "CON" if e2.get("team_harmony",5) > e1.get("team_harmony",5)+1 else "NEUTRAL"),
        ("30. He will win who, prepared himself, waits to take the enemy unprepared", 
         lambda e1,e2: "PRO" if e1.get("preparation",5) > e2.get("preparation",5)+2 else "NEUTRAL"),
        ("31. He will win who has military capacity and is not interfered with by the sovereign", 
         lambda e: "PRO" if e.get("manager_quality",5) > 7 and e.get("organization",5) > 6 else "NEUTRAL"),
        
        # ── KNOW YOURSELF, KNOW YOUR ENEMY ──
        ("32. If you know the enemy and know yourself, you need not fear the result of a hundred battles", 
         lambda e1,e2: "PRO" if e1.get("intelligence",5) > e2.get("intelligence",5) and e1.get("strength",5) > e2.get("strength",5) else "CON" if e2.get("intelligence",5) > e1.get("intelligence",5) and e2.get("strength",5) > e1.get("strength",5) else "NEUTRAL"),
        ("33. If you know yourself but not the enemy, for every victory gained you will also suffer a defeat", 
         lambda e: "CON" if e.get("intelligence",5) < 5 else "NEUTRAL"),
        ("34. If you know neither the enemy nor yourself, you will succumb in every battle", 
         lambda e: "CON" if e.get("intelligence",5) < 3 and e.get("preparation",5) < 3 else "NEUTRAL"),
        ("35. Knowledge is the foundation of all strategic victory", 
         lambda e1,e2: "PRO" if e1.get("intelligence",5) > e2.get("intelligence",5)+1 else "CON" if e2.get("intelligence",5) > e1.get("intelligence",5)+1 else "NEUTRAL"),
    ]


if __name__ == "__main__":
    rules = CHAPTER_3_RULES()
    print(f"Chapter 3: {len(rules)} principles loaded")