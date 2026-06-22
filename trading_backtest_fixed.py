"""
TRADING BACKTEST - FIXED
- Only HIGH CONFIDENCE trades (>60%)
- 3-day forward testing
- News sentiment from price action
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

class TradingBacktester:
    def __init__(self):
        self.sun_tzu = SunTzuEngine()
        self.quant = QuantEngine()
        self.learner = SelfLearner()
        self.results = []
        self.total_trades = 0
        self.total_correct = 0
        self.total_profit = 0
        self.min_confidence = 60  # Only trade with 60%+ confidence
        self.forward_days = 3     # 3-day prediction horizon
        
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
    
    def get_news_sentiment(self, symbol, df, idx):
        """Derive sentiment from price action"""
        if idx < 5:
            return 0
        recent_change = (df['Close'].iloc[idx] - df['Close'].iloc[idx-5]) / df['Close'].iloc[idx-5]
        sentiment = np.clip(recent_change * 5, -1, 1)
        confidence = min(1.0, abs(recent_change) * 10)
        return {"sentiment": sentiment, "confidence": confidence}
    
    def calculate_rsi(self, prices, period=14):
        if len(prices) < period:
            return 50
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1] if len(rsi) > 0 else 50
    
    def calculate_atr(self, df, period=14):
        high = df['High']
        low = df['Low']
        close = df['Close']
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(window=period).mean().iloc[-1] if len(tr) > period else 0
    
    def backtest_symbol(self, symbol, period="6mo"):
        print(f"\n📊 Testing {symbol}")
        print("-" * 40)
        
        df = self.fetch_data(symbol, period)
        if df is None or len(df) < 30:
            print(f"  No data available")
            return None
        
        print(f"  Period: {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}")
        print(f"  {len(df)} data points")
        print(f"  Min Confidence: {self.min_confidence}%")
        print(f"  Forward Days: {self.forward_days}")
        
        trades = []
        step = 2  # Trade every 2 days
        
        for i in range(step, len(df) - self.forward_days, step):
            idx = df.index[i]
            lookback = df.iloc[:i+1]
            
            if len(lookback) < 20:
                continue
            
            current_price = lookback['Close'].iloc[-1]
            high_30d = lookback['High'].iloc[-30:].max()
            low_30d = lookback['Low'].iloc[-30:].min()
            rsi = self.calculate_rsi(lookback['Close'])
            volume_avg = lookback['Volume'].iloc[-20:].mean()
            change_pct = (lookback['Close'].iloc[-1] - lookback['Close'].iloc[-5]) / lookback['Close'].iloc[-5] * 100
            atr = self.calculate_atr(lookback)
            
            trend = "bullish" if lookback['Close'].iloc[-1] > lookback['Close'].iloc[-5] else "bearish"
            
            # Get news sentiment
            news = self.get_news_sentiment(symbol, df, i)
            
            market_data = {
                "name": symbol,
                "price": current_price,
                "high_30d": high_30d,
                "low_30d": low_30d,
                "rsi_14": rsi,
                "volume_avg": volume_avg,
                "trend": trend,
                "change_pct": change_pct,
                "atr": atr,
                "source": "YAHOO_FINANCE",
                "news_sentiment": news["sentiment"],
                "news_confidence": news["confidence"]
            }
            
            try:
                engine = CombinedTrading(symbol)
                result = engine.analyze()
            except Exception as e:
                continue
            
            # SKIP LOW CONFIDENCE TRADES
            confidence = result.get("confidence", 0)
            if confidence < self.min_confidence:
                continue
            
            action = result.get("action", "WAIT")
            if action == "WAIT":
                continue
            
            # Get future price (3 days later)
            future_idx = min(i + self.forward_days, len(df) - 1)
            future_price = df['Close'].iloc[future_idx]
            price_change = (future_price - current_price) / current_price * 100
            
            if action == "BUY":
                correct = price_change > 0
                profit = price_change
            elif action == "SELL":
                correct = price_change < 0
                profit = -price_change
            else:
                continue
            
            trades.append({
                "symbol": symbol,
                "date": idx.strftime("%Y-%m-%d"),
                "action": action,
                "confidence": confidence,
                "entry": round(current_price, 2),
                "exit": round(future_price, 2),
                "change_pct": round(price_change, 2),
                "profit_pct": round(profit, 2),
                "correct": correct,
                "wyckoff_phase": result.get("wyckoff", {}).get("phase", ""),
                "prediction_id": result.get("prediction_id", "")
            })
            
            if result.get("prediction_id"):
                self.learner.learn_from_outcome(result["prediction_id"], price_change)
        
        if not trades:
            print(f"  No high-confidence trades generated")
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
        print(f"  Avg Confidence: {sum(t['confidence'] for t in trades)/total:.1f}%")
        
        self.total_correct += correct
        self.total_trades += total
        self.total_profit += profit
        
        return {
            "symbol": symbol,
            "total": total,
            "correct": correct,
            "accuracy": acc,
            "profit": profit,
            "avg_profit": profit/total if total > 0 else 0,
            "avg_confidence": sum(t['confidence'] for t in trades)/total if total > 0 else 0,
            "trades": trades
        }
    
    def run_all(self):
        symbols = [
            "BTC-USD", "ETH-USD", "SOL-USD",
            "AAPL", "TSLA", "NVDA", "MSFT",
            "GC=F", "EURUSD=X"
        ]
        
        print("=" * 60)
        print("🔶 TRADING BACKTEST - FIXED")
        print(f"   Min Confidence: {self.min_confidence}%")
        print(f"   Forward Days: {self.forward_days}")
        print("   Symbols: Crypto, Stocks, Commodities, Forex")
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
        print("📊 TRADING BACKTEST SUMMARY")
        print("=" * 60)
        
        for r in self.results:
            symbol = r["symbol"]
            total = r["total"]
            correct = r["correct"]
            acc = r["accuracy"]
            profit = r["profit"]
            conf = r.get("avg_confidence", 0)
            print(f"  {symbol}: {correct}/{total} = {acc:.1f}%  |  Profit: {profit:.1f}%  |  Avg Conf: {conf:.0f}%")
        
        overall_acc = (self.total_correct / self.total_trades * 100) if self.total_trades > 0 else 0
        print("=" * 60)
        print(f"🏆 OVERALL: {self.total_correct}/{self.total_trades} = {overall_acc:.1f}%")
        print(f"💰 Total Profit: {self.total_profit:.1f}%")
        print(f"📊 Avg Profit per Trade: {self.total_profit/self.total_trades:.1f}%" if self.total_trades > 0 else "")
        print("=" * 60)

def main():
    tester = TradingBacktester()
    tester.run_all()
    tester.print_summary()
    print("\n✅ Trading backtest complete!")

if __name__ == "__main__":
    main()
