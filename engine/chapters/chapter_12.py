"""Shadow - Chapter 12: Attack by Fire"""

def CHAPTER_12_RULES():
    return [
        # ── THE FIVE WAYS OF ATTACKING WITH FIRE ──
        ("1. There are five ways of attacking with fire", 
         lambda e: "PRO" if e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("2. The first is to burn soldiers in their camp", 
         lambda e1,e2: "PRO" if e2.get("injuries",0) > 2 and e1.get("energy",50) > 60 else "NEUTRAL"),
        ("3. The second is to burn their stores of provisions", 
         lambda e: "PRO" if e.get("supply_line",5) < 4 else "NEUTRAL"),
        ("4. The third is to burn their baggage train", 
         lambda e: "PRO" if e.get("squad_value",0) < 200 else "NEUTRAL"),
        ("5. The fourth is to burn their arsenals and magazines", 
         lambda e: "PRO" if e.get("squad_depth",0) < 15 else "NEUTRAL"),
        ("6. The fifth is to hurl fire among them by launching burning projectiles", 
         lambda e: "PRO" if e.get("crowd_support",5) > 7 else "NEUTRAL"),
        ("7. Fire must be used as a weapon when conditions are right", 
         lambda e: "PRO" if e.get("weather","") in ["Wind","Storm","Dry"] else "NEUTRAL"),
        ("8. There are appropriate seasons for attacking with fire — dry weather and wind", 
         lambda e: "PRO" if e.get("weather","") in ["Clear","Wind"] else "NEUTRAL"),
        
        # ── RESPONDING TO FIRE ──
        ("9. When fire breaks out in the enemy's camp, respond immediately", 
         lambda e1,e2: "PRO" if e2.get("injuries",0) > 2 and e1.get("energy",50) > 60 else "NEUTRAL"),
        ("10. If the enemy's soldiers are quiet, wait and do not attack", 
         lambda e1,e2: "CON" if e2.get("discipline",5) > 6 and e1.get("energy",50) < 50 else "NEUTRAL"),
        ("11. When the fire reaches its height, attack if you can", 
         lambda e: "PRO" if e.get("momentum",0) > 2 and e.get("energy",50) > 70 else "NEUTRAL"),
        ("12. If you cannot, wait — do not force the moment", 
         lambda e: "CON" if e.get("energy",50) < 50 else "NEUTRAL"),
        ("13. Fire may be set from outside the enemy's camp — you need not enter", 
         lambda e: "PRO" if e.get("counter_attack",0) > 1 else "NEUTRAL"),
        ("14. Attack when the fire has done its damage, not before", 
         lambda e: "PRO" if e.get("intelligence",5) > 5 and e.get("momentum",0) > 0 else "NEUTRAL"),
        
        # ── THE USE OF EXTERNAL FORCES ──
        ("15. Those who use fire as a weapon are intelligent", 
         lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("16. Those who use water as a weapon are powerful", 
         lambda e: "PRO" if e.get("strength",5) > 7 else "NEUTRAL"),
        ("17. Water can isolate the enemy but cannot destroy their supplies", 
         lambda e: "NEUTRAL"),
        ("18. Fire can destroy everything the enemy possesses", 
         lambda e: "PRO" if e.get("weather","") in ["Dry","Wind"] else "NEUTRAL"),
        ("19. To win battles and capture enemy resources but fail to consolidate these gains is a waste", 
         lambda e: "CON" if e.get("goals_for",0) > 10 and e.get("form","").count("W") < 3 else "NEUTRAL"),
        ("20. This is called wasteful delay", 
         lambda e: "CON" if e.get("energy",50) < 40 and e.get("fixture_congestion",0) > 3 else "NEUTRAL"),
        ("21. The enlightened ruler lays his plans well ahead", 
         lambda e: "PRO" if e.get("preparation",5) > 6 else "NEUTRAL"),
        ("22. The good general cultivates his resources", 
         lambda e: "PRO" if e.get("squad_depth",0) > 20 and e.get("supply_line",5) > 5 else "NEUTRAL"),
        ("23. Move not unless you see an advantage", 
         lambda e: "PRO" if e.get("intelligence",5) > 5 and e.get("energy",50) > 50 else "NEUTRAL"),
        ("24. Use not your troops unless there is something to be gained", 
         lambda e: "PRO" if e.get("preparation",5) > 5 else "NEUTRAL"),
        ("25. Fight not unless the position is critical", 
         lambda e: "PRO" if e.get("must_win",False) else "NEUTRAL"),
        ("26. No ruler should put troops into the field merely to gratify his own anger", 
         lambda e: "CON" if e.get("discipline",5) < 4 and e.get("manager_quality",5) < 5 else "NEUTRAL"),
        ("27. No general should fight a battle simply out of pique", 
         lambda e: "CON" if e.get("discipline",5) < 4 and e.get("intelligence",5) < 5 else "NEUTRAL"),
        ("28. If it is to your advantage, advance — if not, stay where you are", 
         lambda e1,e2: "PRO" if e1.get("strength",5) > e2.get("strength",5) else "CON" if e2.get("strength",5) > e1.get("strength",5)*1.2 else "NEUTRAL"),
        ("29. Anger may change to joy, but a kingdom destroyed cannot be restored", 
         lambda e: "NEUTRAL"),
        ("30. The dead cannot be brought back to life", 
         lambda e: "NEUTRAL"),
        ("31. Therefore the enlightened ruler is prudent and the good general is cautious", 
         lambda e: "PRO" if e.get("intelligence",5) > 6 and e.get("manager_quality",5) > 6 else "NEUTRAL"),
        ("32. This is the way to keep the state at peace and the army intact", 
         lambda e: "PRO" if e.get("team_harmony",5) > 6 and e.get("discipline",5) > 6 else "NEUTRAL"),
    ]


if __name__ == "__main__":
    rules = CHAPTER_12_RULES()
    print(f"Chapter 12: {len(rules)} principles loaded")