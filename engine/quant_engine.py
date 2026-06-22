import sqlite3
from datetime import datetime
from typing import Dict

CHAPTER_WEIGHTS_TRADING = {1:1.0,2:1.0,3:1.0,4:0.8,5:1.5,6:1.2,7:0.9,8:0.7,9:1.0,10:0.8,11:0.8,12:0.5,13:1.3}
CHAPTER_WEIGHTS_SPORTS = {1:1.3,2:0.8,3:1.1,4:0.9,5:1.1,6:1.2,7:1.0,8:0.8,9:0.9,10:1.5,11:1.2,12:0.5,13:1.0}
SOURCE_RELIABILITY = {"Reuters":1.0,"Bloomberg":1.0,"AP":0.95,"BBC":0.9,"ESPN":0.85,"CNN":0.8,"CNBC":0.85,"WSJ":0.95,"FOREX.com":0.8,"Investing.com":0.75,"News":0.5}

class QuantEngine:
    def __init__(self, db_path="data/shadow_history.db"):
        self.db = sqlite3.connect(db_path, check_same_thread=False)
        self._init_db()
    
    def _init_db(self):
        self.db.execute("""CREATE TABLE IF NOT EXISTS predictions (id TEXT PRIMARY KEY, entity_1 TEXT, entity_2 TEXT, domain TEXT, league TEXT, s1 REAL, e1 REAL, m1 REAL, s2 REAL, e2 REAL, m2 REAL, pick TEXT, ground TEXT, heaven TEXT, margin REAL, confidence REAL, convergence REAL, chapter_used TEXT, timestamp TEXT, outcome TEXT, accuracy REAL)""")
        self.db.execute("""CREATE TABLE IF NOT EXISTS chapter_weights_v4 (chapter INTEGER, domain TEXT, league TEXT, correct INTEGER DEFAULT 0, total INTEGER DEFAULT 0, weight REAL DEFAULT 1.0, PRIMARY KEY(chapter, domain, league))""")
        self.db.execute("""CREATE TABLE IF NOT EXISTS no_signal_thresholds (domain TEXT PRIMARY KEY, margin_threshold REAL DEFAULT 0.5, confidence_threshold REAL DEFAULT 0.3)""")
        for dom in ["trading","sports"]:
            self.db.execute("INSERT OR IGNORE INTO no_signal_thresholds(domain) VALUES (?)",(dom,))
        self.db.commit()
    
    def score_trading(self, raw: dict) -> Dict[str, float]:
        price = raw.get("price",0); change = raw.get("change_pct",0)
        high = raw.get("high_30d",price); low = raw.get("low_30d",price)
        rsi = raw.get("rsi_14",50); trend = raw.get("trend","neutral")
        range_score = ((price - low) / (high - low)) * 10 if high > low else 5
        rsi_score = 10 if rsi > 70 else 3 if rsi < 30 else 5 + (rsi-50)/4
        trend_score = 8 if trend == "bullish" else 3 if trend == "bearish" else 5
        strength = round(range_score * 0.3 + rsi_score * 0.3 + trend_score * 0.4, 1)
        energy = min(100, max(10, abs(change) * 8 + (100-rsi if rsi > 50 else rsi) * 0.3))
        morale = 8 if change > 0 and rsi > 50 else 3 if change < 0 and rsi < 50 else 5
        intelligence = 8.0 if raw.get("source") == "YAHOO_FINANCE" else 4.0
        resources = min(100, max(10, raw.get("volume_avg",0) / 500000))
        return {"name":raw.get("name",""),"strength":strength,"energy":round(energy,1),"morale":morale,"intelligence":intelligence,"resources":round(resources,1),"momentum":round(change,2)}
    
    def score_sports(self, raw: dict) -> Dict[str, float]:
        wins = raw.get("wins",0) or 0; draws = raw.get("draws",0) or 0; losses = raw.get("losses",0) or 0
        played = wins + draws + losses
        gf = raw.get("goals_for",0) or 0; ga = raw.get("goals_against",0) or 0
        form_str = raw.get("form","") or ""
        if played == 0:
            founded = raw.get("founded","2000") or "2000"
            try: age = 2026 - int(str(founded)[:4]); strength = min(10, max(1, age/15))
            except: strength = 5.0
            return {"name":raw.get("name",""),"strength":round(strength,1),"energy":50,"morale":5,"intelligence":4,"resources":50,"momentum":0.0}
        win_rate = wins / max(played, 1)
        goal_diff = (gf - ga) / max(played, 1)
        form_score = form_str.count("W") / max(len(form_str), 1) * 10 if form_str else 5
        strength = round(win_rate * 5 + max(0, min(5, goal_diff * 2.5)) + form_score * 0.3, 1)
        strength = max(1, min(10, strength))
        energy = min(100, max(10, form_score * 8))
        recent = form_str[-3:] if len(form_str) >= 3 else form_str
        morale = 9 if recent.count("W") >= 2 else 5 if recent.count("W") >= 1 else 3
        intelligence = 8 if raw.get("source") == "FOOTBALL_DATA_ORG" else 5
        resources = energy
        return {"name":raw.get("name",""),"strength":strength,"energy":round(energy,1),"morale":morale,"intelligence":intelligence,"resources":round(resources,1),"momentum":form_score/2}
    
    def score_news(self, articles: list) -> Dict[str, float]:
        total_sentiment, total_weight = 0, 0
        for a in articles:
            source = a.get("source","Unknown"); title = a.get("title","")
            reliability = SOURCE_RELIABILITY.get(source, 0.5)
            published = a.get("published","")
            if published:
                try:
                    pub_time = datetime.fromisoformat(published.replace("Z",""))
                    hours_old = (datetime.now() - pub_time).total_seconds() / 3600
                    decay = 0.5 ** (hours_old / 6)
                except: decay = 0.5
            else: decay = 0.5
            positive = ["win","gain","rise","bull","growth","beat","strong","record","high","victory"]
            negative = ["lose","loss","fall","bear","drop","weak","crash","low","risk","defeat"]
            tl = title.lower()
            pos = sum(1 for w in positive if w in tl); neg = sum(1 for w in negative if w in tl)
            sentiment = (pos - neg) / max(pos + neg, 1)
            total_sentiment += sentiment * reliability * decay
            total_weight += reliability * decay
        avg = total_sentiment / max(total_weight, 0.01)
        conf = min(1.0, total_weight / len(articles)) if articles else 0
        return {"sentiment":round(avg,3),"confidence":round(conf,3),"article_count":len(articles)}
    
    def compute_overall(self, q1: dict, q2: dict, news1: dict, news2: dict, domain: str) -> dict:
        s1 = q1["strength"]*0.35 + (q1["energy"]/10)*0.25 + q1["morale"]*0.20 + (q1["resources"]/10)*0.10 + q1["intelligence"]*0.10
        s2 = q2["strength"]*0.35 + (q2["energy"]/10)*0.25 + q2["morale"]*0.20 + (q2["resources"]/10)*0.10 + q2["intelligence"]*0.10
        s1 *= (1 + news1["sentiment"] * 0.10 * news1["confidence"])
        s2 *= (1 + news2["sentiment"] * 0.10 * news2["confidence"])
        s1, s2 = round(max(1, min(10, s1)), 1), round(max(1, min(10, s2)), 1)
        margin = round(abs(s1 - s2), 1)
        if s1 >= s2: pick, ps, opps = q1.get("name","Entity 1"), s1, s2
        else: pick, ps, opps = q2.get("name","Entity 2"), s2, s1
        ground = "accessible" if margin > 3 else "contentious" if margin > 1 else "steep_heights"
        md = q1.get("momentum",0) - q2.get("momentum",0)
        heaven = "wind_favorable" if md > 1 else "wind_unfavorable" if md < -1 else "clear"
        confidence = min(1.0, (margin/10) + (news1["confidence"]+news2["confidence"])/4)
        return {"entity_1_name":q1.get("name",""),"entity_2_name":q2.get("name",""),"entity_1_strength":s1,"entity_1_energy":q1["energy"],"entity_1_morale":q1["morale"],"entity_2_strength":s2,"entity_2_energy":q2["energy"],"entity_2_morale":q2["morale"],"pick":pick,"pick_score":ps,"opponent_score":opps,"ground":ground,"heaven":heaven,"margin":margin,"confidence":round(confidence,2),"domain":domain}
    
    def no_signal_check(self, scores: dict) -> bool:
        row = self.db.execute("SELECT margin_threshold, confidence_threshold FROM no_signal_thresholds WHERE domain=?",(scores.get("domain","sports"),)).fetchone()
        mt, ct = (row[0], row[1]) if row else (0.5, 0.3)
        return scores.get("margin",0) < mt and scores.get("confidence",0) < ct
    
    def get_weights(self, domain: str, league: str = "default") -> dict:
        rows = self.db.execute("SELECT chapter, weight FROM chapter_weights_v4 WHERE domain=? AND league=?",(domain,league)).fetchall()
        if rows: return {r[0]:r[1] for r in rows}
        rows = self.db.execute("SELECT chapter, weight FROM chapter_weights_v4 WHERE domain=? AND league='default'",(domain,)).fetchall()
        if rows: return {r[0]:r[1] for r in rows}
        return CHAPTER_WEIGHTS_TRADING if domain=="trading" else CHAPTER_WEIGHTS_SPORTS
    
    def update_weights(self, chapter: int, domain: str, league: str, correct: bool):
        self.db.execute("INSERT OR IGNORE INTO chapter_weights_v4(chapter,domain,league) VALUES (?,?,?)",(chapter,domain,league))
        self.db.execute("UPDATE chapter_weights_v4 SET correct=correct+?, total=total+1 WHERE chapter=? AND domain=? AND league=?",(1 if correct else 0,chapter,domain,league))
        row = self.db.execute("SELECT correct,total FROM chapter_weights_v4 WHERE chapter=? AND domain=? AND league=?",(chapter,domain,league)).fetchone()
        if row and row[1] >= 10:
            wr = row[0]/row[1]
            nw = max(0.5, min(1.5, 1.0 + (wr-0.5)*1.5)) if row[1] < 50 else max(0.3, min(2.0, 1.0 + (wr-0.5)*2))
            self.db.execute("UPDATE chapter_weights_v4 SET weight=? WHERE chapter=? AND domain=? AND league=?",(round(nw,2),chapter,domain,league))
        self.db.commit()
    
    def record_outcome(self, pred_id: str, was_correct: bool, domain: str, league: str, chapter_scores: dict):
        self.db.execute("UPDATE predictions SET outcome=?, accuracy=? WHERE id=?",("correct" if was_correct else "incorrect",1 if was_correct else 0,pred_id))
        for ch, correct in chapter_scores.items(): self.update_weights(ch, domain, league, correct)
        self.db.commit()
    
    def save_prediction(self, pred_id: str, data: dict):
        self.db.execute("INSERT OR REPLACE INTO predictions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(pred_id,data.get("entity_1_name",""),data.get("entity_2_name",""),data.get("domain",""),data.get("league","default"),data.get("entity_1_strength",0),data.get("entity_1_energy",0),data.get("entity_1_morale",0),data.get("entity_2_strength",0),data.get("entity_2_energy",0),data.get("entity_2_morale",0),data.get("pick",""),data.get("ground",""),data.get("heaven",""),data.get("margin",0),data.get("confidence",0),data.get("convergence",0),data.get("chapter_used",""),datetime.now().isoformat(),"pending",0))
        self.db.commit()
    
    def get_win_rate(self, domain: str = None) -> float:
        q = "SELECT AVG(accuracy) FROM predictions WHERE outcome!='pending'"
        if domain: q += f" AND domain='{domain}'"
        r = self.db.execute(q).fetchone()
        return round((r[0] or 0), 2)