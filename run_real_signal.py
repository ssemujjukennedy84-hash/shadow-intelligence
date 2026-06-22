import yfinance as yf
from engine.combined_trading import CombinedTrading
import json

# Create engine
engine = CombinedTrading("BTC-USD")

# Load data for different timeframes
ticker = yf.Ticker("BTC-USD")
data = {
    "D": ticker.history(period="30d", interval="1d"),
    "4H": ticker.history(period="30d", interval="4h"),
    "1H": ticker.history(period="14d", interval="1h"),
    "15M": ticker.history(period="7d", interval="15m")
}

# Inject data
engine.data = data

# Analyze with real data
result = engine.analyze()

print("=" * 60)
print("🔶 COMBINED TRADING - REAL DATA SIGNAL")
print("=" * 60)
print(f"\n📊 SIGNAL:")
print(f"  Action:      {result.get('action', 'N/A')}")
print(f"  Confidence:  {result.get('confidence', 'N/A')}")
print(f"  Wyckoff:     {result.get('wyckoff', {}).get('phase', 'N/A')}")
print(f"  Sun Tzu:     PRO: {result.get('sun_tzu', {}).get('pro', 0)} / CON: {result.get('sun_tzu', {}).get('con', 0)}")

exec_data = result.get('execution', {})
if exec_data:
    print(f"\n📈 EXECUTION LEVELS:")
    print(f"    Entry:       ${exec_data.get('entry', 'N/A')}")
    print(f"    Stop Loss:   ${exec_data.get('stop_loss', 'N/A')}")
    print(f"    Take Profit: ${exec_data.get('take_profit', 'N/A')}")
    print(f"    Risk/Reward: {exec_data.get('risk_reward', 'N/A')}")

tf = result.get('timeframes', {})
if tf:
    print(f"\n⏰ TIMEFRAME SIGNALS:")
    print(f"    Daily:  {tf.get('daily', 'N/A')}")
    print(f"    4H:     {tf.get('4h', 'N/A')}")
    print(f"    1H:     {tf.get('1h', 'N/A')}")
    print(f"    15M:    {tf.get('15m', 'N/A')}")

# Show prediction ID
print(f"\n📌 Prediction ID: {result.get('prediction_id', 'N/A')}")
