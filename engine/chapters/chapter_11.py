"""Shadow - Chapter 11: The Nine Situations"""

def CHAPTER_11_RULES():
    return [
        # ── THE NINE SITUATIONS ──
        ("1. The art of war recognizes nine varieties of ground", 
         lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        
        # 1. DISPERSIVE GROUND
        ("2. Dispersive ground: when a chieftain is fighting in his own territory", 
         lambda e: "PRO" if e.get("home_away","") == "home" else "NEUTRAL"),
        ("3. On dispersive ground, do not fight — the soldiers are near home and will scatter", 
         lambda e: "CON" if e.get("home_away","") == "home" and e.get("morale",5) < 6 else "NEUTRAL"),
        ("4. On dispersive ground, unify the army's purpose and inspire them to defend their homes", 
         lambda e: "PRO" if e.get("team_harmony",5) > 6 and e.get("home_away","") == "home" else "NEUTRAL"),
        
        # 2. FRONTIER GROUND
        ("5. Frontier ground: when an army has penetrated only a short distance into enemy territory", 
         lambda e: "PRO" if e.get("away_wins",0) > 0 else "NEUTRAL"),
        ("6. On frontier ground, do not stop — push deeper to show commitment", 
         lambda e: "PRO" if e.get("energy",50) > 60 and e.get("away_wins",0) > 0 else "NEUTRAL"),
        
        # 3. CONTENTIOUS GROUND
        ("7. Contentious ground: ground that offers advantage to whoever holds it", 
         lambda e1,e2: "PRO" if abs(e1.get("strength",5)-e2.get("strength",5)) < 2 else "NEUTRAL"),
        ("8. On contentious ground, do not attack if the enemy has occupied it first", 
         lambda e1,e2: "CON" if e2.get("home_away","") == "home" and abs(e1.get("strength",5)-e2.get("strength",5)) < 2 else "NEUTRAL"),
        ("9. Race to occupy contentious ground before the enemy", 
         lambda e: "PRO" if e.get("energy",50) > 70 else "NEUTRAL"),
        
        # 4. OPEN GROUND
        ("10. Open ground: where both sides have freedom of movement", 
         lambda e: "NEUTRAL"),
        ("11. On open ground, do not try to block the enemy — prepare your defenses", 
         lambda e: "PRO" if e.get("clean_sheets",0) > 3 else "NEUTRAL"),
        
        # 5. INTERSECTING GROUND
        ("12. Intersecting ground: ground that is key to multiple territories — whoever holds it controls the region", 
         lambda e: "PRO" if e.get("capacity",0) > 50000 else "NEUTRAL"),
        ("13. On intersecting ground, form alliances with neighboring powers", 
         lambda e: "PRO" if e.get("team_harmony",5) > 6 else "NEUTRAL"),
        
        # 6. SERIOUS GROUND
        ("14. Serious ground: when an army has penetrated deep into enemy territory", 
         lambda e: "PRO" if e.get("away_wins",0) > 2 and e.get("travel_distance",0) > 2000 else "NEUTRAL"),
        ("15. On serious ground, gather provisions and live off the enemy's resources", 
         lambda e1,e2: "PRO" if e1.get("goals_for",0) > e2.get("goals_for",0) and e1.get("away_wins",0) > 1 else "NEUTRAL"),
        ("16. Keep the army constantly on the move to avoid detection", 
         lambda e: "PRO" if e.get("energy",50) > 60 and e.get("counter_attack",0) > 0 else "NEUTRAL"),
        
        # 7. DIFFICULT GROUND
        ("17. Difficult ground: forests, marshes, steep country — hard to traverse", 
         lambda e: "CON" if e.get("pitch_condition","") == "poor" or e.get("weather","") in ["Storm","Snow"] else "NEUTRAL"),
        ("18. On difficult ground, keep steadily on the march — do not stop or encamp", 
         lambda e: "PRO" if e.get("energy",50) > 60 and e.get("travel_distance",0) > 1000 else "NEUTRAL"),
        
        # 8. FATAL GROUND
        ("19. Fatal ground: terrain where only a swift victory can save you", 
         lambda e: "PRO" if e.get("must_win",False) else "NEUTRAL"),
        ("20. On fatal ground, fight immediately — there is no other option", 
         lambda e: "PRO" if e.get("must_win",False) and e.get("energy",50) > 60 else "NEUTRAL"),
        ("21. On fatal ground, make it clear to the soldiers that there is no retreat", 
         lambda e: "PRO" if e.get("must_win",False) else "NEUTRAL"),
        
        # 9. DESPERATE GROUND
        ("22. Desperate ground: where you can only be saved by fighting without delay", 
         lambda e: "PRO" if e.get("must_win",False) and e.get("strength",5) < 6 else "NEUTRAL"),
        ("23. On desperate ground, soldiers will fight to the death because there is no escape", 
         lambda e: "PRO" if e.get("must_win",False) else "NEUTRAL"),
        ("24. On desperate ground, proclaim the hopelessness of saving their lives", 
         lambda e: "NEUTRAL"),
        
        # ── THE GENERAL'S SKILL IN SITUATIONS ──
        ("25. The skillful tactician leads his enemy like a sheep on a string", 
         lambda e1,e2: "PRO" if e1.get("intelligence",5) > e2.get("intelligence",5)+1 and e1.get("counter_attack",0) > 0 else "NEUTRAL"),
        ("26. He can make the enemy follow by offering advantage", 
         lambda e1,e2: "PRO" if e1.get("counter_attack",0) > e2.get("counter_attack",0) else "NEUTRAL"),
        ("27. He can prevent the enemy from advancing by inflicting damage", 
         lambda e1,e2: "PRO" if e1.get("goals_for",0) > e2.get("goals_for",0)*1.2 else "NEUTRAL"),
        ("28. Speed is the essence of war — strike before the enemy is ready", 
         lambda e1,e2: "PRO" if e1.get("energy",50) > e2.get("energy",50)*1.2 else "NEUTRAL"),
        ("29. At first, be like a maiden — the enemy will open the door", 
         lambda e1,e2: "PRO" if e1.get("counter_attack",0) > 0 and e2.get("preparation",5) < 5 else "NEUTRAL"),
        ("30. Then be like a hare — the enemy will be too late to catch you", 
         lambda e: "PRO" if e.get("energy",50) > 70 and e.get("momentum",0) > 1 else "NEUTRAL"),
        ("31. The general must be calm and inscrutable", 
         lambda e: "PRO" if e.get("manager_quality",5) > 7 else "NEUTRAL"),
        ("32. He must be able to keep his own counsel and not reveal his plans", 
         lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("33. He drives his men to action without explaining the full design", 
         lambda e: "PRO" if e.get("manager_quality",5) > 6 else "NEUTRAL"),
        ("34. By altering his arrangements and changing his plans, he keeps the enemy in the dark", 
         lambda e: "PRO" if e.get("formation_changes",0) > 2 else "NEUTRAL"),
        ("35. He shifts his camp and takes circuitous routes to confuse the enemy", 
         lambda e: "PRO" if e.get("counter_attack",0) > 1 else "NEUTRAL"),
        ("36. The general leads his army as though he were leading a single man by the hand", 
         lambda e: "PRO" if e.get("team_harmony",5) > 7 and e.get("manager_quality",5) > 7 else "NEUTRAL"),
        ("37. The principle on which to manage an army is to set up one standard of courage for all", 
         lambda e: "PRO" if e.get("discipline",5) > 6 else "NEUTRAL"),
        ("38. The skillful warrior places his army in a position from which there is no retreat", 
         lambda e: "PRO" if e.get("must_win",False) else "NEUTRAL"),
        ("39. Soldiers in desperate straits lose all sense of fear", 
         lambda e: "PRO" if e.get("must_win",False) else "NEUTRAL"),
        ("40. They fight because there is no place to run", 
         lambda e: "PRO" if e.get("must_win",False) else "NEUTRAL"),
    ]


if __name__ == "__main__":
    rules = CHAPTER_11_RULES()
    print(f"Chapter 11: {len(rules)} principles loaded")