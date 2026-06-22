"""Shadow - Chapter 7: Maneuvering"""

def CHAPTER_7_RULES():
    return [
        # ── THE DIFFICULTY OF MANEUVERING ──
        ("1. In war, the general receives his commands from the sovereign", 
         lambda e: "PRO" if e.get("manager_quality",5) > 6 else "NEUTRAL"),
        ("2. Having collected an army and concentrated his forces, he must blend and harmonize them", 
         lambda e: "PRO" if e.get("team_harmony",5) > 6 and e.get("organization",5) > 5 else "NEUTRAL"),
        ("3. After that comes tactical maneuvering, and there is nothing more difficult", 
         lambda e: "PRO" if e.get("formation_changes",0) > 1 else "NEUTRAL"),
        ("4. The difficulty of tactical maneuvering consists in turning the devious into the direct", 
         lambda e: "PRO" if e.get("counter_attack",0) > 0 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("5. And turning misfortune into gain", 
         lambda e: "PRO" if e.get("comeback_wins",0) > 1 else "NEUTRAL"),
        ("6. To take a long and circuitous route after enticing the enemy out of the way", 
         lambda e1,e2: "PRO" if e1.get("counter_attack",0) > e2.get("counter_attack",0) and e1.get("energy",50) > 60 else "NEUTRAL"),
        ("7. And though starting after him, to contrive to reach the goal before him", 
         lambda e1,e2: "PRO" if e1.get("energy",50) > e2.get("energy",50)*1.2 else "NEUTRAL"),
        ("8. This shows knowledge of the artifice of deviation", 
         lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        
        # ── THE DANGERS OF MANEUVERING ──
        ("9. Maneuvering with an army is advantageous — with an undisciplined multitude, most dangerous", 
         lambda e1,e2: "CON" if e1.get("discipline",5) < 5 else "PRO" if e2.get("discipline",5) < 5 else "NEUTRAL"),
        ("10. A whole army may be robbed of its spirit if the general is not careful", 
         lambda e: "CON" if e.get("morale",5) < 5 and e.get("manager_quality",5) < 5 else "NEUTRAL"),
        ("11. The strongest men will be exhausted and the weakest will fall behind", 
         lambda e: "CON" if e.get("energy",50) < 40 and e.get("squad_depth",0) < 18 else "NEUTRAL"),
        ("12. If you march fifty miles to wrest an advantage, only half your force will arrive", 
         lambda e: "CON" if e.get("travel_distance",0) > 3000 else "NEUTRAL"),
        ("13. If you march thirty miles, two-thirds will arrive", 
         lambda e: "CON" if e.get("travel_distance",0) > 1500 else "NEUTRAL"),
        ("14. An army without its baggage train is lost", 
         lambda e: "CON" if e.get("supply_line",5) < 4 else "NEUTRAL"),
        ("15. Without provisions it is lost", 
         lambda e: "CON" if e.get("energy",50) < 30 else "NEUTRAL"),
        ("16. Without bases of supply it is lost", 
         lambda e: "CON" if e.get("home_away","") != "home" and e.get("travel_distance",0) > 2000 else "NEUTRAL"),
        
        # ── KNOWLEDGE OF THE ENEMY ──
        ("17. We cannot enter into alliances until we are acquainted with the designs of our neighbors", 
         lambda e: "PRO" if e.get("intelligence",5) > 6 else "NEUTRAL"),
        ("18. We are not fit to lead an army on the march unless we are familiar with the face of the country", 
         lambda e: "PRO" if e.get("pitch_condition","good") == "good" and e.get("home_away","") == "home" else "NEUTRAL"),
        ("19. Its mountains and forests, its pitfalls and precipices, its marshes and swamps", 
         lambda e: "PRO" if e.get("altitude",0) > 0 and e.get("weather","") not in ["Storm","Snow"] else "NEUTRAL"),
        ("20. We shall be unable to turn natural advantage to account unless we make use of local guides", 
         lambda e: "PRO" if e.get("home_away","") == "home" else "NEUTRAL"),
        
        # ── DECEPTION IN MANEUVERING ──
        ("21. In war, practice dissimulation and you will succeed", 
         lambda e1,e2: "PRO" if e1.get("counter_attack",0) > e2.get("counter_attack",0) else "NEUTRAL"),
        ("22. Move only if there is a real advantage to be gained", 
         lambda e: "PRO" if e.get("intelligence",5) > 5 and e.get("energy",50) > 50 else "NEUTRAL"),
        ("23. Whether to concentrate or to divide your troops must be decided by circumstances", 
         lambda e: "PRO" if e.get("formation_changes",0) > 1 else "NEUTRAL"),
        ("24. Let your rapidity be that of the wind", 
         lambda e1,e2: "PRO" if e1.get("energy",50) > e2.get("energy",50)*1.2 else "NEUTRAL"),
        ("25. Your compactness that of the forest", 
         lambda e: "PRO" if e.get("team_harmony",5) > 6 and e.get("discipline",5) > 6 else "NEUTRAL"),
        ("26. In raiding and plundering be like fire", 
         lambda e: "PRO" if e.get("goals_for",0) > 10 and e.get("energy",50) > 60 else "NEUTRAL"),
        ("27. In immovability like a mountain", 
         lambda e: "PRO" if e.get("clean_sheets",0) > 4 else "NEUTRAL"),
        ("28. In movement be like the thunderbolt", 
         lambda e: "PRO" if e.get("momentum",0) > 2 and e.get("energy",50) > 70 else "NEUTRAL"),
        ("29. When you plunder the countryside, let the spoil be divided amongst your men", 
         lambda e: "PRO" if e.get("crowd_support",5) > 6 else "NEUTRAL"),
        ("30. When you capture new territory, cut it up into allotments", 
         lambda e: "PRO" if e.get("squad_value",0) > 300 else "NEUTRAL"),
        ("31. Ponder and deliberate before you make a move", 
         lambda e: "PRO" if e.get("preparation",5) > 6 else "NEUTRAL"),
        ("32. He will conquer who has learnt the artifice of deviation", 
         lambda e: "PRO" if e.get("counter_attack",0) > 1 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("33. Such is the art of maneuvering", 
         lambda e: "PRO" if e.get("formation_changes",0) > 2 else "NEUTRAL"),
    ]


if __name__ == "__main__":
    rules = CHAPTER_7_RULES()
    print(f"Chapter 7: {len(rules)} principles loaded")