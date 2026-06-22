"""
Shadow - Wyckoff Method Engine
Reads market structure: Accumulation, Distribution, Markup, Markdown.
Works hand in hand with Sun Tzu's strategic framework.

The Wyckoff Market Cycle:
1. Accumulation (Smart money buying quietly)
2. Markup (Price rises as public joins)
3. Distribution (Smart money selling to latecomers)
4. Markdown (Price falls as weak hands panic)
"""

import yfinance as yf
import pandas as pd
from datetime import datetime

class WyckoffEngine:
    def __init__(self, symbol="BTC-USD"):
        self.symbol = symbol
        self.data = {}
        self.load_data()
    
    def load_data(self):
        try:
            self.data['D'] = yf.Ticker(self.symbol).history(period="180d", interval="1d")
            self.data['4H'] = yf.Ticker(self.symbol).history(period="60d", interval="1h").resample('4h').agg({
                'Open':'first','High':'max','Low':'min','Close':'last','Volume':'sum'}).dropna()
            self.data['1H'] = yf.Ticker(self.symbol).history(period="14d", interval="1h")
            return True
        except:
            return False
    
    def get_stats(self, df):
        if df is None or df.empty: return {}
        close = float(df['Close'].iloc[-1])
        high = float(df['High'].max())
        low = float(df['Low'].min())
        volume = int(df['Volume'].mean()) if 'Volume' in df.columns else 0
        
        # Price range
        price_range = high - low
        position = (close - low) / max(price_range, 0.01)
        
        # Volume trend
        vol_5 = float(df['Volume'].iloc[-5:].mean()) if len(df) >= 5 else volume
        vol_20 = float(df['Volume'].iloc[-20:].mean()) if len(df) >= 20 else volume
        vol_rising = vol_5 > vol_20 * 1.2
        vol_declining = vol_5 < vol_20 * 0.8
        
        return {
            "close": round(close, 4),
            "high": round(high, 4),
            "low": round(low, 4),
            "position": round(position, 2),
            "volume": volume,
            "vol_5": int(vol_5),
            "vol_20": int(vol_20),
            "vol_rising": vol_rising,
            "vol_declining": vol_declining
        }
    
    def detect_phase(self):
        """
        Detect which Wyckoff phase the market is in.
        Uses price position, volume analysis, and price action.
        """
        daily = self.get_stats(self.data.get('D'))
        h4 = self.get_stats(self.data.get('4H'))
        
        if not daily or not h4:
            return {"phase": "UNKNOWN", "confidence": 0, "action": "WAIT"}
        
        pos_d = daily['position']
        vol_rising = daily['vol_rising']
        vol_declining = daily['vol_declining']
        
        # ═══════════════════════════════════════════════
        # PHASE 1: ACCUMULATION
        # Price at lows, volume declining on dips, increasing on rallies
        # Smart money buying quietly
        # ═══════════════════════════════════════════════
        if pos_d < 0.35 and not vol_declining:
            if vol_rising and pos_d > 0.2:
                phase = "LATE ACCUMULATION - Ready for Markup"
                confidence = 0.75
                action = "BUY - Position for breakout"
            else:
                phase = "EARLY ACCUMULATION - Smart money entering"
                confidence = 0.55
                action = "BUY - Scale in slowly at support"
        
        # ═══════════════════════════════════════════════
        # PHASE 2: MARKUP
        # Price rising, volume increasing on up days
        # The trend is established
        # ═══════════════════════════════════════════════
        elif pos_d > 0.35 and pos_d < 0.75 and vol_rising:
            phase = "MARKUP - Trend in motion"
            confidence = 0.80
            action = "BUY - Ride the trend, trail stops"
        
        # ═══════════════════════════════════════════════
        # PHASE 3: DISTRIBUTION
        # Price at highs, volume declining on rallies, increasing on dips
        # Smart money selling to latecomers
        # ═══════════════════════════════════════════════
        elif pos_d > 0.65 and vol_declining:
            if pos_d > 0.80:
                phase = "LATE DISTRIBUTION - Ready for Markdown"
                confidence = 0.75
                action = "SELL - Take profits, prepare for short"
            else:
                phase = "EARLY DISTRIBUTION - Smart money exiting"
                confidence = 0.60
                action = "SELL - Reduce longs, tighten stops"
        
        # ═══════════════════════════════════════════════
        # PHASE 4: MARKDOWN
        # Price falling, volume increasing on down days
        # Weak hands panic, smart money prepares to accumulate
        # ═══════════════════════════════════════════════
        elif pos_d < 0.35 and vol_rising and pos_d < 0.25:
            phase = "MARKDOWN - Trend declining"
            confidence = 0.80
            action = "SELL - Stay short or in cash"
        
        # ═══════════════════════════════════════════════
        # TRANSITIONAL / UNCLEAR
        # ═══════════════════════════════════════════════
        else:
            phase = "TRANSITION - Unclear phase"
            confidence = 0.30
            action = "WAIT - No clear Wyckoff signal"
        
        return {
            "phase": phase,
            "confidence": round(confidence, 2),
            "action": action,
            "position_in_range": pos_d,
            "volume_rising": vol_rising,
            "volume_declining": vol_declining
        }
    
    def detect_events(self):
        """
        Detect specific Wyckoff events:
        - Spring (false breakdown at support)
        - Upthrust (false breakout at resistance)
        - Sign of Strength (SOS) - high volume rally
        - Sign of Weakness (SOW) - high volume decline
        - Test - low volume retest of a level
        """
        daily = self.data.get('D')
        h4 = self.data.get('4H')
        
        if daily is None or daily.empty:
            return {}
        
        events = {}
        
        # Check last 5 candles for patterns
        last_5 = daily.iloc[-5:]
        last_close = float(last_5['Close'].iloc[-1])
        last_low = float(last_5['Low'].iloc[-1])
        last_high = float(last_5['High'].iloc[-1])
        last_vol = float(last_5['Volume'].iloc[-1])
        avg_vol = float(last_5['Volume'].mean())
        
        # Spring: price breaks below support then closes back above
        if last_low < float(daily['Low'].iloc[-20:].min()) * 1.01 and last_close > last_low * 1.02:
            events['spring'] = {"detected": True, "strength": "strong" if last_vol > avg_vol else "weak"}
        
        # Upthrust: price breaks above resistance then closes back below
        if last_high > float(daily['High'].iloc[-20:].max()) * 0.99 and last_close < last_high * 0.98:
            events['upthrust'] = {"detected": True, "strength": "strong" if last_vol > avg_vol else "weak"}
        
        # Sign of Strength: large bullish candle with high volume
        if float(last_5['Close'].iloc[-1]) > float(last_5['Open'].iloc[-1]) * 1.03 and last_vol > avg_vol * 1.5:
            events['sos'] = {"detected": True, "message": "Strong buying pressure"}
        
        # Sign of Weakness: large bearish candle with high volume
        if float(last_5['Close'].iloc[-1]) < float(last_5['Open'].iloc[-1]) * 0.97 and last_vol > avg_vol * 1.5:
            events['sow'] = {"detected": True, "message": "Strong selling pressure"}
        
        return events
    
    def full_analysis(self):
        """Complete Wyckoff analysis with phase detection and events."""
        phase = self.detect_phase()
        events = self.detect_events()
        
        return {
            "symbol": self.symbol,
            "wyckoff_phase": phase,
            "wyckoff_events": events,
            "timestamp": datetime.now().isoformat()
        }


if __name__ == "__main__":
    engine = WyckoffEngine("BTC-USD")
    result = engine.full_analysis()
    
    print("=" * 60)
    print("WYCKOFF ANALYSIS - BTC-USD")
    print("=" * 60)
    print(f"\nPhase: {result['wyckoff_phase']['phase']}")
    print(f"Confidence: {result['wyckoff_phase']['confidence']:.0%}")
    print(f"Action: {result['wyckoff_phase']['action']}")
    print(f"Position: {result['wyckoff_phase']['position_in_range']:.0%} in range")
    
    events = result['wyckoff_events']
    if events:
        print(f"\nDetected Events:")
        for name, data in events.items():
            print(f"  {name.upper()}: {data}")