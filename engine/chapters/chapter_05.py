"""Shadow - Chapter 5: Energy"""

def CHAPTER_5_RULES():
    return [
        # ── THE CONTROL OF FORCES ──
        ("1. The control of a large force is the same principle as the control of a few men", 
         lambda e: "PRO" if e.get("organization",5) > 6 else "NEUTRAL"),
        ("2. It is merely a question of dividing up their numbers", 
         lambda e: "PRO" if e.get("squad_depth",0) > 15 else "NEUTRAL"),
        ("3. Fighting with a large army under your command is no different from fighting with a small one", 
         lambda e: "PRO" if e.get("manager_quality",5) > 6 else "NEUTRAL"),
        ("4. It is merely a question of instituting signs and signals", 
         lambda e: "PRO" if e.get("discipline",5) > 6 else "NEUTRAL"),
        
        # ── DIRECT AND INDIRECT ──
        ("5. In all fighting, the direct method may be used for joining battle", 
         lambda e1,e2: "PRO" if e1.get("strength",5) > e2.get("strength",5) else "NEUTRAL"),
        ("6. But indirect methods will be needed in order to secure victory", 
         lambda e1,e2: "PRO" if e1.get("counter_attack",0) > e2.get("counter_attack",0) else "NEUTRAL"),
        ("7. Indirect tactics, efficiently applied, are inexhaustible as Heaven and Earth", 
         lambda e: "PRO" if e.get("formation_changes",0) > 2 and e.get("counter_attack",0) > 0 else "NEUTRAL"),
        ("8. The direct and the indirect lead on to each other in turn", 
         lambda e: "PRO" if e.get("possession",50) > 50 and e.get("counter_attack",0) > 0 else "NEUTRAL"),
        ("9. It is like moving in a circle — you never come to an end", 
         lambda e: "PRO" if e.get("formations",0) > 2 else "NEUTRAL"),
        ("10. Who can exhaust the possibilities of their combination?", 
         lambda e: "PRO" if e.get("intelligence",5) > 7 else "NEUTRAL"),
        
        # ── ENERGY AND TIMING ──
        ("11. The onset of troops is like the rush of a torrent", 
         lambda e: "PRO" if e.get("momentum",0) > 2 and e.get("energy",50) > 70 else "NEUTRAL"),
        ("12. The energy developed by good fighting men is as the momentum of a round stone rolled down a mountain", 
         lambda e1,e2: "PRO" if e1.get("momentum",0) > e2.get("momentum",0)+1 else "CON" if e2.get("momentum",0) > e1.get("momentum",0)+1 else "NEUTRAL"),
        ("13. Energy is the power that drives the attack — it must be harnessed and directed", 
         lambda e: "PRO" if e.get("energy",50) > 60 and e.get("trend","") == "bullish" else "NEUTRAL"),
        ("14. The quality of decision is like the well-timed swoop of a falcon", 
         lambda e: "PRO" if e.get("rsi",50) > 50 and e.get("rsi",50) < 70 else "NEUTRAL"),
        ("15. The falcon strikes at exactly the right moment to destroy its prey", 
         lambda e: "PRO" if e.get("momentum",0) > 1 and e.get("energy",50) > 65 else "NEUTRAL"),
        ("16. Timing is the art of releasing energy at the precise moment of maximum impact", 
         lambda e: "PRO" if 50 < e.get("rsi",50) < 70 and e.get("momentum",0) > 0 else "NEUTRAL"),
        
        # ── THE USE OF COMBINED ENERGY ──
        ("17. The clever combatant looks to the effect of combined energy", 
         lambda e: "PRO" if e.get("possession",50) > 55 and e.get("shots_on_target",0) > 5 else "NEUTRAL"),
        ("18. He does not require too much from individuals", 
         lambda e: "PRO" if e.get("squad_depth",0) > 20 else "NEUTRAL"),
        ("19. He takes individual talent into account and uses each man according to his capabilities", 
         lambda e: "PRO" if e.get("manager_quality",5) > 6 and e.get("squad_depth",0) > 18 else "NEUTRAL"),
        ("20. When he utilizes combined energy, his fighting men become like rolling logs or stones", 
         lambda e: "PRO" if e.get("team_harmony",5) > 6 and e.get("energy",50) > 60 else "NEUTRAL"),
        ("21. The weight of the combined force is unstoppable once set in motion", 
         lambda e1,e2: "PRO" if e1.get("strength",5) > e2.get("strength",5)*1.2 and e1.get("momentum",0) > 1 else "NEUTRAL"),
        
        # ── THE GENERAL'S ABILITY ──
        ("22. Thus the energy of one skilled in battle is overwhelming", 
         lambda e: "PRO" if e.get("energy",50) > 70 and e.get("form","").count("W") >= 3 else "NEUTRAL"),
        ("23. He selects his men and they combine their energy", 
         lambda e: "PRO" if e.get("manager_quality",5) > 6 and e.get("team_harmony",5) > 6 else "NEUTRAL"),
        ("24. He who can modify his tactics in relation to his opponent may be called heaven-born", 
         lambda e: "PRO" if e.get("formation_changes",0) > 2 and e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("25. The general must read the flow of battle and release energy at the decisive moment", 
         lambda e: "PRO" if e.get("momentum",0) > 0 and e.get("energy",50) > 60 and e.get("intelligence",5) > 5 else "NEUTRAL"),
    ]


if __name__ == "__main__":
    rules = CHAPTER_5_RULES()
    print(f"Chapter 5: {len(rules)} principles loaded")