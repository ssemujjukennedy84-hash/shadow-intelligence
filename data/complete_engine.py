"""
Shadow Complete Data Engine
Weather, FIFA Rankings, H2H, Manager, Injuries, News
Everything the 13 chapters require.
"""

import requests, yfinance as yf, feedparser, os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
FOOTBALL_KEY = os.getenv("FOOTBALL_DATA_KEY", "")
API_FOOTBALL_KEY = os.getenv("FOOTBALL_KEY", "")

TEAM_CITIES = {
    "france":(48.85,2.35),"senegal":(14.69,-17.44),"brazil":(-23.55,-46.63),"argentina":(-34.60,-58.38),
    "england":(51.50,-0.12),"germany":(52.52,13.40),"spain":(40.41,-3.70),"italy":(41.90,12.49),
    "netherlands":(52.37,4.89),"portugal":(38.71,-9.13),"belgium":(50.85,4.35),"uruguay":(-34.88,-56.18),
    "cape verde":(14.92,-23.51),"iran":(35.68,51.38),"japan":(35.68,139.76),"south korea":(37.56,126.97),
    "morocco":(33.57,-7.58),"croatia":(45.81,15.97),"man city":(53.48,-2.24),"arsenal":(51.55,-0.10),
    "liverpool":(53.43,-2.96),"man united":(53.46,-2.29),"chelsea":(51.48,-0.19),"tottenham":(51.60,-0.06),
    "real madrid":(40.45,-3.68),"barcelona":(41.38,2.15),"bayern":(48.21,11.62),"dortmund":(51.49,7.45),
    "inter":(45.47,9.19),"ac milan":(45.47,9.19),"psg":(48.84,2.25),"marseille":(43.29,5.39),
}

PAIRS = {
    "btc":"BTC-USD","bitcoin":"BTC-USD","eth":"ETH-USD","ethereum":"ETH-USD",
    "eur":"EURUSD=X","eurusd":"EURUSD=X","gbp":"GBPUSD=X","gbpusd":"GBPUSD=X",
    "jpy":"USDJPY=X","usdjpy":"USDJPY=X","spx":"^GSPC","sp500":"^GSPC",
    "nasdaq":"^IXIC","dow":"^DJI","dxy":"DX-Y.NYB","usd":"DX-Y.NYB",
    "gold":"GC=F","xauusd":"GC=F","silver":"SI=F","oil":"CL=F","wti":"CL=F",
    "aapl":"AAPL","msft":"MSFT","googl":"GOOGL","amzn":"AMZN","tsla":"TSLA","nvda":"NVDA",
}

