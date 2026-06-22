import yfinance as yf
from engine.combined_trading import CombinedTrading
import json

# Get real BTC data
btc = yf.Ticker("BTC-USD")
data = btc.history(period="7d")

if len(data) > 0:
    latest = data.iloc[-1]
    
    print("=" * 50)
    print("📊 REAL BTC DATA")
    print("=" * 50)
    print(f"  Price:  ${latest['Close']:.2f}")
    print(f"  High:   ${latest['High']:.2f}")
    print(f"  Low:    ${latest['Low']:.2f}")
    print(f"  Volume: {latest['Volume']:,.0f}")
    
    print("\n" + "=" * 50)
    print("🔶 SHADOW ANALYSIS")
    print("=" * 50)
    
    # Run CombinedTrading
    engine = CombinedTrading("BTC-USD")
    result = engine.analyze()
    
    print(f"\n  Action:      {result.get('action', 'N/A')}")
    print(f"  Confidence:  {result.get('confidence', 'N/A')}")
    print(f"  Wyckoff:     {result.get('wyckoff', {}).get('phase', 'N/A')}")
    print(f"  Sun Tzu:     PRO: {result.get('sun_tzu', {}).get('pro', 0)} / CON: {result.get('sun_tzu', {}).get('con', 0)}")
    
    exec_data = result.get('execution', {})
    if exec_data:
        print(f"\n  📈 EXECUTION LEVELS:")
        print(f"    Entry:       ${exec_data.get('entry', 'N/A')}")
        print(f"    Stop Loss:   ${exec_data.get('stop_loss', 'N/A')}")
        print(f"    Take Profit: ${exec_data.get('take_profit', 'N/A')}")
        print(f"    Risk/Reward: {exec_data.get('risk_reward', 'N/A')}")
    
    tf = result.get('timeframes', {})
    if tf:
        print(f"\n  ⏰ TIMEFRAME SIGNALS:")
        print(f"    Daily:  {tf.get('daily', 'N/A')}")
        print(f"    4H:     {tf.get('4h', 'N/A')}")
        print(f"    1H:     {tf.get('1h', 'N/A')}")
        print(f"    15M:    {tf.get('15m', 'N/A')}")
    
    chapters = result.get('chapter_breakdown', [])
    if chapters:
        print(f"\n  📖 CHAPTER BREAKDOWN (First 5):")
        for ch in chapters[:5]:
            print(f"    Ch.{ch.get('chapter', '')}: {ch.get('verdict', 'N/A')} (weight: {ch.get('weight', 1.0):.2f})")
    
    print("\n" + "=" * 50)
    print(f"📌 Prediction ID: {result.get('prediction_id', 'N/A')}")
    
else:
    print("No data available")
