"""Shadow - Chapter 6: Weak Points and Strong"""

def CHAPTER_6_RULES():
    return [
        # ── SEIZING THE INITIATIVE ──
        ("1. Whoever is first in the field and awaits the coming of the enemy will be fresh for the fight", 
         lambda e1,e2: "PRO" if e1.get("rest_days",7) > e2.get("rest_days",7)+1 else "CON" if e2.get("rest_days",7) > e1.get("rest_days",7)+1 else "NEUTRAL"),
        ("2. Whoever is second in the field and has to hasten to battle will arrive exhausted", 
         lambda e1,e2: "CON" if e1.get("travel_distance",0) > e2.get("travel_distance",0) else "PRO" if e2.get("travel_distance",0) > e1.get("travel_distance",0) else "NEUTRAL"),
        ("3. The clever combatant imposes his will on the enemy", 
         lambda e1,e2: "PRO" if e1.get("possession",50) > 55 and e1.get("strength",5) > e2.get("strength",5) else "NEUTRAL"),
        ("4. He does not allow the enemy's will to be imposed on him", 
         lambda e: "PRO" if e.get("discipline",5) > 6 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("5. By holding out advantages to him, he can cause the enemy to approach of his own accord", 
         lambda e1,e2: "PRO" if e1.get("counter_attack",0) > e2.get("counter_attack",0) else "NEUTRAL"),
        ("6. By inflicting damage, he can make it impossible for the enemy to draw near", 
         lambda e1,e2: "PRO" if e1.get("goals_for",0) > e2.get("goals_for",0)*1.3 else "NEUTRAL"),
        
        # ── ATTACKING EMPTY SPACES ──
        ("7. Appear at points which the enemy must hasten to defend", 
         lambda e1,e2: "PRO" if e2.get("goals_against",0) > e1.get("goals_against",0)*1.3 else "CON" if e1.get("goals_against",0) > e2.get("goals_against",0)*1.3 else "NEUTRAL"),
        ("8. March swiftly to places where you are not expected", 
         lambda e1,e2: "PRO" if e1.get("counter_attack",0) > e2.get("counter_attack",0)+1 else "NEUTRAL"),
        ("9. You can be sure of succeeding in your attacks if you only attack places which are undefended", 
         lambda e1,e2: "PRO" if e2.get("clean_sheets",0) < 2 and e1.get("goals_for",0) > 10 else "NEUTRAL"),
        ("10. You can ensure the safety of your defense if you only hold positions that cannot be attacked", 
         lambda e: "PRO" if e.get("clean_sheets",0) > 4 and e.get("goals_against",0) < 8 else "NEUTRAL"),
        ("11. The general who is skilled in attack makes his enemy not know where to defend", 
         lambda e1,e2: "PRO" if e1.get("formation_changes",0) > 2 and e1.get("counter_attack",0) > 0 else "NEUTRAL"),
        ("12. He whose defense is hidden makes his enemy not know where to attack", 
         lambda e: "PRO" if e.get("clean_sheets",0) > 5 and e.get("intelligence",5) > 6 else "NEUTRAL"),
        
        # ── THE ART OF CONCEALMENT ──
        ("13. By discovering the enemy's dispositions and remaining invisible ourselves", 
         lambda e1,e2: "PRO" if e1.get("intelligence",5) > e2.get("intelligence",5)+1 else "CON" if e2.get("intelligence",5) > e1.get("intelligence",5)+1 else "NEUTRAL"),
        ("14. We can keep our forces concentrated while the enemy must be divided", 
         lambda e1,e2: "PRO" if e1.get("squad_depth",0) > e2.get("squad_depth",0) and e1.get("team_harmony",5) > e2.get("team_harmony",5) else "NEUTRAL"),
        ("15. We can form a single united body while the enemy must split into fractions", 
         lambda e1,e2: "PRO" if e1.get("team_harmony",5) > e2.get("team_harmony",5)+1 else "CON" if e2.get("team_harmony",5) > e1.get("team_harmony",5)+1 else "NEUTRAL"),
        ("16. The spot where we intend to fight must not be made known", 
         lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("17. The enemy must not know where I intend to give battle", 
         lambda e: "PRO" if e.get("counter_attack",0) > 1 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        
        # ── NUMERICAL SUPERIORITY AT THE POINT OF ATTACK ──
        ("18. If the enemy knows not where he will be attacked, he must prepare in every direction", 
         lambda e1,e2: "PRO" if e1.get("formation_changes",0) > 2 else "NEUTRAL"),
        ("19. And his forces being spread thin, I can concentrate overwhelming numbers at any point", 
         lambda e1,e2: "PRO" if e1.get("strength",5) > e2.get("strength",5)*1.3 and e1.get("squad_depth",0) > e2.get("squad_depth",0) else "NEUTRAL"),
        ("20. Numerical weakness comes from having to prepare against possible attacks", 
         lambda e: "CON" if e.get("injuries",0) > 3 and e.get("squad_depth",0) < 18 else "NEUTRAL"),
        ("21. Numerical strength comes from compelling our adversary to make these preparations against us", 
         lambda e: "PRO" if e.get("counter_attack",0) > 2 and e.get("strength",5) > 6 else "NEUTRAL"),
        
        # ── SHAPE AND ADAPTATION ──
        ("22. An army may march great distances without distress if it marches through country where the enemy is not", 
         lambda e: "PRO" if e.get("travel_distance",0) < 1000 and e.get("energy",50) > 50 else "NEUTRAL"),
        ("23. Military tactics are like unto water — water shapes its course according to the ground", 
         lambda e: "PRO" if e.get("formation_changes",0) > 2 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("24. The soldier works out his victory in relation to the foe whom he is facing", 
         lambda e: "PRO" if e.get("manager_quality",5) > 6 else "NEUTRAL"),
        ("25. Water retains no constant shape — so in warfare there are no constant conditions", 
         lambda e: "PRO" if e.get("formation_changes",0) > 1 else "NEUTRAL"),
        ("26. He who can modify his tactics in relation to his opponent may be called heaven-born", 
         lambda e: "PRO" if e.get("formation_changes",0) > 2 and e.get("intelligence",5) > 6 else "NEUTRAL"),
    ]


if __name__ == "__main__":
    rules = CHAPTER_6_RULES()
    print(f"Chapter 6: {len(rules)} principles loaded")