"""
Shadow Trading Backtest - Full Sun Tzu Mind
61 assets. Crypto, Forex, Indices, Commodities, Stocks.
Walks forward. No data leakage. All 13 chapters.
"""

import requests, time, yfinance as yf
from datetime import datetime

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

def backtest(symbol, name, days=90):
    print(f"\n{'='*60}")
    print(f"{name} ({symbol})")
    print(f"{'='*60}")
    
    try:
        df = yf.Ticker(symbol).history(period=f"{days}d")
    except:
        print("  Failed to fetch")
        return {"total":0,"correct":0}
    
    if len(df) < 30:
        print("  Not enough data")
        return {"total":0,"correct":0}
    
    st = {"total":0,"correct":0,"wrong":0,"no_signal":0}
    
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
            ma50 = float(past['Close'].rolling(50).mean().iloc[-1]) if len(past)>=50 else ma20
            trend = "bullish" if cur>ma20>ma50 else "bearish" if cur<ma20<ma50 else "neutral"
            vol = int(past['Volume'].mean()) if 'Volume' in past.columns else 0
            
            home = {"name":symbol,"price":round(cur,4),"change_pct":round(chg,2),
                    "rsi_14":round(rsi,1),"atr":round(atr,4),"ma_20":round(ma20,4),
                    "ma_50":round(ma50,4),"trend":trend,"high_30d":round(hi,4),
                    "low_30d":round(lo,4),"volume_avg":vol}
            away = {"name":"USD","strength":5,"energy":50,"morale":5}
            
            resp = requests.post(f"{API}/analyze",json={
                "entity_1":symbol,"entity_2":"USD","domain":"trading",
                "home_stats":home,"away_stats":away},timeout=60)
            
            if resp.status_code!=200: continue
            r = resp.json()
            if r.get("no_signal"): st["no_signal"]+=1; continue
            
            score = r.get("quant",{}).get("e1",{}).get("strength",5)
            predicted = "up" if score > 5 else "down"
            correct = (predicted==actual)
            
            st["total"]+=1
            if correct: st["correct"]+=1
            else: st["wrong"]+=1
            
        except: pass
        time.sleep(0.2)
    
    if st["total"]>0:
        wr = st["correct"]/st["total"]*100
        print(f"  {st['correct']}/{st['total']} ({wr:.1f}%)")
    return st


if __name__=="__main__":
    import sys
    try:
        r=requests.get(f"{API}/",timeout=3)
        if r.status_code!=200: print("API not running"); sys.exit(1)
    except: print("API not running"); sys.exit(1)
    
    sym = sys.argv[1] if len(sys.argv)>1 else None
    
    if sym:
        if sym not in ASSETS: print(f"Options: {list(ASSETS.keys())}"); sys.exit(1)
        backtest(sym, ASSETS[sym])
    else:
        print("\n📡 61 ASSETS TRADING BACKTEST\n")
        tc=tp=0
        for sym,name in ASSETS.items():
            st=backtest(sym,name)
            tc+=st["correct"]; tp+=st["total"]
        if tp>0: print(f"\n{'='*60}\nOVERALL: {tc}/{tp} ({tc/tp*100:.1f}%)\n{'='*60}")
    print("\nDone.")