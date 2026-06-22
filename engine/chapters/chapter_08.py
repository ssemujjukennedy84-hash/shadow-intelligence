"""Shadow - Chapter 8: Variation in Tactics"""

def CHAPTER_8_RULES():
    return [
        # ── THE NEED FOR FLEXIBILITY ──
        ("1. In war, the general receives his commands from the sovereign, collects his army and concentrates his forces", 
         lambda e: "PRO" if e.get("manager_quality",5) > 5 and e.get("organization",5) > 5 else "NEUTRAL"),
        ("2. When in difficult country, do not encamp", 
         lambda e: "CON" if e.get("pitch_condition","") == "poor" else "NEUTRAL"),
        ("3. In country where high roads intersect, join hands with your allies", 
         lambda e: "PRO" if e.get("team_harmony",5) > 5 and e.get("home_away","") == "home" else "NEUTRAL"),
        ("4. Do not linger in dangerously isolated positions", 
         lambda e: "CON" if e.get("away_wins",0) < 2 and e.get("travel_distance",0) > 3000 else "NEUTRAL"),
        ("5. In hemmed-in situations, you must resort to stratagem", 
         lambda e: "PRO" if e.get("counter_attack",0) > 1 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("6. In desperate position, you must fight", 
         lambda e: "PRO" if e.get("must_win",False) else "NEUTRAL"),
        ("7. There are roads which must not be followed", 
         lambda e: "CON" if e.get("travel_distance",0) > 5000 and e.get("energy",50) < 50 else "NEUTRAL"),
        ("8. There are armies which must not be attacked", 
         lambda e1,e2: "CON" if e2.get("strength",5) > e1.get("strength",5)*1.5 else "NEUTRAL"),
        ("9. There are towns which must not be besieged", 
         lambda e1,e2: "CON" if e2.get("clean_sheets",0) > e1.get("goals_for",0) else "NEUTRAL"),
        ("10. There are positions which must not be contested", 
         lambda e1,e2: "CON" if e2.get("home_away","") == "home" and e2.get("strength",5) > e1.get("strength",5) else "NEUTRAL"),
        ("11. There are commands of the sovereign which must not be obeyed", 
         lambda e: "PRO" if e.get("manager_quality",5) > 7 else "NEUTRAL"),
        
        # ── THE GENERAL WHO UNDERSTANDS VARIATION ──
        ("12. The general who thoroughly understands the advantages that accompany variation of tactics knows how to handle his troops", 
         lambda e: "PRO" if e.get("formation_changes",0) > 2 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("13. The general who does not understand these may be well acquainted with the configuration of the country", 
         lambda e: "CON" if e.get("formation_changes",0) < 1 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("14. Yet he will not be able to turn his knowledge to practical account", 
         lambda e: "CON" if e.get("intelligence",5) > 5 and e.get("form","").count("L") >= 2 else "NEUTRAL"),
        ("15. The student of war who is unversed in the art of varying his plans will fail to make the best use of his men", 
         lambda e: "CON" if e.get("formation_changes",0) < 1 and e.get("squad_depth",0) > 15 else "NEUTRAL"),
        
        # ── THE FIVE DANGEROUS FAULTS ──
        ("16. There are five dangerous faults which may affect a general", 
         lambda e: "CON" if e.get("manager_quality",5) < 6 else "NEUTRAL"),
        ("17. Recklessness, which leads to destruction", 
         lambda e: "CON" if e.get("lead_lost",0) > 2 else "NEUTRAL"),
        ("18. Cowardice, which leads to capture", 
         lambda e: "CON" if e.get("comeback_wins",0) < 1 and e.get("losses",0) > 3 else "NEUTRAL"),
        ("19. A hasty temper, which can be provoked by insults", 
         lambda e: "CON" if e.get("discipline",5) < 4 else "NEUTRAL"),
        ("20. A delicacy of honor which is sensitive to shame", 
         lambda e: "CON" if e.get("media_pressure",5) > 7 else "NEUTRAL"),
        ("21. Over-solicitude for his men, which exposes him to worry and trouble", 
         lambda e: "CON" if e.get("team_harmony",5) > 8 and e.get("strength",5) < 6 else "NEUTRAL"),
        ("22. These five faults are the most dangerous in a general", 
         lambda e: "CON" if e.get("discipline",5) < 5 and e.get("manager_quality",5) < 5 else "NEUTRAL"),
        ("23. When an army is overthrown and its leader slain, the cause will surely be found among these five faults", 
         lambda e: "CON" if e.get("losses",0) > 5 else "NEUTRAL"),
        ("24. Let them be a subject of meditation", 
         lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        
        # ── ADAPTING TO CIRCUMSTANCES ──
        ("25. The wise general considers both favorable and unfavorable factors", 
         lambda e: "PRO" if e.get("intelligence",5) > 6 and e.get("preparation",5) > 6 else "NEUTRAL"),
        ("26. In the midst of difficulties he sees opportunity", 
         lambda e: "PRO" if e.get("comeback_wins",0) > 1 else "NEUTRAL"),
        ("27. In the midst of success he sees danger", 
         lambda e: "PRO" if e.get("clean_sheets",0) > 3 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("28. Reduce the hostile chiefs by inflicting damage on them", 
         lambda e1,e2: "PRO" if e1.get("goals_for",0) > e2.get("goals_for",0)*1.2 else "NEUTRAL"),
        ("29. Make trouble for them and keep them constantly engaged", 
         lambda e1,e2: "PRO" if e1.get("counter_attack",0) > e2.get("counter_attack",0) else "NEUTRAL"),
        ("30. Hold out specious allurements and make them rush to any given point", 
         lambda e: "PRO" if e.get("counter_attack",0) > 2 else "NEUTRAL"),
    ]


if __name__ == "__main__":
    rules = CHAPTER_8_RULES()
    print(f"Chapter 8: {len(rules)} principles loaded")