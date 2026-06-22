import streamlit as st, requests
from datetime import datetime

st.set_page_config(page_title="Shadow Terminal", layout="wide")

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@300;400;500;600;700&display=swap');
*{font-family:'Inter',sans-serif}.stApp{background:#0B0E11}
.th{background:#161A1E;border-bottom:1px solid #2B3139;padding:10px 20px;display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}
.th .t{color:#F0B90B;font-weight:700;font-size:1.1rem}.th .s{color:#848E9C;font-size:0.7rem}
.tc{background:#161A1E;border:1px solid #2B3139;border-radius:4px;padding:14px;margin-bottom:10px}
.pt{font-size:0.7rem;font-weight:600;color:#848E9C;text-transform:uppercase;margin-bottom:10px;letter-spacing:1px;border-left:2px solid #F0B90B;padding-left:8px}
.kpi{display:flex;gap:8px;margin-bottom:8px}
.ki{background:#1E2329;border:1px solid #2B3139;border-radius:4px;padding:10px;flex:1;text-align:center}
.kl{color:#848E9C;font-size:0.6rem;text-transform:uppercase;letter-spacing:1px}
.kv{font-family:'Fira Code',monospace;font-size:1.3rem;font-weight:600;color:#EAECEF;margin:4px 0}
.g{color:#0ECB81}.r{color:#F6465D}.y{color:#F0B90B}
.ab{background:#1E2329;border-left:3px solid #F0B90B;padding:14px;margin:10px 0;border-radius:0 4px 4px 0}
.al{color:#F0B90B;font-size:0.65rem;font-weight:700;font-family:'Fira Code',monospace;text-transform:uppercase;margin-bottom:6px}
.at{color:#EAECEF;font-size:0.8rem;line-height:1.6}
.exec{background:#0D3320;border:1px solid #0ECB81;border-radius:4px;padding:14px;margin:8px 0}
.el{color:#0ECB81;font-size:0.6rem;text-transform:uppercase;letter-spacing:2px;font-family:'Fira Code',monospace}
.ev{color:#EAECEF;font-family:'Fira Code',monospace;font-size:0.9rem;font-weight:600}
.tag{display:inline-block;background:#1E2329;border:1px solid #0ECB81;border-radius:4px;padding:6px 12px;margin:3px;font-family:'Fira Code',monospace;font-size:0.75rem;color:#0ECB81}
.vote-pro{color:#0ECB81;font-size:0.65rem;padding:2px 0}.vote-con{color:#F6465D;font-size:0.65rem;padding:2px 0}.vote-neu{color:#F0B90B;font-size:0.65rem;padding:2px 0}
.stButton>button{background:#F0B90B;color:#0B0E11;border:none;border-radius:4px;font-weight:600;font-size:0.8rem;width:100%;padding:8px}
.stButton>button:hover{background:#C99A08}
.stTextInput>div>div>input{background:#0B0E11;border:1px solid #2B3139;color:#EAECEF;font-size:0.8rem;border-radius:4px}
.stSelectbox>div>div{background:#0B0E11;border:1px solid #2B3139;color:#EAECEF}
</style>""", unsafe_allow_html=True)

API = "http://127.0.0.1:8000"

if 'domain' not in st.session_state: st.session_state.domain = "trading"
if 'a1' not in st.session_state: st.session_state.a1 = "BTC-USD"
if 'a2' not in st.session_state: st.session_state.a2 = "USD"
if 'report' not in st.session_state: st.session_state.report = None

st.markdown(f"""<div class="th"><div style="display:flex;align-items:center;gap:20px;"><span class="t">🔶 SHADOW</span><span class="s">SUN TZU MIND</span></div><div style="font-family:'Fira Code',monospace;font-size:0.7rem;color:#848E9C;">{datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</div></div>""", unsafe_allow_html=True)

c1,c2,c3 = st.columns([1,2.2,1.3])

with c1:
    st.markdown('<div class="tc"><div class="pt">Search</div>', unsafe_allow_html=True)
    st.session_state.domain = st.selectbox("Domain", ["trading","sports"], index=0)
    
    if st.session_state.domain == "trading":
        st.session_state.a1 = st.text_input("Asset", st.session_state.a1, placeholder="BTC-USD, EURUSD=X, GC=F...")
        st.session_state.a2 = st.text_input("vs", st.session_state.a2, placeholder="USD")
    else:
        st.session_state.a1 = st.text_input("Team 1", st.session_state.a1, placeholder="France")
        st.session_state.a2 = st.text_input("Team 2", st.session_state.a2, placeholder="Senegal")
    
    st.markdown("<br>", unsafe_allow_html=True)
    btn = st.button("⚡ ANALYZE", use_container_width=True)
    st.caption("Full 13-chapter audit. Takes ~30 seconds.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="tc"><div class="pt">Quick Pick</div>', unsafe_allow_html=True)
    picks = [("BTC","BTC-USD","USD"),("ETH","ETH-USD","USD"),("Gold","GC=F","USD"),
             ("AAPL","AAPL","USD"),("EUR/USD","EURUSD=X","USD"),("France/Senegal","France","Senegal")]
    for label,v1,v2 in picks:
        if st.button(label, use_container_width=True):
            st.session_state.a1=v1; st.session_state.a2=v2
            st.session_state.domain="sports" if "France" in label else "trading"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

if btn:
    with st.spinner("13 chapters analyzing..."):
        try:
            resp = requests.post(f"{API}/analyze", json={
                "entity_1":st.session_state.a1,"entity_2":st.session_state.a2,"domain":st.session_state.domain
            }, timeout=180)
            if resp.status_code==200: st.session_state.report = resp.json()
            else: st.error(f"Error: {resp.status_code}")
        except Exception as e: st.error(str(e))

with c2:
    if st.session_state.report:
        r = st.session_state.report; q = r.get("quant",{}); e1 = q.get("e1",{}); e2 = q.get("e2",{})
        pro=r.get("pro_count",0); con=r.get("con_count",0); neu=r.get("neutral_count",0)
        
        st.markdown(f"""<div class="kpi">
            <div class="ki"><div class="kl">PICK</div><div class="kv g">{r.get('pick','?')}</div></div>
            <div class="ki"><div class="kl">STR</div><div class="kv">{e1.get('strength','?')}/{e2.get('strength','?')}</div></div>
            <div class="ki"><div class="kl">ENG</div><div class="kv">{e1.get('energy','?')}/{e2.get('energy','?')}</div></div>
            <div class="ki"><div class="kl">MOR</div><div class="kv">{e1.get('morale','?')}/{e2.get('morale','?')}</div></div>
            <div class="ki"><div class="kl">VOTE</div><div class="kv">{pro}P/{con}C/{neu}N</div></div>
        </div>""", unsafe_allow_html=True)
        
        st.markdown(f'<div class="ab"><div class="al">[BATTLE PLAN]</div><div class="at">{r.get("battle_plan","")}</div></div>', unsafe_allow_html=True)
        
        ex = r.get("execution",{})
        if ex:
            if st.session_state.domain == "trading":
                st.markdown(f"""<div class="exec">
                    <div style="display:flex;gap:20px;flex-wrap:wrap;">
                        <div><div class="el">Action</div><div class="ev" style="color:#0ECB81;">{ex.get('action','')}</div></div>
                        <div><div class="el">Entry</div><div class="ev">{ex.get('entry','')}</div></div>
                        <div><div class="el">Stop Loss</div><div class="ev" style="color:#F6465D;">{ex.get('stop_loss','')}</div></div>
                        <div><div class="el">Take Profit</div><div class="ev" style="color:#0ECB81;">{ex.get('take_profit','')}</div></div>
                        <div><div class="el">Risk</div><div class="ev">{ex.get('risk','')}</div></div>
                        <div><div class="el">Size</div><div class="ev">{ex.get('size','')}</div></div>
                    </div>
                </div>""", unsafe_allow_html=True)
            elif st.session_state.domain == "sports":
                markets=ex.get("markets",[]); conf=ex.get("confidence","")
                st.markdown(f"""<div class="exec">
                    <div class="el" style="margin-bottom:8px;">Betting Markets ({conf})</div>
                    <div>{"".join([f'<span class="tag">{m}</span>' for m in markets])}</div>
                    <div style="color:#848E9C;font-size:0.65rem;margin-top:8px;">{ex.get('hedge','')}</div>
                </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center;padding:60px;color:#848E9C;"><div style="font-size:3rem;opacity:0.2;">🔶</div><div>SHADOW</div><div style="font-size:0.7rem;">Sun Tzu Mind. 13 Chapters. Full Analysis.</div></div>', unsafe_allow_html=True)

with c3:
    if st.session_state.report:
        r = st.session_state.report
        st.markdown('<div class="tc"><div class="pt">13 Chapter Votes</div>', unsafe_allow_html=True)
        for v in r.get("chapter_verdicts",[]):
            c = "vote-pro" if v['verdict']=='PRO' else "vote-con" if v['verdict']=='CON' else "vote-neu"
            st.markdown(f'<div class="{c}">Ch.{v["chapter"]} {v["chapter_name"]}: {v["verdict"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<div style="text-align:center;color:#2B3139;font-size:0.55rem;padding:8px;">SHADOW · SUN TZU MIND · {datetime.now().strftime("%H:%M UTC")}</div>', unsafe_allow_html=True)