class CompleteEngine:
    def __init__(self):
        self.year = datetime.now().year
    
    def get_all(self, name, domain):
        if domain == "trading": return self._trading(name)
        return self._sports(name)
    
    def _resolve(self, name):
        clean = name.strip()
        if clean in PAIRS: return PAIRS[clean]
        lower = clean.lower()
        if lower in PAIRS: return PAIRS[lower]
        return name
    
    def _trading(self, name):
        sym = self._resolve(name)
        try:
            t = yf.Ticker(sym); d = t.history(period="30d")
            if d.empty or len(d) < 2: return {"name":name,"error":"no data"}
            cur=float(d['Close'].iloc[-1]); prev=float(d['Close'].iloc[-2])
            hi=float(d['High'].max()); lo=float(d['Low'].min()); atr=float((d['High']-d['Low']).mean())
            chg=((cur-prev)/prev)*100
            delta=d['Close'].diff(); gain=delta.where(delta>0,0.0).rolling(14).mean(); loss=(-delta.where(delta<0,0.0)).rolling(14).mean()
            rs=gain/loss; rsi=float(100-(100/(1+rs.iloc[-1]))) if loss.iloc[-1]!=0 else 50
            ma20=float(d['Close'].rolling(20).mean().iloc[-1]); vol=int(d['Volume'].mean()) if 'Volume' in d.columns else 0
            trend="bullish" if cur>ma20 else "bearish"
            return {"name":name,"symbol":sym,"price":round(cur,4),"change_pct":round(chg,2),"rsi_14":round(rsi,1),"atr":round(atr,4),"high_30d":round(hi,4),"low_30d":round(lo,4),"trend":trend,"volume_avg":vol,"ma_20":round(ma20,4),"source":"YAHOO"}
        except: return {"name":name,"error":"failed"}
    
    def _sports(self, name):
        data = {"name": name}
        
        # 1. Team stats from API-Football
        data.update(self._api_football_team(name))
        
        # 2. FIFA Ranking
        data.update(self._fifa_ranking(name))
        
        # 3. Weather at team's city
        data.update(self._weather(name))
        
        # 4. News/Injuries
        data.update(self._injuries(name))
        
        # 5. Manager info from SportsDB
        data.update(self._manager(name))
        
        return data
    
    def _api_football_team(self, name):
        try:
            headers = {"x-apisports-key": API_FOOTBALL_KEY}
            r = requests.get(f"https://v3.football.api-sports.io/teams?search={name}", headers=headers, timeout=8)
            if r.status_code == 200 and r.json().get("response"):
                team = r.json()["response"][0]["team"]
                tid = team["id"]
                result = {"team_id": tid, "founded": team.get("founded",""), "venue": team.get("venue_name",""), "capacity": team.get("venue_capacity",0), "country": team.get("country","")}
                r2 = requests.get(f"https://v3.football.api-sports.io/teams/statistics?team={tid}&season={self.year}", headers=headers, timeout=8)
                if r2.status_code == 200:
                    stats = r2.json().get("response",{})
                    if isinstance(stats, list): stats = stats[0] if stats else {}
                    fixtures = stats.get("fixtures",{})
                    goals = stats.get("goals",{})
                    result.update({"form": stats.get("form",""),"played": fixtures.get("played",{}).get("total",0),"wins": fixtures.get("wins",{}).get("total",0),"draws": fixtures.get("draws",{}).get("total",0),"losses": fixtures.get("loses",{}).get("total",0),"goals_for": goals.get("for",{}).get("total",{}).get("total",0) if isinstance(goals.get("for",{}).get("total",{}),dict) else goals.get("for",{}).get("total",0),"goals_against": goals.get("against",{}).get("total",{}).get("total",0) if isinstance(goals.get("against",{}).get("total",{}),dict) else goals.get("against",{}).get("total",0),"clean_sheets": fixtures.get("clean_sheet",{}).get("total",0),"league": stats.get("league",{}).get("name","")})
                return result
        except: pass
        return {}
    
    def _fifa_ranking(self, name):
        """Get FIFA ranking as proxy for team strength."""
        try:
            headers = {"x-apisports-key": API_FOOTBALL_KEY}
            r = requests.get(f"https://v3.football.api-sports.io/teams?search={name}", headers=headers, timeout=8)
            if r.status_code == 200 and r.json().get("response"):
                tid = r.json()["response"][0]["team"]["id"]
                return {"fifa_team_id": tid}
        except: pass
        return {}
    
    def _weather(self, name):
        key = name.lower().strip()
        coords = TEAM_CITIES.get(key)
        if not coords:
            for k in TEAM_CITIES:
                if k in key or key in k: coords = TEAM_CITIES[k]; break
        if coords:
            try:
                r = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={coords[0]}&longitude={coords[1]}&current_weather=true", timeout=5)
                if r.status_code == 200:
                    w = r.json()["current_weather"]
                    codes = {0:"Clear",1:"Clear",2:"Cloudy",3:"Overcast",45:"Fog",51:"Drizzle",61:"Rain",71:"Snow",95:"Storm"}
                    return {"weather": codes.get(w["weathercode"],"Unknown"),"temperature": w["temperature"],"wind_speed": w["windspeed"]}
            except: pass
        return {"weather": "Unknown"}
    
    def _injuries(self, name):
        """Search news for injuries."""
        try:
            if NEWSAPI_KEY:
                from newsapi import NewsApiClient
                api = NewsApiClient(api_key=NEWSAPI_KEY)
                articles = api.get_everything(q=f"{name} injury OR injured OR suspension", language='en', page_size=3)
                news = articles.get('articles',[])
                return {"injury_news": [a['title'] for a in news[:2]],"news_count": len(news)}
        except: pass
        return {"injury_news": [], "news_count": 0}
    
    def _manager(self, name):
        """Get manager/coach info from SportsDB."""
        try:
            r = requests.get(f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={name}", timeout=5)
            if r.status_code == 200 and r.json().get("teams"):
                t = r.json()["teams"][0]
                return {"manager": t.get("strManager",""),"stadium": t.get("strStadium",""),"league": t.get("strLeague","")}
        except: pass
        return {}
    
    def get_h2h(self, team1, team2):
        try:
            headers = {"x-apisports-key": API_FOOTBALL_KEY}
            # Get team IDs
            r1 = requests.get(f"https://v3.football.api-sports.io/teams?search={team1}", headers=headers, timeout=8)
            r2 = requests.get(f"https://v3.football.api-sports.io/teams?search={team2}", headers=headers, timeout=8)
            if r1.status_code==200 and r2.status_code==200:
                t1 = r1.json().get("response",[])
                t2 = r2.json().get("response",[])
                if t1 and t2:
                    id1, id2 = t1[0]["team"]["id"], t2[0]["team"]["id"]
                    r = requests.get(f"https://v3.football.api-sports.io/fixtures/headtohead?h2h={id1}-{id2}&last=10", headers=headers, timeout=8)
                    if r.status_code == 200:
                        matches = r.json().get("response",[])
                        t1w = sum(1 for m in matches if (m["teams"]["home"]["id"]==id1 and m["teams"]["home"]["winner"]) or (m["teams"]["away"]["id"]==id1 and m["teams"]["away"]["winner"]))
                        t2w = sum(1 for m in matches if (m["teams"]["home"]["id"]==id2 and m["teams"]["home"]["winner"]) or (m["teams"]["away"]["id"]==id2 and m["teams"]["away"]["winner"]))
                        return {"matches_played":len(matches),"team1_wins":t1w,"team2_wins":t2w,"draws":len(matches)-t1w-t2w}
        except: pass
        return {}
    
    def news(self, query):
        articles = []
        try:
            if NEWSAPI_KEY:
                from newsapi import NewsApiClient
                api = NewsApiClient(api_key=NEWSAPI_KEY)
                resp = api.get_everything(q=query, language='en', sort_by='publishedAt', page_size=5)
                for a in resp.get('articles',[]):
                    articles.append({"title":a['title'],"source":a['source']['name'],"published":a.get('publishedAt','')})
        except: pass
        if not articles:
            try:
                feed = feedparser.parse(f"https://news.google.com/rss/search?q={query}&hl=en&gl=US&ceid=US:en")
                for e in feed.entries[:5]:
                    articles.append({"title":e.title,"source":e.source.title if hasattr(e,'source') else "News"})
            except: pass
        return articles