from engine.trading_engine import TradingEngine

t = TradingEngine()
print('Balances:')
for b in t.get_portfolio():
    asset = b['asset']
    free = b['free']
    print(f'  {asset}: {free}')