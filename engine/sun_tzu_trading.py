"""
Shadow - Sun Tzu Trading Engine
Uses trading-specific chapters. All principles. Multi-timeframe.
"""

import yfinance as yf
from datetime import datetime
import sys, os, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data_mapper import map_trading

class SunTzuTrading:
    def __init__(self, symbol="BTC-USD"):
        self.symbol = symbol
        self.chapters = {}
        self.load_chapters()
        self.load_data()
    
    def load_chapters(self):
        """Load all available trading chapters."""
        for ch_num in range(1, 14):
            try:
                module = __import__(f"chapters_trading.chapter_{ch_num:02d}", fromlist=[f"CHAPTER_{ch_num}_RULES"])
                rules_func = getattr(module, f"CHAPTER_{ch_num}_RULES")
                self.chapters[ch_num] = rules_func()
            except Exception as e:
                pass  # Chapter not yet created
        
        total = sum(len(r) for r in self.chapters.values())
        loaded = ", ".join([f"Ch.{n}" for n in sorted(self.chapters.keys())])
        print(f"Trading Engine: {total} principles from {len(self.chapters)} chapters ({loaded})")
    
    def load_data(self):
        """Load multi-timeframe market data."""
        try:
            self.data = {}
            self.data['D'] = yf.Ticker(self.symbol).history(period="90d", interval="1d")
            self.data['4H'] = yf.Ticker(self.symbol).history(period="30d", interval="1h").resample('4h').agg({
                'Open':'first','High':'max','Low':'min','Close':'last','Volume':'sum'}).dropna()
            self.data['1H'] = yf.Ticker(self.symbol).history(period="7d", interval="1h")
            self.data['15M'] = yf.Ticker(self.symbol).history(period="5d", interval="15m")
        except:
            self.data = {}
    
    def get_stats(self, df):
        if df is None or df.empty: return {}
        close = float(df['Close'].iloc[-1])
        prev = float(df['Close'].iloc[-2]) if len(df) > 1 else close
        high = float(df['High'].max())
        low = float(df['Low'].min())
        atr = float((df['High'] - df['Low']).mean())
        change = ((close - prev) / prev) * 100
        
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0.0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0.0)).rolling(14).mean()
        rs = gain / loss
        rsi = float(100 - (100 / (1 + rs.iloc[-1]))) if loss.iloc[-1] != 0 else 50
        
        ma20 = float(df['Close'].rolling(20).mean().iloc[-1]) if len(df) >= 20 else close
        ma50 = float(df['Close'].rolling(50).mean().iloc[-1]) if len(df) >= 50 else ma20
        vol = int(df['Volume'].mean()) if 'Volume' in df.columns else 0
        trend = "bullish" if close > ma20 > ma50 else "bearish" if close < ma20 < ma50 else "neutral"
        
        price_range = high - low
        position = (close - low) / max(price_range, 0.01)
        
        return {
            "price": round(close, 4), "change_pct": round(change, 2),
            "rsi": round(rsi, 1), "atr": round(atr, 4),
            "high_30d": round(high, 4), "low_30d": round(low, 4),
            "trend": trend, "volume_avg": vol, "ma_20": round(ma20, 4),
            "ma_50": round(ma50, 4), "source": "YAHOO",
            "position_in_range": round(position, 2),
            "trend_strength": round(position if trend == "bullish" else (1-position) if trend == "bearish" else 0.5, 2),
        }
    
    def analyze(self):
        """Run trading chapters against market data."""
        if not self.chapters:
            return {"action": "WAIT", "error": "No trading chapters loaded"}
        
        # Get daily stats
        daily = self.get_stats(self.data.get('D'))
        if not daily: return {"action": "WAIT", "error": "No market data"}
        
        m15 = self.get_stats(self.data.get('15M'))
        
        # Map to Sun Tzu keys
        asset = map_trading(daily)
        asset["name"] = self.symbol
        
        # Add trading-specific keys
        asset["capital_risk"] = 3
        asset["stop_loss_set"] = True
        asset["entry_trigger"] = m15.get("trend") == "bullish" and 45 < m15.get("rsi",50) < 65
        asset["at_support"] = asset.get("position_in_range",0) < 0.35
        asset["at_resistance"] = asset.get("position_in_range",0) > 0.65
        asset["tf_alignment"] = 0.5
        asset["patience"] = 7
        asset["setup_quality"] = 6 if asset.get("trend") == "bullish" else 4
        asset["risk_management"] = 7
        asset["rr_ratio"] = 2.0
        asset["take_profit_pct"] = 3.0
        asset["profit_factor"] = 1.5 if asset.get("trend") == "bullish" else 0.8
        asset["spread_cost"] = 0.1
        asset["position_size"] = 5
        asset["drawdown"] = 10
        
        enemy = map_trading({"name":"USD","price":1,"change_pct":-0.1,"rsi":48,"trend":"neutral","volume_avg":100000})
        enemy["name"] = "USD"
        
        # Run all principles
        all_scores = []
        for ch_num in sorted(self.chapters.keys()):
            for name, fn in self.chapters[ch_num]:
                try:
                    result = fn(asset, enemy)
                except TypeError:
                    try:
                        result = fn(asset)
                    except:
                        result = "NEUTRAL"
                except:
                    result = "NEUTRAL"
                all_scores.append((ch_num, name, result))
        
        pro = sum(1 for _, _, r in all_scores if r == "PRO")
        con = sum(1 for _, _, r in all_scores if r == "CON")
        neu = sum(1 for _, _, r in all_scores if r == "NEUTRAL")
        
        action = "BUY" if pro > con else "SELL" if con > pro else "WAIT"
        
        entry = m15.get("price", daily.get("price", 0))
        atr = m15.get("atr", entry * 0.005)
        
        return {
            "symbol": self.symbol,
            "action": action,
            "entry": entry,
            "stop_loss": round(entry - atr * 1.5, 2) if action == "BUY" else round(entry + atr * 1.5, 2),
            "take_profit": round(entry + atr * 3, 2) if action == "BUY" else round(entry - atr * 3, 2),
            "pro_count": pro, "con_count": con, "neutral_count": neu,
            "total_principles": len(all_scores),
            "confidence": round(max(pro, con) / len(all_scores), 2) if all_scores else 0,
            "timestamp": datetime.now().isoformat()
        }


if __name__ == "__main__":
    engine = SunTzuTrading("BTC-USD")
    r = engine.analyze()
    print(f"\nAction: {r['action']}")
    print(f"Entry: ${r['entry']:,.2f}")
    print(f"SL: ${r['stop_loss']:,.2f} | TP: ${r['take_profit']:,.2f}")
    print(f"Vote: {r['pro_count']}P/{r['con_count']}C/{r['neutral_count']}N of {r['total_principles']}")