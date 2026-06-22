import sys, os, json, concurrent.futures, requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine.art_of_war_rag import ArtOfWarRAG

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:1.5b"

CHAPTER_FEATURES = {
    1: "Fundamentals", 2: "Resources", 3: "Indirect Path", 4: "Defense",
    5: "Momentum", 6: "Asymmetries", 7: "Positioning", 8: "Adaptability",
    9: "Signals", 10: "Terrain", 11: "Situation", 12: "External Forces", 13: "Intelligence"
}
CHAPTER_NAMES = ["","Laying Plans","Waging War","Attack by Stratagem","Tactical Dispositions","Energy","Weak Points and Strong","Maneuvering","Variation in Tactics","The Army on the March","Terrain","The Nine Situations","Attack by Fire","Use of Spies"]

class ThirteenAudit:
    def __init__(self):
        self.rag = ArtOfWarRAG()
    
    def _ollama(self, prompt):
        try:
            r = requests.post(OLLAMA_URL, json={"model":MODEL,"prompt":prompt,"stream":False,"options":{"num_predict":60,"temperature":0.5}}, timeout=15)
            if r.status_code==200: return r.json().get("response","").strip()
        except: pass
        return ""
    
    def _audit_one(self, ch_num, scores):
        name = CHAPTER_NAMES[ch_num]
        focus = CHAPTER_FEATURES.get(ch_num, "Strategy")
        pick = scores.get("pick","")
        margin = scores.get("margin",0)
        ps = scores.get("pick_score",5)
        opps = scores.get("opponent_score",5)
        
        # Verdict from quant scores - the book's chapters agree/disagree based on margin
        if margin > 4: verdict, expl = "PRO", f"overwhelming {focus} advantage"
        elif margin > 2: verdict, expl = "PRO", f"clear {focus} edge"
        elif margin > 1: verdict, expl = "PRO", f"moderate {focus} lead"
        elif margin > 0.3: verdict, expl = "NEUTRAL", f"{focus} too close"
        else: verdict, expl = "CON", f"{focus} insufficient"
        
        # Get passage from this chapter
        passages = self.rag.search(f"{name}", n_results=1)
        pt = passages[0]['text'][:120] if passages else "Know your enemy and yourself."
        
        # Ollama adds the "why" in Sun Tzu's voice
        prompt = f"Chapter {ch_num} ({name}) of Art of War focuses on {focus}. Passage: \"{pt}\". The data shows {pick} leads by {margin} points ({ps} vs {opps}). Verdict: {verdict}. In 5 words, why does this chapter say {verdict}?"
        insight = self._ollama(prompt)
        
        return {
            "chapter": ch_num, "chapter_name": name,
            "verdict": verdict, "verdict_explanation": expl,
            "risk_score": max(1, min(10, 10 - margin)),
            "strategic_insight": insight or f"{verdict}: {expl}"
        }
    
    def run(self, raw1, raw2, scores, domain, chapter_weights, n1=None, n2=None, is_home_1=True, league="default"):
        # Run all 13 audits in parallel
        reports = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=13) as ex:
            futs = {ex.submit(self._audit_one, ch, scores): ch for ch in range(1,14)}
            for f in concurrent.futures.as_completed(futs):
                reports.append(f.result())
        reports.sort(key=lambda r: r.get("chapter",0))
        
        pro = sum(1 for r in reports if r.get("verdict")=="PRO")
        con = sum(1 for r in reports if r.get("verdict")=="CON")
        neu = sum(1 for r in reports if r.get("verdict")=="NEUTRAL")
        
        # Weighted convergence
        tw, wp = 0, 0
        for r in reports:
            w = chapter_weights.get(r.get("chapter",1),1.0)
            tw += w; 
            if r.get("verdict")=="PRO": wp += w
        conv = round(wp/tw,2) if tw>0 else 0.5
        
        # Primary chapter = highest weight
        best = max(reports, key=lambda r: chapter_weights.get(r.get("chapter",1),1.0))
        
        # Synthesizer prompt
        summaries = "\n".join([f"Ch.{r['chapter']} {r['chapter_name']}: {r['verdict']} - {r['strategic_insight']}" for r in reports])
        synth_prompt = f"13 chapters of Art of War analyzed {scores.get('entity_1_name','')} vs {scores.get('entity_2_name','')}.\n{summaries}\n\n{pro} PRO, {con} CON, {neu} NEUTRAL for {scores.get('pick','')}. Give: ANALYSIS (2 sentences on what the book reveals) and RECOMMENDATION (1 sentence action)."
        synth_resp = self._ollama(synth_prompt)
        
        def get(p):
            for l in synth_resp.split('\n'):
                if l.strip().upper().startswith(p.upper()): return l.split(':',1)[1].strip()
            return None
        
        return {
            **scores,
            "audit_reports": reports,
            "final_analysis": get("ANALYSIS") or f"{pro}/13 chapters support {scores.get('pick','')}.",
            "final_recommendation": get("RECOMMENDATION") or f"Back {scores.get('pick','')}.",
            "convergence_score": conv,
            "primary_chapter": f"Ch.{best['chapter']}: {best['chapter_name']}",
            "contradictions": [],
            "league": league
        }