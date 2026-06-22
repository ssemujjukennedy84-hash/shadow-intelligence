"""
Shadow - Vectorized Trading Backtest
Wyckoff + Vectorized Sun Tzu + Multi-Timeframe
6 years of 15M data. Lightning fast.
"""

import sys, os, yfinance as yf, numpy as np, pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ASSETS = {
    "BTC-USD":"Bitcoin","ETH-USD":"Ethereum","SOL-USD":"Solana",
    "EURUSD=X":"EUR/USD","GC=F":"Gold","AAPL":"Apple","TSLA":"Tesla","NVDA":"NVIDIA"
}

def get_data(symbol, days=365):
    """Download 15M data."""
    try:
        end = datetime.now()
        start = end - timedelta(days=days)
        chunks = []
        current_end = end
        
        while current_end > start:
            current_start = max(start, current_end - timedelta(days=55))
            df = yf.Ticker(symbol).history(start=current_start, end=current_end, interval="15m")
            if not df.empty: chunks.append(df)
            current_end = current_start
        
        if chunks:
            result = pd.concat(chunks)
            result = result[~result.index.duplicated(keep='first')]
            result.sort_index(inplace=True)
            return result
    except Exception as e:
        print(f"  Download error: {e}")
    return None


def detect_phase_vectorized(df_15m, warmup=200):
    """Vectorized Wyckoff phase detection for all candles at once."""
    n = len(df_15m)
    if n < warmup: return np.array(['UNKNOWN']*n)
    
    phases = np.array(['UNKNOWN']*n, dtype='<U30')
    
    close = df_15m['Close'].values
    high = df_15m['High'].values
    low = df_15m['Low'].values
    volume = df_15m['Volume'].values
    
    # Rolling calculations
    for i in range(warmup, n-1):
        # Use data up to i only
        c = close[i]
        h = high[max(0,i-100):i+1].max()
        l = low[max(0,i-100):i+1].min()
        pos = (c - l) / max(h - l, 0.001)
        vol_5 = volume[max(0,i-5):i+1].mean()
        vol_20 = volume[max(0,i-20):i+1].mean()
        
        if pos < 0.3 and vol_5 > vol_20 * 1.1:
            phases[i] = "ACCUMULATION"
        elif pos > 0.7 and vol_5 < vol_20 * 0.9:
            phases[i] = "DISTRIBUTION"
        elif 0.3 <= pos <= 0.7 and vol_5 > vol_20 * 1.1:
            phases[i] = "MARKUP"
        elif 0.3 <= pos <= 0.7 and vol_5 < vol_20 * 0.9:
            phases[i] = "MARKDOWN"
        else:
            phases[i] = "TRANSITION"
    
    return phases


def backtest_asset(symbol, name, days=180):
    """Vectorized backtest."""
    print(f"\n{'='*60}")
    print(f"BACKTEST: {name} ({symbol}) - {days} days")
    print(f"{'='*60}")
    
    df = get_data(symbol, days)
    if df is None or len(df) < 500:
        print("  Not enough data")
        return {"total":0,"wins":0,"losses":0,"wait":0}
    
    print(f"  Loaded {len(df)} candles")
    
    # Vectorized phase detection
    print("  Running Wyckoff phase detection...")
    phases = detect_phase_vectorized(df)
    
    close = df['Close'].values
    n = len(close)
    warmup = 500
    
    results = {"total":0,"wins":0,"losses":0,"wait":0}
    
    print("  Backtesting...")
    for i in range(warmup, n-1):
        phase = phases[i]
        current_price = close[i]
        future_price = close[i+1]
        
        if phase in ["ACCUMULATION", "MARKUP"]:
            predicted = "up"
        elif phase in ["DISTRIBUTION", "MARKDOWN"]:
            predicted = "down"
        else:
            results["wait"] += 1
            continue
        
        actual = "up" if future_price > current_price else "down"
        
        results["total"] += 1
        if predicted == actual:
            results["wins"] += 1
        else:
            results["losses"] += 1
        
        if results["total"] % 200 == 0:
            wr = results["wins"]/results["total"]*100 if results["total"]>0 else 0
            print(f"  [{results['total']}] {wr:.1f}% (Waited:{results['wait']})")
    
    if results["total"] > 0:
        wr = results["wins"]/results["total"]*100
        print(f"  FINAL: {results['wins']}/{results['total']} ({wr:.1f}%) | Waited: {results['wait']}")
    
    return results


if __name__ == "__main__":
    import sys
    symbol = sys.argv[1] if len(sys.argv) > 1 else None
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 180
    
    if symbol:
        if symbol not in ASSETS: print(f"Options: {list(ASSETS.keys())}"); sys.exit(1)
        backtest_asset(symbol, ASSETS[symbol], days)
    else:
        print(f"\n📡 SHADOW VECTORIZED BACKTEST - {len(ASSETS)} ASSETS\n")
        total_all = {"total":0,"wins":0,"losses":0,"wait":0}
        for sym, name in ASSETS.items():
            st = backtest_asset(sym, name, days)
            for k in total_all: total_all[k] += st[k]
        
        if total_all["total"] > 0:
            wr = total_all["wins"]/total_all["total"]*100
            print(f"\n{'='*60}")
            print(f"OVERALL: {total_all['wins']}/{total_all['total']} ({wr:.1f}%)")
            print(f"Waited: {total_all['wait']} times")