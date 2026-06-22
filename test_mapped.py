from engine.sun_tzu_engine import SunTzuEngine
from engine.data_mapper import map_trading, map_sports

engine = SunTzuEngine()

# Test trading
btc = map_trading({'name':'BTC-USD','price':64000,'change_pct':2.5,'rsi':62,'trend':'bullish','volume_avg':500000,'atr':1200,'source':'YAHOO'})
usd = map_trading({'name':'USD','price':1,'change_pct':-0.5,'rsi':45,'trend':'bearish','volume_avg':100000,'atr':0.01,'source':'YAHOO'})

r = engine.analyze(btc, usd)
print("TRADING:")
print(f"  Principles: {r['total_principles']}")
print(f"  PRO: {r['pro_count']} | CON: {r['con_count']} | NEU: {r['neutral_count']}")
print(f"  Active (non-NEUTRAL): {r['pro_count'] + r['con_count']} of {r['total_principles']}")
print()

# Test sports
france = map_sports({'name':'France','wins':7,'losses':1,'draws':2,'goals_for':22,'goals_against':5,'clean_sheets':5,'form':'WWDWW','played':10,'capacity':80000,'home_away':'home','manager_quality':8,'team_harmony':8,'discipline':7,'counter_attack':4,'away_wins':4,'squad_depth':25,'squad_value':500,'preparation':8,'intelligence':7,'weather':'Clear','altitude':35,'pitch_condition':'good','rest_days':5,'travel_distance':0,'fixture_congestion':2,'injury_count':1,'comeback_wins':2,'possession':58,'shots_on_target':6,'first_half':12,'second_half':10,'crowd_support':8,'media_pressure':4,'news_count':5,'source':'API_FOOTBALL','h2h_advantage':2,'data_freshness':6,'season_advantage':True,'time_advantage':True,'must_win':False,'lead_lost':1,'set_pieces':3,'formation_changes':3,'suspension':0,'injury_news':['minor knock'],'morale_change':1})

senegal = map_sports({'name':'Senegal','wins':4,'losses':3,'draws':3,'goals_for':12,'goals_against':10,'clean_sheets':2,'form':'WLDLW','played':10,'capacity':50000,'home_away':'away','manager_quality':6,'team_harmony':6,'discipline':5,'counter_attack':2,'away_wins':1,'squad_depth':18,'squad_value':200,'preparation':5,'intelligence':5,'weather':'Cloudy','altitude':20,'pitch_condition':'average','rest_days':3,'travel_distance':4500,'fixture_congestion':4,'injury_count':3,'comeback_wins':1,'possession':42,'shots_on_target':3,'first_half':5,'second_half':7,'crowd_support':4,'media_pressure':3,'news_count':2,'source':'SPORTSDB','h2h_advantage':0,'data_freshness':48,'season_advantage':False,'time_advantage':False,'must_win':False,'lead_lost':3,'set_pieces':1,'formation_changes':1,'suspension':1,'injury_news':[],'morale_change':-1})

r2 = engine.analyze(france, senegal)
print("SPORTS:")
print(f"  Principles: {r2['total_principles']}")
print(f"  PRO: {r2['pro_count']} | CON: {r2['con_count']} | NEU: {r2['neutral_count']}")
print(f"  Active (non-NEUTRAL): {r2['pro_count'] + r2['con_count']} of {r2['total_principles']}")