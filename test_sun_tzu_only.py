from engine.sun_tzu_engine import SunTzuEngine
import yfinance as yf
import json

# Get BTC data
btc = yf.Ticker("BTC-USD")
data = btc.history(period="7d")
latest = data.iloc[-1]

# Build market data
market_data = {
    "name": "BTC-USD",
    "price": latest['Close'],
    "high_30d": data['High'].iloc[-30:].max(),
    "low_30d": data['Low'].iloc[-30:].min(),
    "volume_avg": data['Volume'].iloc[-20:].mean(),
    "trend": "bullish" if latest['Close'] > data['Close'].iloc[-5] else "bearish",
    "change_pct": ((latest['Close'] - data['Close'].iloc[-5]) / data['Close'].iloc[-5] * 100),
    "source": "YAHOO_FINANCE"
}

# Run Sun Tzu ONLY (no Wyckoff)
engine = SunTzuEngine()
# Convert to sports/trading format
result = engine.analyze(market_data, None)

print("=" * 50)
print("🔶 SUN TZU ONLY ANALYSIS")
print("=" * 50)
print(f"  Action: {result.get('action', 'N/A')}")
print(f"  Confidence: {result.get('confidence', 'N/A')}")
print(f"  PRO: {result.get('pro_count', 0)}")
print(f"  CON: {result.get('con_count', 0)}")
print(f"  Chapter Breakdown:")
for ch in result.get('chapter_breakdown', [])[:5]:
    print(f"    Ch.{ch.get('chapter', '')}: {ch.get('verdict', 'N/A')}")
