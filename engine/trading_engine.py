"""
Shadow Trading Engine - Binance Testnet
Sun Tzu executes trades. Pure strategy.
"""

import os, hashlib, hmac, time, requests, json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

API_KEY = os.getenv("BINANCE_API_KEY")
SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
BASE_URL = "https://testnet.binance.vision"

class TradingEngine:
    def __init__(self):
        self.connected = self._check()
        if self.connected:
            print(f"✅ Binance Testnet Connected")
            print(f"   Balance: {self.balance('USDT'):.2f} USDT")
        else:
            print("❌ Connection failed. Check keys.")
    
    def _sign(self, params):
        query = '&'.join([f"{k}={v}" for k,v in params.items()])
        return hmac.new(SECRET_KEY.encode(), query.encode(), hashlib.sha256).hexdigest()
    
    def _request(self, method, endpoint, params=None, signed=False):
        url = f"{BASE_URL}{endpoint}"
        headers = {"X-MBX-APIKEY": API_KEY}
        if signed and params:
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self._sign(params)
        try:
            r = requests.request(method, url, headers=headers, params=params, timeout=10)
            return r.json() if r.status_code == 200 else {"error": r.status_code}
        except: return {"error": "connection"}
    
    def _check(self):
        r = self._request("GET", "/api/v3/ping")
        return r == {}
    
    def balance(self, asset="USDT"):
        r = self._request("GET", "/api/v3/account", signed=True)
        if "error" in r: return 0
        for b in r.get("balances", []):
            if b["asset"] == asset: return float(b["free"])
        return 0
    
    def price(self, symbol="BTCUSDT"):
        r = self._request("GET", "/api/v3/ticker/price", params={"symbol": symbol})
        return float(r.get("price", 0)) if "error" not in r else 0
    
    def stats(self, symbol="BTCUSDT"):
        r = self._request("GET", "/api/v3/ticker/24hr", params={"symbol": symbol})
        if "error" in r: return {}
        return {
            "price": float(r.get("lastPrice", 0)),
            "change": float(r.get("priceChangePercent", 0)),
            "high": float(r.get("highPrice", 0)),
            "low": float(r.get("lowPrice", 0)),
            "volume": float(r.get("volume", 0))
        }
    
    def buy(self, symbol, amount_usdt):
        """Market buy with USDT amount."""
        return self._request("POST", "/api/v3/order", params={
            "symbol": symbol, "side": "BUY", "type": "MARKET",
            "quoteOrderQty": round(amount_usdt, 2)
        }, signed=True)
    
    def sell(self, symbol, quantity):
        """Market sell asset quantity."""
        return self._request("POST", "/api/v3/order", params={
            "symbol": symbol, "side": "SELL", "type": "MARKET",
            "quantity": quantity
        }, signed=True)
    
    def execute_shadow_signal(self, asset, action, confidence, margin):
        """
        Execute a trade based on Shadow's analysis.
        asset: "BTC", "ETH", etc.
        action: "BUY" or "SELL"
        confidence: 0-1 from chapter convergence
        margin: strength difference
        """
        symbol = f"{asset}USDT"
        price = self.price(symbol)
        balance = self.balance("USDT")
        
        if balance < 15:
            return {"error": f"Low balance: {balance:.2f} USDT"}
        
        # Position size: Kelly-inspired based on edge
        edge = confidence - 0.5  # How much above 50%
        base = balance * 0.10  # 10% of capital
        size = base * (1 + edge * 2)  # More edge = bigger bet
        size = max(10, min(size, balance * 0.20))  # $10 min, 20% max
        
        print(f"\n⚔️ SHADOW EXECUTION")
        print(f"   {action} {symbol} @ ${price:,.2f}")
        print(f"   Size: ${size:.2f} | Edge: {edge:.0%} | Margin: {margin}")
        
        if action == "BUY":
            result = self.buy(symbol, size)
        else:
            asset_bal = self.balance(asset)
            result = self.sell(symbol, asset_bal) if asset_bal > 0 else {"error": "No balance"}
        
        if "error" not in result:
            print(f"   ✅ Executed: {result.get('executedQty', '?')} {asset}")
        else:
            print(f"   ❌ Failed: {result.get('error', 'unknown')}")
        
        return result
    
    def get_portfolio(self):
        """Get current holdings."""
        r = self._request("GET", "/api/v3/account", signed=True)
        if "error" in r: return []
        return [{"asset": b["asset"], "free": float(b["free"]), "locked": float(b["locked"])} 
                for b in r.get("balances", []) if float(b["free"]) > 0 or float(b["locked"]) > 0]


if __name__ == "__main__":
    engine = TradingEngine()
    if engine.connected:
        print("\n📊 Market Snapshot:")
        for sym in ["BTCUSDT", "ETHUSDT", "SOLUSDT"]:
            s = engine.stats(sym)
            if s:
                print(f"   {sym}: ${s['price']:,.2f} ({s['change']:+.2f}%)")
        
        print(f"\n📂 Portfolio:")
        for p in engine.get_portfolio():
            print(f"   {p['asset']}: {p['free']:.4f}")