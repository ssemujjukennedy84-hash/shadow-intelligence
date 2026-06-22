"""
BACKTEST - UNLOCKED STRATEGY
Sun Tzu overrides Wyckoff when PRO > CON + 50
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict
import time

from engine.combined_trading import CombinedTrading
from engine.sun_tzu_engine import SunTzuEngine
from engine.quant_engine import QuantEngine
from engine.self_learner import SelfLearner

class BacktestUnlocked:
    def __init__(self):
        self.sun_tzu = SunTzuEngine()
        self.quant = QuantEngine()
        self.learner = SelfLearner()
        self.results = []
        self.total_trades = 0
        self.total_correct = 0
        self.total_profit = 0
        
    def fetch_data(self, symbol, period="6mo"):
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period)
            if len(df) > 0:
                return df
            return None
        except Exception as e:
            print(f"  Error: {e}")
            return None
    
    def get_signal(self, symbol, df, idx):
        """Get signal using UNLOCKED strategy"""
        lookback = df.iloc[:idx+1]
        
        if len(lookback) < 20:
            return {"action": "WAIT", "confidence": 0, "reason": "Insufficient data"}
        
        # Load data into CombinedTrading
        try:
            engine = CombinedTrading(symbol)
            # Load timeframes
            ticker = yf.Ticker(symbol)
            engine.data = {
                "D": ticker.history(period="30d", interval="1d"),
                "4H": ticker.history(period="30d", interval="4h"),
                "1H": ticker.history(period="14d", interval="1h"),
                "15M": ticker.history(period="7d", interval="15m")
            }
            result = engine.analyze()
        except Exception as e:
            return {"action": "WAIT", "confidence": 0, "reason": f"Engine error: {e}"}
        
        # Get Sun Tzu counts
        sun_tzu = result.get('sun_tzu', {})
        pro = sun_tzu.get('pro', 0)
        con = sun_tzu.get('con', 0)
        diff = pro - con
        wyckoff = result.get('wyckoff', {}).get('phase', 'UNKNOWN')
        
        # UNLOCKED STRATEGY: Override Wyckoff when Sun Tzu is strong
        if diff >= 50:
            return {
                "action": "BUY",
                "confidence": "HIGH",
                "reason": f"Sun Tzu strong ({pro} PRO vs {con} CON, diff={diff})",
                "sun_tzu": {"pro": pro, "con": con, "diff": diff},
                "wyckoff": wyckoff
            }
        elif diff <= -50:
            return {
                "action": "SELL",
                "confidence": "HIGH",
                "reason": f"Sun Tzu strong bearish ({pro} PRO vs {con} CON, diff={diff})",
                "sun_tzu": {"pro": pro, "con": con, "diff": diff},
                "wyckoff": wyckoff
            }
        elif result.get('action') != "WAIT":
            return {
                "action": result.get('action'),
                "confidence": result.get('confidence', 'MEDIUM'),
                "reason": f"Combined signal: {result.get('action')}",
                "sun_tzu": {"pro": pro, "con": con, "diff": diff},
                "wyckoff": wyckoff
            }
        else:
            return {
                "action": "WAIT",
                "confidence": "LOW",
                "reason": f"Mixed signals. Sun Tzu diff={diff}, Wyckoff={wyckoff}",
                "sun_tzu": {"pro": pro, "con": con, "diff": diff},
                "wyckoff": wyckoff
            }
    
    def backtest_symbol(self, symbol, period="6mo"):
        print(f"\n📊 Testing {symbol}")
        print("-" * 40)
        
        df = self.fetch_data(symbol, period)
        if df is None or len(df) < 30:
            print(f"  No data available")
            return None
        
        print(f"  Period: {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}")
        print(f"  {len(df)} data points")
        
        trades = []
        forward_days = 3
        step = 2
        
        for i in range(step, len(df) - forward_days, step):
            idx = df.index[i]
            
            # Get signal
            signal = self.get_signal(symbol, df, i)
            
            if signal['action'] == "WAIT":
                continue
            
            # Get future price
            future_idx = min(i + forward_days, len(df) - 1)
            future_price = df['Close'].iloc[future_idx]
            current_price = df['Close'].iloc[i]
            price_change = (future_price - current_price) / current_price * 100
            
            if signal['action'] == "BUY":
                correct = price_change > 0
                profit = price_change
            elif signal['action'] == "SELL":
                correct = price_change < 0
                profit = -price_change
            else:
                continue
            
            trades.append({
                "symbol": symbol,
                "date": idx.strftime("%Y-%m-%d"),
                "action": signal['action'],
                "confidence": signal['confidence'],
                "entry": round(current_price, 2),
                "exit": round(future_price, 2),
                "change_pct": round(price_change, 2),
                "profit_pct": round(profit, 2),
                "correct": correct,
                "reason": signal['reason'],
                "sun_tzu_diff": signal.get('sun_tzu', {}).get('diff', 0),
                "wyckoff": signal.get('wyckoff', 'UNKNOWN')
            })
            
            # Learn from outcome
            if correct:
                self.total_correct += 1
            self.total_trades += 1
            self.total_profit += profit
        
        if not trades:
            print(f"  No trades generated")
            return None
        
        correct = sum(1 for t in trades if t["correct"])
        total = len(trades)
        profit = sum(t["profit_pct"] for t in trades)
        acc = (correct / total * 100) if total > 0 else 0
        
        print(f"  Trades: {total}")
        print(f"  Correct: {correct}")
        print(f"  Accuracy: {acc:.1f}%")
        print(f"  Total Profit: {profit:.1f}%")
        print(f"  Avg Profit: {profit/total:.1f}%")
        print(f"  Avg Sun Tzu Diff: {sum(t['sun_tzu_diff'] for t in trades)/total:.0f}")
        
        return {
            "symbol": symbol,
            "total": total,
            "correct": correct,
            "accuracy": acc,
            "profit": profit,
            "avg_profit": profit/total if total > 0 else 0,
            "avg_sun_tzu_diff": sum(t['sun_tzu_diff'] for t in trades)/total if total > 0 else 0,
            "trades": trades
        }
    
    def run_all(self):
        symbols = ["BTC-USD", "ETH-USD", "SOL-USD", "AAPL", "TSLA", "NVDA", "MSFT", "GC=F", "EURUSD=X"]
        
        print("=" * 60)
        print("🔶 BACKTEST - UNLOCKED STRATEGY")
        print("   Sun Tzu overrides Wyckoff when diff >= 50")
        print("=" * 60)
        
        for symbol in symbols:
            result = self.backtest_symbol(symbol, period="6mo")
            if result:
                self.results.append(result)
                self.print_summary()
            time.sleep(1)
        
        return self.results
    
    def print_summary(self):
        print("\n" + "=" * 60)
        print("📊 UNLOCKED STRATEGY - SUMMARY")
        print("=" * 60)
        
        for r in self.results:
            symbol = r["symbol"]
            total = r["total"]
            correct = r["correct"]
            acc = r["accuracy"]
            profit = r["profit"]
            avg_diff = r.get("avg_sun_tzu_diff", 0)
            print(f"  {symbol}: {correct}/{total} = {acc:.1f}%  |  Profit: {profit:.1f}%  |  Avg Diff: {avg_diff:.0f}")
        
        overall_acc = (self.total_correct / self.total_trades * 100) if self.total_trades > 0 else 0
        print("=" * 60)
        print(f"🏆 OVERALL: {self.total_correct}/{self.total_trades} = {overall_acc:.1f}%")
        print(f"💰 Total Profit: {self.total_profit:.1f}%")
        print(f"📊 Avg Profit per Trade: {self.total_profit/self.total_trades:.1f}%" if self.total_trades > 0 else "")
        print("=" * 60)

def main():
    tester = BacktestUnlocked()
    tester.run_all()
    tester.print_summary()
    print("\n✅ Backtest complete!")

if __name__ == "__main__":
    main()
