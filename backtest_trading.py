"""
Shadow Trading Backtest - Combined Engine with Learning
Trains on 2023/24, Tests on 2025/26.
61 assets. Crypto, Forex, Indices, Commodities, Stocks.
"""

import requests, time, yfinance as yf

API = "http://127.0.0.1:8000"

ASSETS = {
    "BTC-USD":"Bitcoin","ETH-USD":"Ethereum","SOL-USD":"Solana","DOGE-USD":"Dogecoin",
    "XRP-USD":"Ripple","ADA-USD":"Cardano","BNB-USD":"Binance Coin","AVAX-USD":"Avalanche",
    "DOT-USD":"Polkadot","LINK-USD":"Chainlink","LTC-USD":"Litecoin","MATIC-USD":"Polygon",
    "EURUSD=X":"EUR/USD","GBPUSD=X":"GBP/USD","USDJPY=X":"USD/JPY","AUDUSD=X":"AUD/USD",
    "USDCAD=X":"USD/CAD","NZDUSD=X":"NZD/USD","USDCHF=X":"USD/CHF",
    "EURJPY=X":"EUR/JPY","GBPJPY=X":"GBP/JPY","EURGBP=X":"EUR/GBP",
    "^GSPC":"S&P 500","^IXIC":"NASDAQ","^DJI":"Dow Jones","^FTSE":"FTSE 100",
    "^GDAXI":"DAX","^N225":"Nikkei 225","^VIX":"VIX",
    "GC=F":"Gold","SI=F":"Silver","CL=F":"Crude Oil","BZ=F":"Brent Oil",
    "HG=F":"Copper","NG=F":"Natural Gas","PL=F":"Platinum","PA=F":"Palladium",
    "AAPL":"Apple","MSFT":"Microsoft","GOOGL":"Google","AMZN":"Amazon",
    "TSLA":"Tesla","NVDA":"NVIDIA","META":"Meta","NFLX":"Netflix",
    "JPM":"JPMorgan","BAC":"Bank of America","WMT":"Walmart","XOM":"Exxon",
    "CVX":"Chevron","JNJ":"Johnson","V":"Visa","MA":"Mastercard",
    "PYPL":"PayPal","UBER":"Uber","AMD":"AMD","INTC":"Intel",
    "PLTR":"Palantir","COIN":"Coinbase","SHOP":"Shopify","SNAP":"Snapchat",
    "RBLX":"Roblox","DIS":"Disney","CRM":"Salesforce",
}

def backtest_asset(symbol, name, train_period="2023-01-01", test_period="2025-01-01"):
    """Walk-forward backtest on one asset."""
    print(f"\n{'='*60}")
    print(f"{name} ({symbol})")
    print(f"{'='*60}")
    
    try:
        train_df = yf.Ticker(symbol).history(start=train_period, end="2024-12-31")
        test_df = yf.Ticker(symbol).history(start=test_period, end="2026-06-22")
    except:
        print("  Failed to fetch data")
        return {"train":{"total":0,"correct":0},"test":{"total":0,"correct":0}}
    
    results = {"train":{"total":0,"correct":0,"wrong":0},"test":{"total":0,"correct":0,"wrong":0}}
    
    for phase, df in [("train", train_df), ("test", test_df)]:
        if len(df) < 30:
            print(f"  {phase}: Not enough data")
            continue
        
        for i in range(30, len(df)-1):
            past = df.iloc[:i]
            cur = float(past['Close'].iloc[-1])
            fut = float(df['Close'].iloc[i+1])
            actual = "up" if fut > cur else "down"
            
            try:
                hi = float(past['High'].max()); lo = float(past['Low'].min())
                atr = float((past['High']-past['Low']).mean())
                chg = ((cur-float(past['Close'].iloc[-2]))/float(past['Close'].iloc[-2]))*100 if i>=2 else 0
                
                delta = past['Close'].diff()
                gain = delta.where(delta>0,0.0).rolling(14).mean()
                loss = (-delta.where(delta<0,0.0)).rolling(14).mean()
                rs = gain/loss
                rsi = float(100-(100/(1+rs.iloc[-1]))) if loss.iloc[-1]!=0 else 50
                ma20 = float(past['Close'].rolling(20).mean().iloc[-1])
                vol = int(past['Volume'].mean()) if 'Volume' in past.columns else 0
                trend = "bullish" if cur > ma20 else "bearish"
                
                home = {"name":symbol,"price":round(cur,4),"change_pct":round(chg,2),
                        "rsi":round(rsi,1),"atr":round(atr,4),"high_30d":round(hi,4),
                        "low_30d":round(lo,4),"trend":trend,"volume_avg":vol}
                away = {"name":"USD","wins":0,"goals_for":0}
                
                resp = requests.post(f"{API}/analyze", json={
                    "entity_1":symbol,"entity_2":"USD","domain":"trading",
                    "home_stats":home,"away_stats":away
                }, timeout=30)
                
                if resp.status_code != 200: continue
                r = resp.json()
                
                pick = r.get("pick","")
                q = r.get("quant",{}).get("e1",{})
                score = q.get("strength",5)
                predicted = "up" if pick == symbol else "down"
                correct = (predicted == actual)
                
                # Learn from outcome
                pid = r.get("pred_id","")
                winner = symbol if actual == "up" else "USD"
                if pid:
                    try:
                        requests.post(f"{API}/learn", params={"pred_id":pid,"winner":winner}, timeout=5)
                    except: pass
                
                results[phase]["total"] += 1
                if correct: results[phase]["correct"] += 1
                else: results[phase]["wrong"] += 1
                
            except: pass
        
        if results[phase]["total"] > 0:
            wr = results[phase]["correct"]/results[phase]["total"]*100
            print(f"  {phase.upper()}: {results[phase]['correct']}/{results[phase]['total']} ({wr:.1f}%)")
    
    return results


if __name__ == "__main__":
    import sys
    
    try:
        r = requests.get(f"{API}/", timeout=3)
        if r.status_code != 200:
            print("API not running: python api/server.py")
            sys.exit(1)
    except:
        print("API not running: python api/server.py")
        sys.exit(1)
    
    symbol = sys.argv[1] if len(sys.argv) > 1 else None
    
    if symbol:
        if symbol not in ASSETS:
            print(f"Unknown: {symbol}. Options: {list(ASSETS.keys())}")
            sys.exit(1)
        backtest_asset(symbol, ASSETS[symbol])
    else:
        print("\n📡 FULL TRADING BACKTEST - 61 ASSETS\n")
        print("Training on 2023-2024 | Testing on 2025-2026")
        print("="*60)
        
        train_total = {"total":0,"correct":0}
        test_total = {"total":0,"correct":0}
        
        for sym, name in ASSETS.items():
            st = backtest_asset(sym, name)
            train_total["total"] += st["train"]["total"]
            train_total["correct"] += st["train"]["correct"]
            test_total["total"] += st["test"]["total"]
            test_total["correct"] += st["test"]["correct"]
        
        print(f"\n{'='*60}")
        print("FINAL SUMMARY")
        print(f"{'='*60}")
        if train_total["total"] > 0:
            print(f"Training (2023-24): {train_total['correct']}/{train_total['total']} ({train_total['correct']/train_total['total']*100:.1f}%)")
        if test_total["total"] > 0:
            print(f"Testing  (2025-26): {test_total['correct']}/{test_total['total']} ({test_total['correct']/test_total['total']*100:.1f}%)")
        print("\n✅ Done.")