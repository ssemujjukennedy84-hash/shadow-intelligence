"""
Shadow - Combined Trading Engine
Wyckoff Method (Market Structure) + Sun Tzu (506 Principles)
Multi-timeframe: Daily → 4H → 1H → 15M Execution
"""

import sys, os, yfinance as yf
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wyckoff.engine import WyckoffEngine

class CombinedTrading:
    def __init__(self, symbol="BTC-USD"):
        self.symbol = symbol
        self.wyckoff = WyckoffEngine(symbol)
        self.chapters = {}
        self._load_chapters()
        self._load_market_data()
    
    def _load_chapters(self):
        for ch_num in range(1, 14):
            try:
                module = __import__(f"chapters_trading.chapter_{ch_num:02d}", fromlist=[f"CHAPTER_{ch_num}_RULES"])
                self.chapters[ch_num] = getattr(module, f"CHAPTER_{ch_num}_RULES")()
            except: pass
        total = sum(len(r) for r in self.chapters.values())
        print(f"Sun Tzu: {total} principles | Wyckoff: Active | Timeframes: D/4H/1H/15M")
    
    def _load_market_data(self):
        try:
            self.data = {
                'D': yf.Ticker(self.symbol).history(period="90d", interval="1d"),
                '4H': yf.Ticker(self.symbol).history(period="30d", interval="1h").resample('4h').agg({
                    'Open':'first','High':'max','Low':'min','Close':'last','Volume':'sum'}).dropna(),
                '1H': yf.Ticker(self.symbol).history(period="7d", interval="1h"),
                '15M': yf.Ticker(self.symbol).history(period="5d", interval="15m"),
            }
        except:
            self.data = {}
    
    def _tf_stats(self, df):
        if df is None or df.empty: return {}
        close = float(df['Close'].iloc[-1])
        prev = float(df['Close'].iloc[-2]) if len(df) > 1 else close
        high = float(df['High'].max())
        low = float(df['Low'].min())
        atr = float((df['High'] - df['Low']).mean())
        change = ((close - prev) / prev) * 100
        vol = int(df['Volume'].mean()) if 'Volume' in df.columns else 0
        
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0.0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0.0)).rolling(14).mean()
        rs = gain / loss
        rsi = float(100 - (100 / (1 + rs.iloc[-1]))) if loss.iloc[-1] != 0 else 50
        
        ma20 = float(df['Close'].rolling(20).mean().iloc[-1]) if len(df) >= 20 else close
        trend = "bullish" if close > ma20 else "bearish"
        pos = (close - low) / max(high - low, 0.01)
        
        return {"close":round(close,4),"atr":round(atr,4),"rsi":round(rsi,1),"trend":trend,"volume":vol,"position":round(pos,2),"change":round(change,2)}
    
    def analyze(self):
        # Wyckoff phase
        try: wyckoff = self.wyckoff.full_analysis()
        except: return {"action":"WAIT","confidence":"NO DATA"}
        
        phase = wyckoff.get('wyckoff_phase', {})
        events = wyckoff.get('wyckoff_events', {})
        
        # Multi-timeframe stats
        d = self._tf_stats(self.data.get('D'))
        h4 = self._tf_stats(self.data.get('4H'))
        h1 = self._tf_stats(self.data.get('1H'))
        m15 = self._tf_stats(self.data.get('15M'))
        
        # Build asset data
        asset = {
            "name":self.symbol,"strength":7,"energy":60,"morale":7,"intelligence":7,
            "discipline":7,"manager_quality":7,"preparation":7,"organization":6,"team_harmony":6,
            "capital_risk":3,"stop_loss_set":True,"risk_management":7,
            "position_size":5,"drawdown":10,"rr_ratio":2.0,"take_profit_pct":3.0,
            "profit_factor":1.5,"spread_cost":0.1,"setup_quality":6,
            "patience":7,"entry_trigger":False,"tf_alignment":0.6,
            "comeback_wins":1,"counter_attack":1,"formation_changes":2,
            "trend_strength":0.6,"momentum":1,"squad_depth":20,"squad_value":300,
            "fixture_congestion":3,"played":50,"rest_days":5,"travel_distance":0,
            "home_away":"home","time_advantage":True,"season_advantage":True,
            "supply_line":7,"earth_score":6,"news_count":4,"data_freshness":1,
            "source":"YAHOO","form":"WWDLW","clean_sheets":2,"goals_for":10,
            "goals_against":5,"losses":1,"lead_lost":0,"volatility":d.get('close',0)*0.02,
        }
        
        # Inject real market data
        if d:
            asset["rsi"] = d.get('rsi', 50)
            asset["trend"] = d.get('trend', 'bullish')
            asset["position_in_range"] = d.get('position', 0.5)
            asset["at_support"] = d.get('position', 0.5) < 0.35
            asset["at_resistance"] = d.get('position', 0.5) > 0.65
            asset["trend_strength"] = 0.7 if d.get('trend') == 'bullish' else 0.3
            asset["momentum"] = d.get('change', 0) / 5
            asset["energy"] = min(100, max(10, abs(d.get('change',0))*5))
            asset["volatility"] = d.get('atr', d.get('close',0)*0.01)
        
        if h4:
            asset["earth_score"] = 7 if h4.get('trend') == d.get('trend') else 4
        if h1:
            asset["entry_trigger"] = h1.get('trend') == d.get('trend') and 40 < h1.get('rsi',50) < 70
        if m15:
            asset["execution_ready"] = m15.get('trend') == d.get('trend')
        
        # Wyckoff context
        asset["wyckoff_phase"] = phase.get('phase','UNKNOWN')
        asset["volume_rising"] = phase.get('volume_rising', False)
        asset["volume_declining"] = phase.get('volume_declining', False)
        
        if events.get('spring',{}).get('detected'): asset["at_support"] = True; asset["comeback_wins"] += 2
        if events.get('sos',{}).get('detected'): asset["momentum"] += 2; asset["trend_strength"] = 0.9
        if events.get('sow',{}).get('detected'): asset["momentum"] -= 2; asset["trend_strength"] = 0.2
        
        enemy = {"name":"USD","strength":5,"energy":50,"morale":5,"intelligence":5}
        
        # Run Sun Tzu
        scores = []
        for ch_num in sorted(self.chapters.keys()):
            for name, fn in self.chapters[ch_num]:
                try: scores.append(fn(asset, enemy))
                except TypeError:
                    try: scores.append(fn(asset))
                    except: scores.append("NEUTRAL")
                except: scores.append("NEUTRAL")
        
        pro = scores.count("PRO")
        con = scores.count("CON")
        
        # Combined decision
        w_act = phase.get('action','WAIT')
        s_act = "BUY" if pro > con else "SELL" if con > pro else "WAIT"
        
        if "BUY" in w_act and s_act == "BUY": action, conf = "BUY", "HIGH"
        elif "SELL" in w_act and s_act == "SELL": action, conf = "SELL", "HIGH"
        elif "WAIT" in w_act or s_act == "WAIT": action, conf = "WAIT", "NO SIGNAL"
        else: action, conf = "WAIT", "MIXED"
        
        result = {
            "symbol":self.symbol,"action":action,"confidence":conf,
            "wyckoff":{"phase":phase.get('phase','?'),"position":phase.get('position_in_range',0.5)},
            "sun_tzu":{"pro":pro,"con":con,"total":len(scores)},
            "timeframes":{"daily":d.get('trend','?'),"4h":h4.get('trend','?'),"1h":h1.get('trend','?'),"15m":m15.get('trend','?')},
        }
        
        # 15M Execution
        if action != "WAIT" and m15:
            entry = m15.get('close', 0)
            atr = m15.get('atr', entry*0.005)
            if action == "BUY":
                result["execution"] = {"entry":round(entry,2),"stop_loss":round(entry-atr*1.5,2),"take_profit":round(entry+atr*3,2)}
            else:
                result["execution"] = {"entry":round(entry,2),"stop_loss":round(entry+atr*1.5,2),"take_profit":round(entry-atr*3,2)}
        
        result["timestamp"] = datetime.now().isoformat()
        return result


if __name__ == "__main__":
    engine = CombinedTrading("BTC-USD")
    r = engine.analyze()
    
    print(f"\n{'='*50}")
    print(f"SHADOW TRADING: {r['symbol']}")
    print(f"{'='*50}")
    print(f"Action: {r['action']} ({r['confidence']})")
    print(f"Wyckoff: {r['wyckoff']['phase']} ({r['wyckoff']['position']:.0%} in range)")
    print(f"Sun Tzu: {r['sun_tzu']['pro']}P/{r['sun_tzu']['con']}C/{r['sun_tzu']['total']} principles")
    print(f"Timeframes: D:{r['timeframes']['daily']} 4H:{r['timeframes']['4h']} 1H:{r['timeframes']['1h']} 15M:{r['timeframes']['15m']}")
    
    ex = r.get('execution')
    if ex:
        print(f"\n15M EXECUTION:")
        print(f"  Entry: ${ex['entry']:,.2f}")
        print(f"  SL: ${ex['stop_loss']:,.2f} | TP: ${ex['take_profit']:,.2f}")