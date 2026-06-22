"""
SHADOW TRADING BOT - UNLOCKED
Uses CombinedTrading but overrides Wyckoff when Sun Tzu is strong
"""

import yfinance as yf
from engine.combined_trading import CombinedTrading
from engine.sun_tzu_engine import SunTzuEngine
import time
import json
from datetime import datetime

class ShadowTradingBot:
    def __init__(self, symbol):
        self.symbol = symbol
        self.engine = CombinedTrading(symbol)
        self.load_data()
        
    def load_data(self):
        """Load real data for all timeframes"""
        ticker = yf.Ticker(self.symbol)
        self.engine.data = {
            "D": ticker.history(period="30d", interval="1d"),
            "4H": ticker.history(period="30d", interval="4h"),
            "1H": ticker.history(period="14d", interval="1h"),
            "15M": ticker.history(period="7d", interval="15m")
        }
        # Get current price
        self.current_price = ticker.history(period="1d")['Close'].iloc[-1]
        
    def analyze(self):
        """Run analysis and unlock signals"""
        result = self.engine.analyze()
        
        sun_tzu = result.get('sun_tzu', {})
        pro = sun_tzu.get('pro', 0)
        con = sun_tzu.get('con', 0)
        diff = pro - con
        wyckoff = result.get('wyckoff', {}).get('phase', 'UNKNOWN')
        
        # Calculate execution levels
        entry = self.current_price
        stop_loss = entry * 0.97  # 3% stop loss
        take_profit = entry * 1.05  # 5% take profit
        risk_reward = round((take_profit - entry) / (entry - stop_loss), 2) if entry != stop_loss else 0
        
        # DECISION RULES
        if diff >= 150:
            action = "BUY"
            confidence = "HIGH"
            reason = f"Sun Tzu strongly bullish ({pro} PRO vs {con} CON, diff={diff})"
        elif diff >= 100:
            action = "BUY"
            confidence = "MEDIUM"
            reason = f"Sun Tzu bullish ({pro} PRO vs {con} CON)"
        elif diff <= -150:
            action = "SELL"
            confidence = "HIGH"
            reason = f"Sun Tzu strongly bearish ({pro} PRO vs {con} CON)"
        elif diff <= -100:
            action = "SELL"
            confidence = "MEDIUM"
            reason = f"Sun Tzu bearish ({pro} PRO vs {con} CON)"
        elif result.get('action') != "WAIT":
            action = result.get('action')
            confidence = result.get('confidence', 'MEDIUM')
            reason = f"Combined signal: {action}"
        else:
            action = "WAIT"
            confidence = "LOW"
            reason = f"Signals mixed. Sun Tzu diff={diff}, Wyckoff={wyckoff}"
        
        return {
            "symbol": self.symbol,
            "timestamp": datetime.now().isoformat(),
            "price": entry,
            "action": action,
            "confidence": confidence,
            "reason": reason,
            "sun_tzu": {"pro": pro, "con": con, "diff": diff},
            "wyckoff": wyckoff,
            "timeframes": result.get('timeframes', {}),
            "execution": {
                "entry": round(entry, 2),
                "stop_loss": round(stop_loss, 2),
                "take_profit": round(take_profit, 2),
                "risk_reward": risk_reward
            }
        }
    
    def print_signal(self, signal):
        """Print signal in a readable format"""
        print("\n" + "=" * 60)
        print(f"🔶 {signal['symbol']} - SHADOW TRADING SIGNAL")
        print("=" * 60)
        print(f"\n⏰ {signal['timestamp']}")
        print(f"💰 Price: ${signal['price']:.2f}")
        print(f"\n📊 SIGNAL: {signal['action']} (Confidence: {signal['confidence']})")
        print(f"   Reason: {signal['reason']}")
        print(f"\n📖 SUN TZU: PRO={signal['sun_tzu']['pro']} CON={signal['sun_tzu']['con']} DIFF={signal['sun_tzu']['diff']}")
        print(f"🌊 WYCKOFF: {signal['wyckoff']}")
        
        tf = signal.get('timeframes', {})
        if tf:
            print(f"\n⏰ TIMEFRAMES:")
            print(f"   Daily: {tf.get('daily', 'N/A')}")
            print(f"   4H:    {tf.get('4h', 'N/A')}")
            print(f"   1H:    {tf.get('1h', 'N/A')}")
            print(f"   15M:   {tf.get('15m', 'N/A')}")
        
        exec_data = signal.get('execution', {})
        if exec_data and signal['action'] != "WAIT":
            print(f"\n📈 TRADE LEVELS:")
            print(f"   Entry:       ${exec_data['entry']}")
            print(f"   Stop Loss:   ${exec_data['stop_loss']}")
            print(f"   Take Profit: ${exec_data['take_profit']}")
            print(f"   Risk/Reward: {exec_data['risk_reward']}")

def main():
    symbol = "BTC-USD"
    
    print("=" * 60)
    print("🔶 SHADOW TRADING BOT - UNLOCKED")
    print("   Overrides Wyckoff when Sun Tzu is strong")
    print("=" * 60)
    
    bot = ShadowTradingBot(symbol)
    signal = bot.analyze()
    bot.print_signal(signal)
    
    print("\n" + "=" * 60)
    print("📌 To use: python shadow_trading_bot.py")
    print("   Add to crontab for automatic signals")
    print("=" * 60)

if __name__ == "__main__":
    main()
