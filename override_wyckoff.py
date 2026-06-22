import yfinance as yf
from engine.combined_trading import CombinedTrading
from engine.sun_tzu_engine import SunTzuEngine

symbol = "BTC-USD"

# Get real data
ticker = yf.Ticker(symbol)
data = ticker.history(period="7d")
latest = data.iloc[-1]

# Run Combined Trading
engine = CombinedTrading(symbol)
ticker = yf.Ticker(symbol)
engine.data = {
    "D": ticker.history(period="30d", interval="1d"),
    "4H": ticker.history(period="30d", interval="4h"),
    "1H": ticker.history(period="14d", interval="1h"),
    "15M": ticker.history(period="7d", interval="15m")
}
combined = engine.analyze()

# Run Sun Tzu ONLY
sun_tzu = SunTzuEngine()
market_data = {
    "name": symbol,
    "price": latest['Close'],
    "high_30d": data['High'].iloc[-30:].max(),
    "low_30d": data['Low'].iloc[-30:].min(),
    "volume_avg": data['Volume'].iloc[-20:].mean(),
    "trend": "bullish" if latest['Close'] > data['Close'].iloc[-5] else "bearish",
    "change_pct": ((latest['Close'] - data['Close'].iloc[-5]) / data['Close'].iloc[-5] * 100),
    "source": "YAHOO_FINANCE"
}
st_result = sun_tzu.analyze(market_data, None)

pro = st_result.get('pro_count', 0)
con = st_result.get('con_count', 0)
diff = pro - con

print("=" * 60)
print(f"🔶 BTC-USD SIGNAL ANALYSIS")
print("=" * 60)
print(f"\n📊 SUN TZU: PRO={pro} CON={con} DIFF={diff}")
print(f"📊 WYCKOFF: {combined.get('wyckoff', {}).get('phase', 'N/A')}")
print(f"📊 COMBINED: {combined.get('action', 'N/A')}")

# DECISION RULES
if diff >= 50:
    print(f"\n🚀 SIGNAL: STRONG BUY")
    print(f"   Reason: Sun Tzu strongly bullish (PRO={pro}, CON={con})")
    print(f"   Entry: ${latest['Close']:.2f}")
    print(f"   Stop Loss: ${latest['Close'] * 0.97:.2f} (3% risk)")
    print(f"   Take Profit: ${latest['Close'] * 1.05:.2f} (5% target)")
    print(f"   Risk/Reward: 1.67")
elif diff >= 30:
    print(f"\n📈 SIGNAL: BUY (cautious)")
    print(f"   Reason: Sun Tzu bullish (PRO={pro}, CON={con})")
elif diff <= -50:
    print(f"\n🔻 SIGNAL: STRONG SELL")
    print(f"   Reason: Sun Tzu strongly bearish")
elif combined.get('action') != "WAIT":
    print(f"\n✅ SIGNAL: {combined.get('action')}")
    print(f"   Confidence: {combined.get('confidence')}")
else:
    print(f"\n⏳ SIGNAL: WAIT")
    print(f"   Reason: Signals mixed. Wyckoff unclear, waiting for confirmation.")
