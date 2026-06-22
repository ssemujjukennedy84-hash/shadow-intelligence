"""Shadow - Chapter 9: The Army on the March"""

def CHAPTER_9_RULES():
    return [
        # ── POSITIONING THE ARMY ──
        ("1. Camp in high places, facing the sun", 
         lambda e: "PRO" if e.get("altitude",0) > 500 and e.get("weather","") in ["Clear","Cloudy"] else "NEUTRAL"),
        ("2. Do not climb heights in order to fight", 
         lambda e1,e2: "CON" if e2.get("altitude",0) > e1.get("altitude",0)+500 else "NEUTRAL"),
        ("3. After crossing a river, get far away from it", 
         lambda e: "NEUTRAL"),
        ("4. When an invading force crosses a river, do not meet it at the water's edge", 
         lambda e: "PRO" if e.get("counter_attack",0) > 1 else "NEUTRAL"),
        ("5. Let half the enemy cross first, then strike", 
         lambda e: "PRO" if e.get("counter_attack",0) > 0 and e.get("intelligence",5) > 5 else "NEUTRAL"),
        ("6. Pass quickly over mountains and keep close to valleys", 
         lambda e: "NEUTRAL"),
        ("7. In dry level country, take up an easily accessible position", 
         lambda e: "PRO" if e.get("pitch_condition","good") == "good" else "NEUTRAL"),
        ("8. Country of high grass and thick vegetation is ideal for ambush", 
         lambda e: "PRO" if e.get("counter_attack",0) > 1 else "NEUTRAL"),
        
        # ── READING ENEMY SIGNALS ──
        ("9. When the enemy is close at hand and remains quiet, he is relying on the natural strength of his position", 
         lambda e1,e2: "CON" if e2.get("strength",5) > e1.get("strength",5)*1.3 and e2.get("energy",50) < 50 else "NEUTRAL"),
        ("10. When he is at a distance and tries to provoke a battle, he wants you to advance", 
         lambda e1,e2: "CON" if e2.get("energy",50) > e1.get("energy",50) and e2.get("strength",5) > e1.get("strength",5) else "NEUTRAL"),
        ("11. When the enemy's envoys speak humbly while preparations continue, they will advance", 
         lambda e1,e2: "PRO" if e2.get("media_pressure",5) < 4 and e2.get("preparation",5) > 6 else "NEUTRAL"),
        ("12. When their language is strong and they threaten, they will retreat", 
         lambda e1,e2: "CON" if e2.get("media_pressure",5) > 7 and e2.get("energy",50) < 50 else "NEUTRAL"),
        ("13. Humble words followed by increased preparations signal attack", 
         lambda e1,e2: "PRO" if e2.get("preparation",5) > e1.get("preparation",5)+1 else "NEUTRAL"),
        ("14. Strong words without substance signal retreat", 
         lambda e1,e2: "PRO" if e2.get("energy",50) < 40 and e2.get("media_pressure",5) > 6 else "NEUTRAL"),
        ("15. When the enemy sees an advantage but does not advance, he is fatigued", 
         lambda e1,e2: "PRO" if e2.get("energy",50) < 40 and e1.get("strength",5) > e2.get("strength",5) else "NEUTRAL"),
        ("16. Birds rising in flight signals an ambush", 
         lambda e: "PRO" if e.get("counter_attack",0) > 2 else "NEUTRAL"),
        ("17. Startled beasts indicate a sudden attack", 
         lambda e: "PRO" if e.get("energy",50) > 70 else "NEUTRAL"),
        ("18. Dust rising in high straight columns indicates chariots approaching", 
         lambda e: "NEUTRAL"),
        ("19. Dust low and widespread indicates infantry advancing", 
         lambda e: "NEUTRAL"),
        ("20. When the enemy's soldiers whisper together in small groups, they have lost confidence", 
         lambda e1,e2: "PRO" if e2.get("team_harmony",5) < 5 else "NEUTRAL"),
        ("21. Too many punishments indicate extreme exhaustion", 
         lambda e: "CON" if e.get("discipline",5) < 4 and e.get("energy",50) < 40 else "NEUTRAL"),
        ("22. When the troops are disorderly, the general's authority is weak", 
         lambda e: "CON" if e.get("discipline",5) < 4 and e.get("manager_quality",5) < 5 else "NEUTRAL"),
        
        # ── JUDGING THE ENEMY ──
        ("23. If the enemy's troops are united in spirit, they will be difficult to defeat", 
         lambda e1,e2: "CON" if e2.get("team_harmony",5) > 7 and e2.get("morale",5) > 7 else "NEUTRAL"),
        ("24. If they are divided, they are vulnerable", 
         lambda e1,e2: "PRO" if e2.get("team_harmony",5) < 5 else "NEUTRAL"),
        ("25. When you outnumber the enemy, you may surround him", 
         lambda e1,e2: "PRO" if e1.get("strength",5) > e2.get("strength",5)*1.5 else "NEUTRAL"),
        ("26. Even when you are strong, appear weak to lure the enemy", 
         lambda e1,e2: "PRO" if e1.get("strength",5) > e2.get("strength",5) and e1.get("counter_attack",0) > 0 else "NEUTRAL"),
        ("27. He who is not thoughtful and treats his opponents with contempt will surely be captured", 
         lambda e: "CON" if e.get("preparation",5) < 4 and e.get("intelligence",5) < 5 else "NEUTRAL"),
        ("28. If soldiers are punished before they have grown attached to you, they will not be submissive", 
         lambda e: "CON" if e.get("discipline",5) > 7 and e.get("team_harmony",5) < 5 else "NEUTRAL"),
        ("29. If they are not punished after becoming attached, they will be useless", 
         lambda e: "CON" if e.get("discipline",5) < 4 and e.get("team_harmony",5) > 6 else "NEUTRAL"),
        ("30. Therefore soldiers must be treated with humanity but kept under control by iron discipline", 
         lambda e: "PRO" if e.get("team_harmony",5) > 5 and e.get("discipline",5) > 5 else "NEUTRAL"),
        ("31. This is the path to victory", 
         lambda e: "PRO" if e.get("discipline",5) > 5 and e.get("morale",5) > 6 else "NEUTRAL"),
    ]


if __name__ == "__main__":
    rules = CHAPTER_9_RULES()
    print(f"Chapter 9: {len(rules)} principles loaded")