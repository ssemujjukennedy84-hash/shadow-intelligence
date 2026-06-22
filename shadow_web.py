"""
Shadow - Cloud-Ready Web App + Mobile PWA
Deploy to Render (free). API key box for broker connection.
"""

import sys, os, json, hashlib, importlib.util, requests as req
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, session, redirect
from flask_cors import CORS

# ─── CONFIG ───
PASSWORD_HASH = hashlib.sha256("Kennedy999.".encode()).hexdigest()
SECRET_KEY = os.environ.get("SECRET_KEY", "shadow-strategic-intelligence-2026")
PORT = int(os.environ.get("PORT", 5000))

# ─── LOAD ENGINES ───
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(BASE, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

ct = load_module("combined_trading", "engine/combined_trading.py")
ste = load_module("sun_tzu_engine", "engine/sun_tzu_engine.py")
qe = load_module("quant_engine", "engine/quant_engine.py")
dm = load_module("data_mapper", "engine/data_mapper.py")

CombinedTrading = ct.CombinedTrading
SunTzuEngine = ste.SunTzuEngine
QuantEngine = qe.QuantEngine

LEAGUE_IDS = {"epl":39,"laliga":140,"bundesliga":78,"seriea":135,"ligue1":61}

app = Flask(__name__)
app.secret_key = SECRET_KEY
CORS(app)

# Store broker API keys in memory
broker_config = {"api_key": "", "api_secret": "", "exchange": ""}

# ═══════════════════════════════════════════════
# LOGIN PAGE
# ═══════════════════════════════════════════════
LOGIN_PAGE = """
<!DOCTYPE html>
<html><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Shadow - Login</title>
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#0B0E11">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Inter',sans-serif}
body{background:#0B0E11;display:flex;align-items:center;justify-content:center;min-height:100vh}
.box{background:#161A1E;border:1px solid #2B3139;border-radius:8px;padding:40px;width:360px;text-align:center}
.box h1{color:#F0B90B;font-size:1.5rem;margin-bottom:8px}
.box p{color:#848E9C;font-size:0.8rem;margin-bottom:24px}
input{width:100%;background:#0B0E11;border:1px solid #2B3139;color:#EAECEF;padding:12px;border-radius:4px;font-size:0.9rem;margin-bottom:12px}
button{width:100%;background:#F0B90B;color:#0B0E11;border:none;padding:12px;border-radius:4px;font-weight:600;font-size:0.9rem;cursor:pointer}
button:hover{background:#C99A08}
.error{color:#F6465D;font-size:0.75rem;margin-top:8px}
</style></head>
<body><div class="box">
<h1>🔶 SHADOW</h1><p>Strategic Intelligence</p>
<form method="POST"><input type="password" name="password" placeholder="Password" autofocus><button type="submit">Enter</button></form>
{% if error %}<div class="error">{{ error }}</div>{% endif %}
</div></body></html>"""

# ═══════════════════════════════════════════════
# MAIN DASHBOARD
# ═══════════════════════════════════════════════
DASHBOARD = """
<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Shadow Intelligence</title>
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#0B0E11">
<link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Inter',sans-serif}
body{background:#0B0E11;color:#EAECEF;min-height:100vh}
.topbar{background:#161A1E;border-bottom:1px solid #2B3139;padding:8px 16px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
.topbar h1{color:#F0B90B;font-size:1rem;font-weight:700}
.tabs{display:flex;gap:3px;background:#1E2329;border-radius:6px;padding:2px}
.tab{padding:6px 10px;border-radius:4px;font-weight:600;font-size:0.6rem;cursor:pointer;border:none;background:transparent;color:#848E9C}
.tab.active{background:#F0B90B;color:#0B0E11}
.container{max-width:900px;margin:0 auto;padding:12px}
.card{background:#161A1E;border:1px solid #2B3139;border-radius:6px;padding:14px;margin-bottom:10px}
.card-title{font-size:0.65rem;font-weight:600;color:#848E9C;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;border-left:2px solid #F0B90B;padding-left:8px}
.row{display:flex;gap:8px;margin-bottom:8px}
input,select{flex:1;background:#0B0E11;border:1px solid #2B3139;color:#EAECEF;padding:10px;border-radius:4px;font-size:0.8rem}
.btn{width:100%;background:#F0B90B;color:#0B0E11;border:none;padding:10px;border-radius:4px;font-weight:600;font-size:0.8rem;cursor:pointer;margin-top:6px}
.btn:hover{background:#C99A08}.btn:disabled{opacity:0.5}
.kpi-row{display:grid;grid-template-columns:repeat(5,1fr);gap:4px;margin-bottom:8px}
.kpi{background:#1E2329;border:1px solid #2B3139;border-radius:4px;padding:6px;text-align:center}
.kl{color:#848E9C;font-size:0.45rem;text-transform:uppercase;letter-spacing:1px}
.kv{font-family:'Fira Code',monospace;font-size:0.95rem;font-weight:600;margin-top:2px}
.g{color:#0ECB81}.r{color:#F6465D}.y{color:#F0B90B}
.exec{background:#0D3320;border:1px solid #0ECB81;border-radius:4px;padding:8px;margin-bottom:6px}
.exec-g{display:grid;grid-template-columns:repeat(3,1fr);gap:4px}
.ei{text-align:center}.el{color:#0ECB81;font-size:0.45rem;text-transform:uppercase;letter-spacing:1px;font-family:'Fira Code',monospace}
.ev{font-family:'Fira Code',monospace;font-size:0.7rem;font-weight:600;margin-top:2px}
.tag{display:inline-block;background:#1E2329;border:1px solid #0ECB81;border-radius:3px;padding:3px 6px;margin:2px;font-family:'Fira Code',monospace;font-size:0.6rem;color:#0ECB81}
.qbtn{background:#1E2329;color:#848E9C;border:1px solid #2B3139;padding:4px 6px;border-radius:3px;font-size:0.55rem;cursor:pointer;margin:1px}
.qbtn:hover{background:#2B3139;color:#EAECEF}
.vote{font-size:0.55rem;padding:1px 0}.hidden{display:none}.note{color:#848E9C;font-size:0.55rem;margin-top:3px}
.manual-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.manual-box{background:#1E2329;border:1px solid #2B3139;border-radius:4px;padding:8px}
.manual-label{color:#848E9C;font-size:0.5rem;text-transform:uppercase;margin-bottom:3px}
.ds{display:inline-block;padding:2px 6px;border-radius:3px;font-size:0.45rem;margin-left:4px}
.ds-live{background:#0D3320;color:#0ECB81}.ds-manual{background:#332A0D;color:#F0B90B}
.offseason{background:#332A0D;border:1px solid #F0B90B;border-radius:4px;padding:8px;margin-bottom:10px;text-align:center;color:#F0B90B;font-size:0.7rem}
.live-badge{background:#0D3320;color:#0ECB81;font-size:0.45rem;padding:2px 5px;border-radius:3px;margin-left:4px}
.logout-btn{background:transparent;color:#848E9C;border:1px solid #2B3139;padding:4px 10px;border-radius:4px;font-size:0.6rem;cursor:pointer;text-decoration:none}
.api-box{background:#161A1E;border:1px solid #F0B90B;border-radius:4px;padding:10px;margin-bottom:10px}
.api-title{color:#F0B90B;font-size:0.6rem;font-weight:600;text-transform:uppercase;margin-bottom:6px}
.api-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px}
.status-dot{display:inline-block;width:6px;height:6px;border-radius:50%;margin-right:4px}
.status-online{background:#0ECB81}.status-offline{background:#F6465D}
</style></head>
<body>

<div class="topbar">
    <h1>🔶 SHADOW</h1>
    <div class="tabs">
        <button class="tab active" onclick="switchTab('trading')">📈 TRADING <span class="live-badge">LIVE</span></button>
        <button class="tab" onclick="switchTab('leagues')">⚽ LEAGUES</button>
        <button class="tab" onclick="switchTab('worldcup')">🏆 WORLD CUP</button>
    </div>
    <div style="display:flex;gap:8px;align-items:center">
        <span style="font-size:0.6rem;color:#848E9C" id="brokerStatus"><span class="status-dot status-offline"></span>Broker</span>
        <a href="/logout" class="logout-btn">Logout</a>
    </div>
</div>

<div class="container">

    <!-- API KEY BOX -->
    <div class="api-box" id="apiBox">
        <div class="api-title">🔑 Broker API Connection</div>
        <div class="api-grid">
            <input id="apiKey" placeholder="API Key" onchange="saveBrokerConfig()">
            <input id="apiSecret" placeholder="API Secret" onchange="saveBrokerConfig()">
            <select id="apiExchange" onchange="saveBrokerConfig()">
                <option value="">Select Exchange</option>
                <option value="binance">Binance</option>
                <option value="binance_testnet">Binance Testnet</option>
                <option value="alpaca">Alpaca (Stocks)</option>
                <option value="oanda">OANDA (Forex)</option>
                <option value="bybit">Bybit</option>
                <option value="kraken">Kraken</option>
            </select>
        </div>
        <div class="note">Shadow uses these keys to execute trades. Stored in session only.</div>
    </div>

    <!-- TRADING -->
    <div id="panelTrading">
        <div class="card">
            <div class="card-title">Trading · Wyckoff + Sun Tzu · 52% Proven</div>
            <input id="tSymbol" placeholder="Symbol (BTC-USD, ETH-USD, AAPL, GC=F...)" value="BTC-USD">
            <button class="btn" id="tBtn" onclick="analyze('trading')">⚡ ANALYZE</button>
            <div style="margin-top:6px;display:flex;flex-wrap:wrap;gap:2px">
                <button class="qbtn" onclick="setT('BTC-USD')">BTC</button><button class="qbtn" onclick="setT('ETH-USD')">ETH</button>
                <button class="qbtn" onclick="setT('SOL-USD')">SOL</button><button class="qbtn" onclick="setT('GC=F')">Gold</button>
                <button class="qbtn" onclick="setT('AAPL')">Apple</button><button class="qbtn" onclick="setT('TSLA')">Tesla</button>
                <button class="qbtn" onclick="setT('NVDA')">NVIDIA</button><button class="qbtn" onclick="setT('EURUSD=X')">EUR/USD</button>
            </div>
        </div>
        <div id="tResult"></div>
    </div>

    <!-- LEAGUES -->
    <div id="panelLeagues" class="hidden">
        <div class="offseason">⚽ OFF-SEASON — No live matches. 2026/27 starts August.</div>
        <div class="card"><div class="card-title">League Analysis</div>
            <select id="lLeague" style="margin-bottom:8px"><option value="epl">Premier League</option><option value="laliga">La Liga</option><option value="bundesliga">Bundesliga</option><option value="seriea">Serie A</option><option value="ligue1">Ligue 1</option></select>
            <div class="row"><input id="lTeam1" placeholder="Home Team" value="Man City"><span style="color:#848E9C;align-self:center">vs</span><input id="lTeam2" placeholder="Away Team" value="Arsenal"></div>
            <button class="btn" id="lBtn" onclick="analyze('leagues')">⚡ ANALYZE</button>
        </div><div id="lResult"></div>
    </div>

    <!-- WORLD CUP -->
    <div id="panelWorldCup" class="hidden">
        <div class="card"><div class="card-title">World Cup 2026 · Manual Intel</div>
            <div class="row"><input id="wTeam1" placeholder="Team 1" value="France"><span style="color:#848E9C;align-self:center">vs</span><input id="wTeam2" placeholder="Team 2" value="Senegal"></div>
            <div class="manual-grid">
                <div class="manual-box"><div class="manual-label">Team 1</div><input id="w1form" placeholder="Form (WWDWW)" style="margin-bottom:3px"><input id="w1gf" placeholder="Goals For" style="margin-bottom:3px"><input id="w1ga" placeholder="Goals Against" style="margin-bottom:3px"><input id="w1played" placeholder="Matches"></div>
                <div class="manual-box"><div class="manual-label">Team 2</div><input id="w2form" placeholder="Form (WLDLW)" style="margin-bottom:3px"><input id="w2gf" placeholder="Goals For" style="margin-bottom:3px"><input id="w2ga" placeholder="Goals Against" style="margin-bottom:3px"><input id="w2played" placeholder="Matches"></div>
            </div>
            <button class="btn" id="wBtn" onclick="analyze('worldcup')">⚡ ANALYZE</button>
        </div><div id="wResult"></div>
    </div>

</div>

<script>
function switchTab(t){
    document.getElementById('panelTrading').className=t==='trading'?'':'hidden';
    document.getElementById('panelLeagues').className=t==='leagues'?'':'hidden';
    document.getElementById('panelWorldCup').className=t==='worldcup'?'':'hidden';
    document.querySelectorAll('.tab')[0].className=t==='trading'?'tab active':'tab';
    document.querySelectorAll('.tab')[1].className=t==='leagues'?'tab active':'tab';
    document.querySelectorAll('.tab')[2].className=t==='worldcup'?'tab active':'tab';
}
function setT(s){document.getElementById('tSymbol').value=s}

function saveBrokerConfig(){
    const key=document.getElementById('apiKey').value;
    const secret=document.getElementById('apiSecret').value;
    const exchange=document.getElementById('apiExchange').value;
    fetch('/broker/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({api_key:key,api_secret:secret,exchange:exchange})})
    .then(()=>{
        const dot=document.querySelector('#brokerStatus .status-dot');
        if(key&&exchange){dot.className='status-dot status-online';document.getElementById('brokerStatus').innerHTML='<span class="status-dot status-online"></span>'+exchange;}
        else{dot.className='status-dot status-offline';}
    });
}

async function analyze(domain){
    let body={};
    if(domain==='trading'){body={symbol:document.getElementById('tSymbol').value};}
    else if(domain==='leagues'){body={entity_1:document.getElementById('lTeam1').value,entity_2:document.getElementById('lTeam2').value,league:document.getElementById('lLeague').value};}
    else if(domain==='worldcup'){
        const f1=document.getElementById('w1form').value,f2=document.getElementById('w2form').value;
        body={entity_1:document.getElementById('wTeam1').value,entity_2:document.getElementById('wTeam2').value,home_stats:{name:document.getElementById('wTeam1').value,form:f1,goals_for:parseInt(document.getElementById('w1gf').value)||0,goals_against:parseInt(document.getElementById('w1ga').value)||0,played:parseInt(document.getElementById('w1played').value)||0,wins:(f1.match(/W/g)||[]).length,losses:(f1.match(/L/g)||[]).length,draws:(f1.match(/D/g)||[]).length},away_stats:{name:document.getElementById('wTeam2').value,form:f2,goals_for:parseInt(document.getElementById('w2gf').value)||0,goals_against:parseInt(document.getElementById('w2ga').value)||0,played:parseInt(document.getElementById('w2played').value)||0,wins:(f2.match(/W/g)||[]).length,losses:(f2.match(/L/g)||[]).length,draws:(f2.match(/D/g)||[]).length}};
    }
    const btnId=domain==='trading'?'tBtn':domain==='leagues'?'lBtn':'wBtn';
    const resultId=domain==='trading'?'tResult':domain==='leagues'?'lResult':'wResult';
    const btn=document.getElementById(btnId);btn.disabled=true;btn.textContent='Analyzing...';
    try{
        const r=await fetch('/analyze/'+domain,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
        document.getElementById(resultId).innerHTML=render(await r.json(),domain);
    }catch(e){document.getElementById(resultId).innerHTML='<div class="card" style="text-align:center;color:#F6465D">Error</div>';}
    btn.disabled=false;btn.textContent='⚡ ANALYZE';
}

function render(d,domain){
    if(d.error) return '<div class="card" style="background:#332A0D;border-color:#F0B90B;text-align:center">'+d.error+'</div>';
    if(d.data_source==='OFF-SEASON') return '<div class="card" style="background:#332A0D;border-color:#F0B90B;text-align:center;color:#F0B90B">'+d.battle_plan+'</div>';
    let h='<div class="card">';
    if(domain==='trading'){
        h+='<div class="kpi-row"><div class="kpi"><div class="kl">ACTION</div><div class="kv g">'+d.action+'</div></div><div class="kpi"><div class="kl">CONF</div><div class="kv">'+d.confidence+'</div></div><div class="kpi"><div class="kl">WYCKOFF</div><div class="kv" style="font-size:0.6rem">'+d.wyckoff.phase+'</div></div>';
        const st=d.sun_tzu||{};h+='<div class="kpi"><div class="kl">SUN TZU</div><div class="kv">'+st.pro+'P/'+st.con+'C</div></div>';
        const tf=d.timeframes||{};h+='<div class="kpi"><div class="kl">TF</div><div class="kv" style="font-size:0.55rem">'+tf.daily+'/'+tf['4h']+'/'+tf['1h']+'/'+tf['15m']+'</div></div></div>';
        const ex=d.execution;if(ex)h+='<div class="exec"><div class="exec-g"><div class="ei"><div class="el">Entry</div><div class="ev">$'+ex.entry+'</div></div><div class="ei"><div class="el">Stop Loss</div><div class="ev r">$'+ex.stop_loss+'</div></div><div class="ei"><div class="el">Take Profit</div><div class="ev g">$'+ex.take_profit+'</div></div></div></div>';
    }else{
        const q=d.quant||{},e1=q.e1||{},e2=q.e2||{};
        h+='<div class="kpi-row"><div class="kpi"><div class="kl">PICK</div><div class="kv g">'+d.pick+'</div></div><div class="kpi"><div class="kl">STR</div><div class="kv">'+e1.strength+'/'+e2.strength+'</div></div><div class="kpi"><div class="kl">ENG</div><div class="kv">'+e1.energy+'/'+e2.energy+'</div></div><div class="kpi"><div class="kl">MOR</div><div class="kv">'+e1.morale+'/'+e2.morale+'</div></div><div class="kpi"><div class="kl">VOTE</div><div class="kv">'+d.pro_count+'P/'+d.con_count+'C</div></div></div>';
        const ex=d.execution;if(ex)h+='<div class="exec"><div class="el" style="margin-bottom:3px">Markets ('+ex.confidence+')</div><div>'+(ex.markets||[]).map(m=>'<span class="tag">'+m+'</span>').join('')+'</div></div>';
        const vs=d.chapter_breakdown||[];if(vs.length)vs.slice(0,13).forEach(v=>{const c=v.verdict==='PRO'?'g':v.verdict==='CON'?'r':'y';h+='<div class="vote '+c+'">Ch.'+v.chapter+' '+v.chapter_name+': '+v.verdict+'</div>';});
    }
    h+='</div>';return h;
}

// Load saved broker config
fetch('/broker/config').then(r=>r.json()).then(d=>{
    if(d.api_key){document.getElementById('apiKey').value=d.api_key;document.getElementById('apiSecret').value=d.api_secret;document.getElementById('apiExchange').value=d.exchange;
    const dot=document.querySelector('#brokerStatus .status-dot');dot.className='status-dot status-online';document.getElementById('brokerStatus').innerHTML='<span class="status-dot status-online"></span>'+d.exchange;}
});
</script>
</body></html>"""

# ═══════════════════════════════════════════════
# PWA MANIFEST
# ═══════════════════════════════════════════════
@app.route("/manifest.json")
def manifest():
    return jsonify({
        "name":"Shadow Intelligence","short_name":"Shadow",
        "start_url":"/","display":"standalone",
        "background_color":"#0B0E11","theme_color":"#0B0E11",
        "icons":[{"src":"data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🔶</text></svg>","sizes":"any"}]
    })

# ═══════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════
@app.route("/", methods=["GET", "POST"])
def login():
    if session.get("authenticated"): return render_template_string(DASHBOARD)
    error = None
    if request.method == "POST":
        if hashlib.sha256(request.form.get("password","").encode()).hexdigest() == PASSWORD_HASH:
            session["authenticated"] = True; return render_template_string(DASHBOARD)
        error = "Incorrect password"
    return render_template_string(LOGIN_PAGE, error=error)

@app.route("/logout")
def logout(): session.clear(); return redirect("/")

@app.route("/broker/save", methods=["POST"])
def save_broker():
    if not session.get("authenticated"): return jsonify({"error":"Unauthorized"}), 401
    data = request.get_json()
    broker_config["api_key"] = data.get("api_key","")
    broker_config["api_secret"] = data.get("api_secret","")
    broker_config["exchange"] = data.get("exchange","")
    return jsonify({"status":"saved"})

@app.route("/broker/config")
def get_broker():
    return jsonify(broker_config)

@app.route("/analyze/trading", methods=["POST"])
def analyze_trading():
    if not session.get("authenticated"): return jsonify({"error":"Unauthorized"}), 401
    try:
        data = request.get_json()
        engine = CombinedTrading(data.get("symbol","BTC-USD"))
        result = engine.analyze()
        # If broker connected and signal is not WAIT, execute
        if broker_config["api_key"] and result["action"] != "WAIT":
            result["broker_ready"] = True
            result["exchange"] = broker_config["exchange"]
        return jsonify(result)
    except Exception as e:
        return jsonify({"action":"WAIT","error":str(e)})

@app.route("/analyze/leagues", methods=["POST"])
def analyze_leagues():
    if not session.get("authenticated"): return jsonify({"error":"Unauthorized"}), 401
    try:
        data = request.get_json()
        e1_name = data.get("entity_1",""); e2_name = data.get("entity_2","")
        league = data.get("league","epl"); league_id = LEAGUE_IDS.get(league, 39)
        raw1 = data.get("home_stats",{}) or {}; raw1["name"] = e1_name
        raw2 = data.get("away_stats",{}) or {}; raw2["name"] = e2_name
        data_found = False
        try:
            headers = {"x-apisports-key": "dd28cc88d9d6aa5d195a88d04b9c401c"}
            for name, raw in [(e1_name, raw1), (e2_name, raw2)]:
                resp = req.get(f"https://v3.football.api-sports.io/teams?search={name}", headers=headers, timeout=8)
                if resp.status_code == 200 and resp.json().get("response"):
                    team = resp.json()["response"][0]["team"]
                    stats_resp = req.get(f"https://v3.football.api-sports.io/teams/statistics?team={team['id']}&season=2026&league={league_id}", headers=headers, timeout=8)
                    if stats_resp.status_code == 200:
                        stats = stats_resp.json().get("response",{})
                        if isinstance(stats, list): stats = stats[0] if stats else {}
                        fixtures = stats.get("fixtures",{})
                        if fixtures.get("played",{}).get("total",0) > 0:
                            data_found = True; goals = stats.get("goals",{})
                            raw.update({"form":stats.get("form",""),"played":fixtures.get("played",{}).get("total",0),"wins":fixtures.get("wins",{}).get("total",0),"draws":fixtures.get("draws",{}).get("total",0),"losses":fixtures.get("loses",{}).get("total",0),"goals_for":goals.get("for",{}).get("total",{}).get("total",0) if isinstance(goals.get("for",{}).get("total",{}),dict) else 0,"goals_against":goals.get("against",{}).get("total",{}).get("total",0) if isinstance(goals.get("against",{}).get("total",{}),dict) else 0})
        except: pass
        if not data_found: return jsonify({"pick":"NO DATA","battle_plan":f"Off-season. No live {league.upper()} data.","data_source":"OFF-SEASON"})
        raw1 = dm.map_sports(raw1); raw2 = dm.map_sports(raw2)
        quant = QuantEngine(); q1 = quant.score_sports(raw1); q2 = quant.score_sports(raw2)
        e1 = {**raw1,"strength":q1.get("strength",5),"energy":q1.get("energy",50),"morale":q1.get("morale",5)}
        e2 = {**raw2,"strength":q2.get("strength",5),"energy":q2.get("energy",50),"morale":q2.get("morale",5)}
        engine = SunTzuEngine(); result = engine.analyze(e1, e2)
        result["quant"] = {"e1":q1,"e2":q2}; result["data_source"] = f"LIVE ({league.upper()})"
        margin = abs(e1.get("strength",5)-e2.get("strength",5))
        if margin>3: markets,conf=["Match Winner","Handicap -1.5","Over 2.5 Goals"],"HIGH"
        elif margin>1.5: markets,conf=["Match Winner","Double Chance","Under 3.5 Goals"],"MEDIUM"
        else: markets,conf=["Draw No Bet","Under 2.5 Goals","BTTS NO"],"LOW"
        result["execution"] = {"markets":markets,"confidence":conf}
        return jsonify(result)
    except Exception as e: return jsonify({"error":str(e)})

@app.route("/analyze/worldcup", methods=["POST"])
def analyze_worldcup():
    if not session.get("authenticated"): return jsonify({"error":"Unauthorized"}), 401
    try:
        data = request.get_json()
        raw1 = data.get("home_stats",{}) or {}; raw1["name"] = data.get("entity_1","")
        raw2 = data.get("away_stats",{}) or {}; raw2["name"] = data.get("entity_2","")
        raw1 = dm.map_sports(raw1); raw2 = dm.map_sports(raw2)
        quant = QuantEngine(); q1 = quant.score_sports(raw1); q2 = quant.score_sports(raw2)
        e1 = {**raw1,"strength":q1.get("strength",5),"energy":q1.get("energy",50),"morale":q1.get("morale",5)}
        e2 = {**raw2,"strength":q2.get("strength",5),"energy":q2.get("energy",50),"morale":q2.get("morale",5)}
        engine = SunTzuEngine(); result = engine.analyze(e1, e2)
        result["quant"] = {"e1":q1,"e2":q2}; result["data_source"] = "MANUAL"
        margin = abs(e1.get("strength",5)-e2.get("strength",5))
        if margin>3: markets,conf=["Match Winner","Handicap -1.5","Over 2.5 Goals"],"HIGH"
        elif margin>1.5: markets,conf=["Match Winner","Double Chance","Under 3.5 Goals"],"MEDIUM"
        else: markets,conf=["Draw No Bet","Under 2.5 Goals","BTTS NO"],"LOW"
        result["execution"] = {"markets":markets,"confidence":conf}
        return jsonify(result)
    except Exception as e: return jsonify({"error":str(e)})


if __name__ == "__main__":
    print("=" * 50)
    print("🔶 SHADOW - CLOUD READY")
    print(f"   http://0.0.0.0:{PORT}")
    print("   Password: Kennedy999.")
    print("=" * 50)
    app.run(host="0.0.0.0", port=PORT, debug=False)