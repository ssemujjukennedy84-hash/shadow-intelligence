"""Shadow - Chapter 2: Waging War"""

def CHAPTER_2_RULES():
    return [
        # ── THE COST OF WAR ──
        ("1. When war is declared, chariots, horses, armor and supplies must be gathered at enormous cost", 
         lambda e: "CON" if e.get("squad_value",0) < 100 else "NEUTRAL"),
        ("2. A hundred thousand men may be raised, but the daily expenditure is a thousand ounces of silver", 
         lambda e: "CON" if e.get("fixture_congestion",0) > 5 and e.get("squad_depth",0) < 20 else "NEUTRAL"),
        ("3. The cost of war drains the treasury, exhausts the people, and weakens the state", 
         lambda e: "CON" if e.get("energy",50) < 40 and e.get("played",0) > 20 else "NEUTRAL"),
        ("4. The army that takes the field must be fully provisioned or it will starve before reaching the enemy", 
         lambda e: "PRO" if e.get("supply_line",5) > 6 else "CON" if e.get("supply_line",5) < 3 else "NEUTRAL"),
        
        # ── THE DANGER OF PROLONGED WARFARE ──
        ("5. There is no instance of a country having benefited from prolonged warfare", 
         lambda e1,e2: "CON" if e1.get("fixture_congestion",0) > 5 else "PRO" if e2.get("fixture_congestion",0) > 5 else "NEUTRAL"),
        ("6. Protracted war exhausts the army's strength and dulls the edge of its weapons", 
         lambda e: "CON" if e.get("energy",50) < 40 and e.get("played",0) > 15 else "NEUTRAL"),
        ("7. Long campaigns drain morale, deplete resources, and leave the army vulnerable", 
         lambda e: "CON" if e.get("morale",5) < 5 and e.get("played",0) > 15 else "NEUTRAL"),
        ("8. The army's keen spirit wears down like a blade used too long without sharpening", 
         lambda e: "CON" if e.get("form","").count("L") >= 3 and e.get("played",0) > 10 else "NEUTRAL"),
        ("9. When your strength is exhausted, other kingdoms will rise against you", 
         lambda e: "CON" if e.get("strength",5) < 5 and e.get("played",0) > 20 else "NEUTRAL"),
        ("10. Even the wisest commander cannot repair the damage of a protracted campaign", 
         lambda e: "CON" if e.get("manager_quality",5) > 7 and e.get("energy",50) < 30 else "NEUTRAL"),
        
        # ── THE ESSENCE OF SPEED ──
        ("11. Rapidity is the essence of war", 
         lambda e1,e2: "PRO" if e1.get("energy",50) > e2.get("energy",50)*1.3 else "CON" if e2.get("energy",50) > e1.get("energy",50)*1.3 else "NEUTRAL"),
        ("12. Take advantage of the enemy's unreadiness", 
         lambda e1,e2: "PRO" if e1.get("preparation",5) > e2.get("preparation",5)+2 else "NEUTRAL"),
        ("13. Make your way by unexpected routes", 
         lambda e1,e2: "PRO" if e1.get("counter_attack",0) > e2.get("counter_attack",0) else "NEUTRAL"),
        ("14. Strike where the enemy has taken no precautions", 
         lambda e1,e2: "PRO" if e2.get("clean_sheets",0) < 2 else "NEUTRAL"),
        ("15. Speed turns advantage into decisive victory before the enemy can respond", 
         lambda e: "PRO" if e.get("energy",50) > 70 and e.get("form","").count("W") >= 2 else "NEUTRAL"),
        ("16. The swift completion of war saves lives, resources, and morale", 
         lambda e: "PRO" if e.get("energy",50) > 60 and e.get("played",0) < 10 else "NEUTRAL"),
        
        # ── RESOURCE STRATEGY ──
        ("17. A skilled general does not require a second levy of conscripts", 
         lambda e: "PRO" if e.get("squad_depth",0) > 20 else "NEUTRAL"),
        ("18. His provisions are not loaded more than twice", 
         lambda e: "PRO" if e.get("supply_line",5) > 6 else "NEUTRAL"),
        ("19. Bring war material from your own country", 
         lambda e: "PRO" if e.get("home_away","") == "home" else "NEUTRAL"),
        ("20. But forage on the enemy — use their resources against them", 
         lambda e1,e2: "PRO" if e1.get("goals_for",0) > e2.get("goals_for",0)*1.2 else "CON" if e2.get("goals_for",0) > e1.get("goals_for",0)*1.2 else "NEUTRAL"),
        ("21. One cartload of the enemy's provisions is equal to twenty of your own", 
         lambda e1,e2: "PRO" if e1.get("away_wins",0) > 0 and e2.get("goals_against",0) > e1.get("goals_against",0) else "NEUTRAL"),
        ("22. The cost of transporting supplies over long distances ruins the state's treasury", 
         lambda e: "CON" if e.get("travel_distance",0) > 5000 else "PRO" if e.get("travel_distance",0) < 500 else "NEUTRAL"),
        ("23. Supply lines must be short and secure, or the army will starve", 
         lambda e: "CON" if e.get("travel_distance",0) > 3000 and e.get("supply_line",5) < 5 else "NEUTRAL"),
        
        # ── MOTIVATION THROUGH CONQUEST ──
        ("24. Kill the enemy and men's anger is aroused at the spoils of victory", 
         lambda e: "PRO" if e.get("crowd_support",5) > 7 else "NEUTRAL"),
        ("25. In battle, reward the first to capture enemy resources — this motivates the entire army", 
         lambda e: "PRO" if e.get("first_half",0) > e.get("second_half",0) else "NEUTRAL"),
        ("26. Treat captured soldiers well and care for them — this is called winning hearts", 
         lambda e: "PRO" if e.get("team_harmony",5) > 6 else "NEUTRAL"),
        ("27. This is using the conquered foe to augment your own strength", 
         lambda e1,e2: "PRO" if e1.get("squad_value",0) > e2.get("squad_value",0) else "NEUTRAL"),
        ("28. Victory through integration is more efficient than victory through destruction", 
         lambda e: "PRO" if e.get("team_harmony",5) > 7 else "NEUTRAL"),
        ("29. The spoils of war should fuel the next campaign, not sit idle", 
         lambda e: "PRO" if e.get("energy",50) > 60 and e.get("squad_value",0) > 300 else "NEUTRAL"),
        
        # ── THE ULTIMATE OBJECTIVE ──
        ("30. In war, let your great object be victory — not lengthy campaigns", 
         lambda e1,e2: "PRO" if e1.get("goals_for",0) > e2.get("goals_for",0) and e1.get("goals_against",0) < e2.get("goals_against",0) else "CON" if e2.get("goals_for",0) > e1.get("goals_for",0) and e2.get("goals_against",0) < e1.get("goals_against",0) else "NEUTRAL"),
        ("31. Victory must be decisive, swift, and complete — not drawn out", 
         lambda e: "PRO" if e.get("form","").count("W") >= 3 and e.get("energy",50) > 60 else "NEUTRAL"),
        ("32. The general who understands the true cost of war is the guardian of the nation's fate", 
         lambda e: "PRO" if e.get("manager_quality",5) > 7 and e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("33. He must not let operations linger — delay costs lives, resources, and opportunity", 
         lambda e: "CON" if e.get("energy",50) < 50 and e.get("played",0) > 10 else "NEUTRAL"),
        ("34. The wise general attacks the enemy's strategy, not just their soldiers", 
         lambda e1,e2: "PRO" if e1.get("counter_attack",0) > e2.get("counter_attack",0) and e1.get("intelligence",5) > e2.get("intelligence",5) else "NEUTRAL"),
        ("35. Every moment of war consumes the nation's lifeblood — end it quickly", 
         lambda e: "CON" if e.get("fixture_congestion",0) > 5 and e.get("energy",50) < 50 else "NEUTRAL"),
    ]


if __name__ == "__main__":
    rules = CHAPTER_2_RULES()
    print(f"Chapter 2: {len(rules)} principles loaded")