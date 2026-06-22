"""
Shadow - The Complete Art of War Master Engine
All 13 chapters. 460 principles.
"""

import sys, os

class SunTzuEngine:
    def __init__(self):
        self.chapters = {}
        chapter_names = {
            1: "Laying Plans", 2: "Waging War", 3: "Attack by Stratagem",
            4: "Tactical Dispositions", 5: "Energy", 6: "Weak Points and Strong",
            7: "Maneuvering", 8: "Variation in Tactics", 9: "The Army on the March",
            10: "Terrain", 11: "The Nine Situations", 12: "Attack by Fire", 13: "Use of Spies"
        }
        
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        imports = [
            (1, "chapters.chapter_01", "CHAPTER_1_RULES"),
            (2, "chapters.chapter_02", "CHAPTER_2_RULES"),
            (3, "chapters.chapter_03", "CHAPTER_3_RULES"),
            (4, "chapters.chapter_04", "CHAPTER_4_RULES"),
            (5, "chapters.chapter_05", "CHAPTER_5_RULES"),
            (6, "chapters.chapter_06", "CHAPTER_6_RULES"),
            (7, "chapters.chapter_07", "CHAPTER_7_RULES"),
            (8, "chapters.chapter_08", "CHAPTER_8_RULES"),
            (9, "chapters.chapter_09", "CHAPTER_9_RULES"),
            (10, "chapters.chapter_10", "CHAPTER_10_RULES"),
            (11, "chapters.chapter_11", "CHAPTER_11_RULES"),
            (12, "chapters.chapter_12", "CHAPTER_12_RULES"),
            (13, "chapters.chapter_13", "CHAPTER_13_RULES"),
        ]
        
        for ch_num, module_path, func_name in imports:
            try:
                module = __import__(module_path, fromlist=[func_name])
                rules_func = getattr(module, func_name)
                self.chapters[ch_num] = {
                    "name": chapter_names[ch_num],
                    "rules": rules_func()
                }
            except Exception as e:
                print(f"  Ch.{ch_num}: Not loaded - {e}")
        
        total = sum(len(ch["rules"]) for ch in self.chapters.values())
        loaded = ", ".join([f"Ch.{n}" for n in sorted(self.chapters.keys())])
        print(f"Sun Tzu Engine: {total} principles from {len(self.chapters)} chapters ({loaded})")
    
    def analyze(self, e1, e2):
        all_verdicts = []
        chapter_breakdown = []
        
        for ch_num in sorted(self.chapters.keys()):
            ch = self.chapters[ch_num]
            rules = ch["rules"]
            scores = []
            
            for name, fn in rules:
                try:
                    result = fn(e1, e2)
                    scores.append((ch_num, name, result))
                except TypeError:
                    try:
                        result = fn(e1)
                        scores.append((ch_num, name, result))
                    except:
                        scores.append((ch_num, name, "NEUTRAL"))
                except Exception:
                    scores.append((ch_num, name, "NEUTRAL"))
            
            pro = sum(1 for _, _, r in scores if r == "PRO")
            con = sum(1 for _, _, r in scores if r == "CON")
            neu = sum(1 for _, _, r in scores if r == "NEUTRAL")
            verdict = "PRO" if pro > con else "CON" if con > pro else "NEUTRAL"
            
            chapter_breakdown.append({
                "chapter": ch_num, "chapter_name": ch["name"],
                "verdict": verdict, "pro_rules": pro, "con_rules": con,
                "neutral_rules": neu, "total_rules": len(scores)
            })
            all_verdicts.extend(scores)
        
        total_pro = sum(1 for _, _, r in all_verdicts if r == "PRO")
        total_con = sum(1 for _, _, r in all_verdicts if r == "CON")
        total_neu = sum(1 for _, _, r in all_verdicts if r == "NEUTRAL")
        total = len(all_verdicts)
        
        pick = e1.get("name", "Entity 1") if total_pro >= total_con else e2.get("name", "Entity 2")
        
        return {
            "pick": pick,
            "pro_count": total_pro, "con_count": total_con, "neutral_count": total_neu,
            "total_principles": total,
            "convergence": round(max(total_pro, total_con) / total, 2) if total > 0 else 0,
            "chapter_breakdown": chapter_breakdown,
            "all_verdicts": all_verdicts
        }