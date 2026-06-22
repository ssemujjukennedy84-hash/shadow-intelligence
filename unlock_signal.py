import yfinance as yf
from engine.combined_trading import CombinedTrading

symbol = "BTC-USD"

# Create engine with real data
engine = CombinedTrading(symbol)
ticker = yf.Ticker(symbol)
engine.data = {
    "D": ticker.history(period="30d", interval="1d"),
    "4H": ticker.history(period="30d", interval="4h"),
    "1H": ticker.history(period="14d", interval="1h"),
    "15M": ticker.history(period="7d", interval="15m")
}

# Run analysis
result = engine.analyze()

# Get Sun Tzu counts from result
sun_tzu = result.get('sun_tzu', {})
pro = sun_tzu.get('pro', 0)
con = sun_tzu.get('con', 0)
diff = pro - con

print("=" * 60)
print(f"🔶 {symbol} - UNLOCKED SIGNAL")
print("=" * 60)
print(f"\n📊 COMBINED ENGINE DATA:")
print(f"  Action (original): {result.get('action', 'N/A')}")
print(f"  Confidence:        {result.get('confidence', 'N/A')}")
print(f"  Wyckoff:           {result.get('wyckoff', {}).get('phase', 'N/A')}")
print(f"  Sun Tzu PRO/CON:   {pro} / {con} (DIFF: {diff})")

# UNLOCK THE SIGNAL
if diff >= 150:
    print(f"\n🔥 UNLOCKED: STRONG BUY (Sun Tzu diff={diff})")
    print(f"   Reason: Sun Tzu overwhelmingly bullish ({pro} PRO vs {con} CON)")
    
    exec_data = result.get('execution', {})
    if exec_data:
        print(f"\n📈 TRADE LEVELS:")
        print(f"   Entry:       ${exec_data.get('entry', 'N/A')}")
        print(f"   Stop Loss:   ${exec_data.get('stop_loss', 'N/A')}")
        print(f"   Take Profit: ${exec_data.get('take_profit', 'N/A')}")
        print(f"   Risk/Reward: {exec_data.get('risk_reward', 'N/A')}")
    
    tf = result.get('timeframes', {})
    if tf:
        print(f"\n⏰ TIMEFRAMES:")
        print(f"   Daily:  {tf.get('daily', 'N/A')}")
        print(f"   4H:     {tf.get('4h', 'N/A')}")
        print(f"   1H:     {tf.get('1h', 'N/A')}")
        print(f"   15M:    {tf.get('15m', 'N/A')}")
    
    print(f"\n📌 Decision: BUY with 5% target, 3% stop loss")
    print(f"   Current Price: ${exec_data.get('entry', 'N/A')}")
    print(f"   Target: ${exec_data.get('entry', 0) * 1.05:.2f}")
    print(f"   Stop: ${exec_data.get('entry', 0) * 0.97:.2f}")

elif diff <= -150:
    print(f"\n🔻 UNLOCKED: STRONG SELL (Sun Tzu diff={diff})")
else:
    print(f"\n⏳ Waiting: Sun Tzu diff={diff} (need >150 for override)")
    print(f"   Current combined action: {result.get('action', 'N/A')}")
