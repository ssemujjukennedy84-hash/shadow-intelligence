import os, time
from groq import Groq

GROQ_KEY = "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"

CHAPTER_NAMES = [
    "", "Laying Plans", "Waging War", "Attack by Stratagem",
    "Tactical Dispositions", "Energy", "Weak Points and Strong",
    "Maneuvering", "Variation in Tactics", "The Army on the March",
    "Terrain", "The Nine Situations", "Attack by Fire", "Use of Spies"
]

class SunTzuMind:
    def __init__(self):
        self.client = Groq(api_key=GROQ_KEY)
        self.chapters = {}
        for i in range(1, 14):
            path = f'data/chapters/chapter_{i:02d}_{CHAPTER_NAMES[i].lower().replace(" ","_")}.txt'
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    self.chapters[i] = f.read()
        print(f"Loaded {len(self.chapters)} chapters")
    
    def _call(self, prompt):
        for attempt in range(3):
            try:
                chat = self.client.chat.completions.create(
                    messages=[{"role":"user","content":prompt}],
                    model="llama-3.3-70b-versatile", temperature=0.2, max_tokens=30
                )
                return chat.choices[0].message.content.strip()
            except Exception as e:
                if "429" in str(e): time.sleep(10)
                else: time.sleep(3)
        return ""
    
    def analyze(self, e1, e2, domain):
        e1n = e1.get('name','Entity 1')
        e2n = e2.get('name','Entity 2')
        data = f"{e1n}: STR{e1.get('strength',5)}/10 ENG{e1.get('energy',50)}/100 | {e2n}: STR{e2.get('strength',5)}/10 ENG{e2.get('energy',50)}/100"
        
        verdicts = []
        for ch in range(1, 14):
            ch_text = self.chapters.get(ch, "")[:1200]
            ch_name = CHAPTER_NAMES[ch]
            
            resp = self._call(f"Chapter {ch} ({ch_name}) of The Art of War:\n{ch_text}\n\n{data}\nBased ONLY on this chapter, who has advantage? Answer one word: PRO or CON")
            
            r = resp.upper().strip()
            v = "PRO" if r.startswith("PRO") else "CON" if r.startswith("CON") else "NEUTRAL"
            verdicts.append({"chapter":ch, "chapter_name":ch_name, "verdict":v})
            time.sleep(2)  # Rate limit: 30 req/min = 2s between calls
        
        pro = sum(1 for v in verdicts if v['verdict']=='PRO')
        con = sum(1 for v in verdicts if v['verdict']=='CON')
        pick = e1n if pro > con else e2n
        
        return {
            "pick": pick, "pro_count": pro, "con_count": con, "neutral_count": 13-pro-con,
            "battle_plan": f"{pro}/13 chapters support {pick}.",
            "convergence": round(max(pro,con)/13,2),
            "chapter_verdicts": verdicts
        }