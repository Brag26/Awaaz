"""
Awaaz — Voice Bot Platform (No Auth)
"""

import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Awaaz", page_icon="🎙️", layout="wide",
                   initial_sidebar_state="expanded")

API = "http://127.0.0.1:4000/api"

# ─── CSS ──────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&family=Instrument+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap');

:root {
  --bg:#07090e; --bg2:#0c1018; --bg3:#101520;
  --b:rgba(255,255,255,0.07); --b2:rgba(255,255,255,0.13);
  --txt:#e6e1d8; --mut:#56637a; --mut2:#8491a6;
  --gold:#e8b84b; --gold2:#f5cf70;
  --teal:#3ecfb2; --red:#e85555; --blue:#4d9fff; --green:#3ecf8e;
  --r:14px; --rs:8px;
}
html,body,[class*="css"] { font-family:'Instrument Sans',sans-serif; background:var(--bg)!important; color:var(--txt); }
.stApp { background:var(--bg)!important; background-image:radial-gradient(ellipse 90% 50% at 50% -15%,rgba(232,184,75,.05),transparent),radial-gradient(ellipse 60% 40% at 85% 85%,rgba(62,207,178,.03),transparent); min-height:100vh; }
.block-container { padding:0 2rem 3rem!important; max-width:1440px!important; }
[data-testid="stSidebar"] { background:var(--bg2)!important; border-right:1px solid var(--b)!important; }
section[data-testid="stSidebar"] .block-container { padding:0!important; }
#MainMenu,footer,header,[data-testid="stToolbar"],.stDeployButton { visibility:hidden; display:none; }

.stButton>button { font-family:'Syne',sans-serif!important; font-weight:600!important; font-size:13px!important; letter-spacing:.04em!important; border-radius:var(--rs)!important; border:1px solid var(--b2)!important; background:rgba(255,255,255,.04)!important; color:var(--txt)!important; transition:all .18s!important; padding:10px 20px!important; width:100%!important; }
.stButton>button:hover { background:rgba(255,255,255,.08)!important; border-color:rgba(255,255,255,.22)!important; transform:translateY(-1px)!important; }
.btn-gold .stButton>button { background:var(--gold)!important; color:#07090e!important; border-color:var(--gold)!important; font-weight:700!important; box-shadow:0 0 22px rgba(232,184,75,.25)!important; }
.btn-gold .stButton>button:hover { background:var(--gold2)!important; box-shadow:0 0 34px rgba(232,184,75,.4)!important; }
.btn-red .stButton>button { background:rgba(232,85,85,.1)!important; color:var(--red)!important; border-color:rgba(232,85,85,.3)!important; }
.btn-ghost .stButton>button { background:transparent!important; border:none!important; color:var(--mut2)!important; font-family:'Instrument Sans',sans-serif!important; font-size:14px!important; font-weight:400!important; padding:10px 20px!important; border-radius:0!important; letter-spacing:0!important; text-align:left!important; justify-content:flex-start!important; }
.btn-ghost .stButton>button:hover { background:rgba(255,255,255,.04)!important; color:var(--txt)!important; transform:none!important; }
.btn-active .stButton>button { background:rgba(232,184,75,.08)!important; color:var(--gold)!important; border-left:2px solid var(--gold)!important; border-radius:0!important; }

.stTextInput>div>div>input,.stNumberInput>div>div>input { background:var(--bg3)!important; border:1px solid var(--b)!important; border-radius:var(--rs)!important; color:var(--txt)!important; font-family:'Space Mono',monospace!important; font-size:12px!important; padding:10px 14px!important; transition:border-color .2s!important; }
.stTextInput>div>div>input:focus { border-color:var(--gold)!important; box-shadow:0 0 0 3px rgba(232,184,75,.1)!important; }
.stTextInput label,.stNumberInput label,.stSelectbox label,.stSlider label,.stFileUploader label { font-family:'Syne',sans-serif!important; font-size:11px!important; font-weight:600!important; letter-spacing:.1em!important; text-transform:uppercase!important; color:var(--mut2)!important; }
.stSelectbox>div>div { background:var(--bg3)!important; border:1px solid var(--b)!important; border-radius:var(--rs)!important; color:var(--txt)!important; font-family:'Space Mono',monospace!important; font-size:12px!important; }
.stSlider>div>div>div>div { background:var(--gold)!important; }
.stProgress>div>div>div>div { background:linear-gradient(90deg,var(--gold),var(--teal))!important; border-radius:99px!important; }
.stProgress>div>div>div { background:rgba(255,255,255,.06)!important; border-radius:99px!important; }

[data-testid="stMetric"] { background:var(--bg2)!important; border:1px solid var(--b)!important; border-radius:var(--r)!important; padding:18px 20px!important; position:relative; overflow:hidden; }
[data-testid="stMetric"]::before { content:''; position:absolute; top:0; left:0; right:0; height:1px; background:linear-gradient(90deg,transparent,var(--gold),transparent); opacity:.4; }
[data-testid="stMetricLabel"]>div { font-family:'Syne',sans-serif!important; font-size:10px!important; font-weight:700!important; letter-spacing:.14em!important; text-transform:uppercase!important; color:var(--mut)!important; }
[data-testid="stMetricValue"]>div { font-family:'Space Mono',monospace!important; font-size:28px!important; font-weight:700!important; color:var(--txt)!important; line-height:1.1!important; }

.stDataFrame { border:1px solid var(--b)!important; border-radius:var(--r)!important; overflow:hidden!important; }
[data-testid="stForm"] { border:1px solid var(--b)!important; border-radius:var(--r)!important; background:var(--bg2)!important; padding:24px!important; }
.streamlit-expanderHeader { background:var(--bg2)!important; border:1px solid var(--b)!important; border-radius:var(--rs)!important; }
.streamlit-expanderContent { background:var(--bg3)!important; border:1px solid var(--b)!important; border-top:none!important; }
.stDownloadButton>button { font-family:'Syne',sans-serif!important; font-size:12px!important; font-weight:600!important; background:transparent!important; border:1px solid var(--b2)!important; color:var(--mut2)!important; border-radius:var(--rs)!important; padding:8px 16px!important; }
.stDownloadButton>button:hover { border-color:var(--gold)!important; color:var(--gold)!important; }
hr { border:none!important; border-top:1px solid var(--b)!important; margin:24px 0!important; }
.stTabs [data-baseweb="tab-list"] { background:transparent!important; gap:0!important; border-bottom:1px solid var(--b)!important; }
.stTabs [data-baseweb="tab"] { background:transparent!important; color:var(--mut)!important; border:none!important; font-family:'Syne',sans-serif!important; font-size:12px!important; font-weight:600!important; letter-spacing:.06em!important; padding:10px 20px!important; border-bottom:2px solid transparent!important; }
.stTabs [aria-selected="true"] { color:var(--gold)!important; border-bottom:2px solid var(--gold)!important; }
code { font-family:'Space Mono',monospace!important; font-size:11px!important; background:rgba(255,255,255,.06)!important; padding:2px 6px!important; border-radius:4px!important; color:var(--teal)!important; }

.logo { font-family:'Syne',sans-serif; font-size:26px; font-weight:800; letter-spacing:-.03em; background:linear-gradient(135deg,var(--gold),var(--gold2)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.page-title { font-family:'Syne',sans-serif; font-size:28px; font-weight:800; letter-spacing:-.02em; color:var(--txt); line-height:1; }
.page-sub { font-family:'Instrument Sans',sans-serif; font-size:14px; color:var(--mut2); margin-top:6px; font-weight:300; font-style:italic; }
.sec { font-family:'Syne',sans-serif; font-size:10px; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:var(--mut); margin-bottom:10px; margin-top:4px; }
.card { background:var(--bg2); border:1px solid var(--b); border-radius:var(--r); padding:22px; }
.card-gold { background:var(--bg2); border:1px solid rgba(232,184,75,.2); border-radius:var(--r); padding:22px; box-shadow:0 0 36px rgba(232,184,75,.05),inset 0 1px 0 rgba(232,184,75,.1); }
.badge { display:inline-flex; align-items:center; gap:5px; font-family:'Space Mono',monospace; font-size:10px; padding:3px 10px; border-radius:99px; }
.bg { background:rgba(62,207,142,.1); color:var(--green); border:1px solid rgba(62,207,142,.2); }
.bo { background:rgba(232,184,75,.1); color:var(--gold); border:1px solid rgba(232,184,75,.2); }
.br { background:rgba(232,85,85,.1); color:var(--red); border:1px solid rgba(232,85,85,.2); }
.bb { background:rgba(77,159,255,.1); color:var(--blue); border:1px solid rgba(77,159,255,.2); }
.bk { background:rgba(90,100,120,.15); color:var(--mut2); border:1px solid rgba(90,100,120,.2); }
.bt { background:rgba(62,207,178,.1); color:var(--teal); border:1px solid rgba(62,207,178,.2); }
.dot { display:inline-block; width:7px; height:7px; border-radius:50%; margin-right:6px; vertical-align:middle; }
.dg { background:var(--green); box-shadow:0 0 6px var(--green); }
.dr { background:var(--red); box-shadow:0 0 6px var(--red); }
.pulse { animation:pulse 2s ease-in-out infinite; }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.5;transform:scale(.85)} }
.waveform { display:flex; align-items:center; gap:3px; height:22px; }
.waveform span { display:inline-block; width:3px; border-radius:2px; background:var(--gold); animation:wave 1.2s ease-in-out infinite; }
.waveform span:nth-child(1){height:5px;animation-delay:0s}.waveform span:nth-child(2){height:13px;animation-delay:.1s}.waveform span:nth-child(3){height:19px;animation-delay:.2s}.waveform span:nth-child(4){height:13px;animation-delay:.3s}.waveform span:nth-child(5){height:7px;animation-delay:.4s}.waveform span:nth-child(6){height:15px;animation-delay:.5s}.waveform span:nth-child(7){height:9px;animation-delay:.6s}
@keyframes wave { 0%,100%{transform:scaleY(.4);opacity:.5} 50%{transform:scaleY(1);opacity:1} }
.live-pill { display:inline-flex; align-items:center; gap:7px; background:rgba(62,207,142,.08); border:1px solid rgba(62,207,142,.2); border-radius:99px; padding:5px 14px; font-family:'Syne',sans-serif; font-size:11px; font-weight:700; letter-spacing:.08em; color:var(--green); }
.info-row { display:flex; gap:22px; font-family:'Instrument Sans',sans-serif; font-size:13px; color:var(--mut2); margin:14px 0; flex-wrap:wrap; }
.info-row strong { color:var(--txt); font-weight:500; }
.assist-card { background:var(--bg3); border:1px solid var(--b); border-radius:var(--rs); padding:14px 18px; margin-bottom:8px; }
.empty { text-align:center; padding:50px 20px; }
.empty-icon { font-size:44px; opacity:.4; margin-bottom:12px; }
.empty-title { font-family:'Syne',sans-serif; font-size:15px; font-weight:700; color:var(--mut2); margin-bottom:6px; }
.empty-desc { font-size:13px; font-style:italic; font-family:'Instrument Sans',sans-serif; color:var(--mut); }
</style>
""", unsafe_allow_html=True)

# ─── State & API ──────────────────────────────────────────────────────────────

def init_state():
    for k, v in {"tab":"Campaign","contacts":None,"active_campaign_id":None}.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def GET(path, default=None):
    try:
        r = requests.get(f"{API}{path}", timeout=6)
        r.raise_for_status(); return r.json()
    except: return default

def POST(path, data=None):
    try:
        r = requests.post(f"{API}{path}", json=data or {}, timeout=10)
        r.raise_for_status(); return r.json(), None
    except requests.HTTPError as e:
        try: msg = e.response.json().get("detail", str(e))
        except: msg = str(e)
        return None, msg
    except Exception as e:
        return None, str(e)

def DELETE(path):
    try: requests.delete(f"{API}{path}", timeout=6)
    except: pass

def backend_alive():
    try: requests.get(f"{API.replace('/api','')}/health", timeout=2); return True
    except: return False

def assistant_opts():
    settings   = GET("/settings") or {}
    assistants = GET("/assistants") or []
    did   = settings.get("vapi_assistant_id","")
    short = did[:14]+"…" if len(did)>14 else did
    opts  = [("⭐  Default" + (f"  ·  {short}" if did else "  ·  not set"), did)]
    for a in assistants:
        lbl = f"🤖  {a['name']}"
        if a.get("description"): lbl += f"  ·  {a['description']}"
        opts.append((lbl, a["assistant_id"]))
    return opts

def asst_select(label, key):
    opts   = assistant_opts()
    labels = [o[0] for o in opts]
    idx    = st.selectbox(label, range(len(labels)), format_func=lambda i: labels[i], key=key)
    return opts[idx][1]

STATUS_META = {
    "pending":     ("bk","⬡","Pending"),
    "queued":      ("bo","◔","Queued"),
    "dialing":     ("bb","◑","Dialing"),
    "in-progress": ("bt","●","Live"),
    "completed":   ("bg","✓","Done"),
    "failed":      ("br","✗","Failed"),
    "no-answer":   ("bo","⊘","No Answer"),
    "starting":    ("bo","◔","Starting"),
    "running":     ("bg","●","Running"),
    "aborted":     ("br","✗","Aborted"),
}

def page_header(title, sub):
    st.markdown(f'<div style="padding:28px 0 20px;"><div class="page-title">{title}</div><div class="page-sub">{sub}</div></div>', unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────

alive = backend_alive()

with st.sidebar:
    st.markdown(f"""
    <div style="padding:24px 20px 20px;border-bottom:1px solid var(--b);">
      <div class="logo">आवाज़</div>
      <div style="font-family:'Syne',sans-serif;font-size:10px;font-weight:700;letter-spacing:.2em;color:var(--mut);text-transform:uppercase;margin-top:2px;">Awaaz</div>
      <div style="font-family:'Instrument Sans',sans-serif;font-size:11px;color:var(--mut);letter-spacing:.1em;text-transform:uppercase;margin-top:6px;">Voice Bot Platform</div>
    </div>
    <div style="padding:10px 20px;border-bottom:1px solid var(--b);">
      <span class="dot {'dg pulse' if alive else 'dr'}"></span>
      <span style="font-family:'Syne',sans-serif;font-size:11px;font-weight:600;letter-spacing:.06em;color:{'var(--green)' if alive else 'var(--red)'};">
        {'BACKEND LIVE' if alive else 'BACKEND OFFLINE'}
      </span>
    </div>
    """, unsafe_allow_html=True)

    if not alive:
        st.markdown("""
        <div style="padding:10px 20px;">
          <div style="font-family:'Space Mono',monospace;font-size:10px;color:var(--mut);background:rgba(255,255,255,.04);padding:10px;border-radius:6px;border:1px solid var(--b);">
            python -m uvicorn backend:app<br>&nbsp;&nbsp;--port 4000 --host 0.0.0.0
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="padding:12px 0 8px;">', unsafe_allow_html=True)
    nav = [("Campaign","🚀"),("Single Call","📞"),("Dashboard","📊"),
           ("Assistants","🤖"),("Settings","⚙️")]
    for tab, icon in nav:
        active = st.session_state.tab == tab
        css = "btn-active btn-ghost" if active else "btn-ghost"
        st.markdown(f'<div class="{css}">', unsafe_allow_html=True)
        if st.button(f"{icon}  {tab}", key=f"nav_{tab}", use_container_width=True):
            st.session_state.tab = tab; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="position:fixed;bottom:0;left:0;width:inherit;padding:14px 20px;border-top:1px solid var(--b);background:var(--bg2);">
      <div style="display:flex;align-items:center;gap:8px;">
        <div class="waveform"><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div>
        <span style="font-family:'Syne',sans-serif;font-size:10px;font-weight:700;color:var(--mut);letter-spacing:.1em;">VAPI · TWILIO</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  CAMPAIGN
# ══════════════════════════════════════════════════════════════════════════════

if st.session_state.tab == "Campaign":
    page_header("Bulk Campaign", "Upload contacts, pick a voice bot, launch at scale")

    col_l, col_r = st.columns([3,2], gap="large")
    with col_l:
        st.markdown('<div class="sec">01 · Upload Contact List</div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        uploaded = st.file_uploader("Drop CSV or Excel", type=["csv","xlsx","xls"], label_visibility="collapsed")
        if uploaded:
            try:
                df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
                df.columns = [c.strip().lower() for c in df.columns]
                pc = next((c for c in df.columns if any(k in c for k in ["phone","mobile","number"])), df.columns[0])
                nc = next((c for c in df.columns if "name" in c), None)
                df = df.rename(columns={pc:"phone"})
                if nc and nc != "phone": df = df.rename(columns={nc:"name"})
                else: df["name"] = [f"Contact {i+1}" for i in range(len(df))]
                df["phone"] = df["phone"].astype(str).str.strip()
                df = df[df["phone"].str.len()>5][["name","phone"]].reset_index(drop=True)
                st.session_state.contacts = df
                st.markdown(f'<div style="margin-top:10px;padding:12px 16px;background:rgba(62,207,142,.06);border:1px solid rgba(62,207,142,.15);border-radius:8px;"><div style="font-family:Syne,sans-serif;font-size:13px;font-weight:700;color:var(--green);">✅ {len(df)} contacts loaded</div><div style="font-family:Space Mono,monospace;font-size:10px;color:var(--mut);">{uploaded.name}</div></div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Parse error: {e}")
        st.markdown('<div style="margin-top:10px;font-family:Space Mono,monospace;font-size:10px;color:var(--mut);">Accepted: .csv · .xlsx · .xls  |  Columns: name, phone</div>', unsafe_allow_html=True)
        st.download_button("⬇ Sample CSV", data="name,phone\nAlex Kumar,+919876543210\nPriya Sharma,+919123456789",
                           file_name="sample.csv", mime="text/csv")
        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.contacts is not None:
            st.markdown('<div style="height:14px"></div><div class="sec">Preview</div>', unsafe_allow_html=True)
            p = st.session_state.contacts.head(12).copy(); p.index += 1
            st.dataframe(p, use_container_width=True, height=260)

    with col_r:
        st.markdown('<div class="sec">02 · Campaign Settings</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-gold">', unsafe_allow_html=True)
        cname    = st.text_input("Campaign Name", placeholder="e.g. May Follow-up")
        sel_asst = asst_select("Voice Assistant", "camp_asst")
        settings = GET("/settings") or {}
        cpm      = settings.get("calls_per_minute", 10)
        if st.session_state.contacts is not None:
            n   = len(st.session_state.contacts)
            est = round(n/max(cpm,1),1)
            st.markdown(f"""
            <div style="margin:14px 0;padding:14px 16px;background:var(--bg3);border-radius:8px;border:1px solid var(--b);">
              <div style="display:flex;justify-content:space-between;margin-bottom:7px;">
                <span style="font-family:'Syne',sans-serif;font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);">Contacts</span>
                <span style="font-family:'Space Mono',monospace;font-size:13px;font-weight:700;color:var(--txt);">{n:,}</span>
              </div>
              <div style="display:flex;justify-content:space-between;margin-bottom:7px;">
                <span style="font-family:'Syne',sans-serif;font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);">Rate</span>
                <span style="font-family:'Space Mono',monospace;font-size:13px;font-weight:700;color:var(--txt);">{cpm}/min</span>
              </div>
              <div style="display:flex;justify-content:space-between;">
                <span style="font-family:'Syne',sans-serif;font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);">Est. Time</span>
                <span style="font-family:'Space Mono',monospace;font-size:13px;font-weight:700;color:var(--gold);">~{est} min</span>
              </div>
            </div>""", unsafe_allow_html=True)
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        launch = st.button("▶  Launch Campaign", disabled=(st.session_state.contacts is None or not cname))
        st.markdown('</div>', unsafe_allow_html=True)
        if launch:
            if not alive: st.error("Backend offline.")
            else:
                data, err = POST("/campaign/start", {
                    "campaign_name": cname,
                    "contacts": st.session_state.contacts.to_dict("records"),
                    "assistant_id": sel_asst or None,
                })
                if err: st.error(err)
                else:
                    st.session_state.active_campaign_id = data["campaign_id"]
                    st.session_state.tab = "Dashboard"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="height:14px"></div><div class="card"><div class="sec">💡 Tips</div><div style="font-family:\'Instrument Sans\',sans-serif;font-size:13px;color:var(--mut2);line-height:1.8;">· E.164 format: <code>+91XXXXXXXXXX</code><br>· Max 60 calls/min per VAPI plan<br>· Set up webhook for live status</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SINGLE CALL
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.tab == "Single Call":
    page_header("Single Call", "Trigger a one-off call — great for testing an assistant")
    c1, c2 = st.columns([3,2], gap="large")
    with c1:
        st.markdown('<div class="card-gold">', unsafe_allow_html=True)
        r1, r2 = st.columns(2)
        with r1: name  = st.text_input("Contact Name", placeholder="e.g. Rahul Verma")
        with r2: phone = st.text_input("Phone Number", placeholder="+919876543210")
        asst_id = asst_select("Voice Assistant", "single_asst")
        st.markdown('<div style="height:8px"></div><div class="btn-gold">', unsafe_allow_html=True)
        call_btn = st.button("📞  Call Now")
        st.markdown('</div>', unsafe_allow_html=True)
        if call_btn:
            if not phone: st.warning("Phone number required.")
            elif not alive: st.error("Backend offline.")
            else:
                data, err = POST("/call/single", {"name":name or "Test","phone":phone,"assistant_id":asst_id or None})
                if err: st.error(err)
                else: st.markdown(f'<div style="margin-top:14px;padding:14px 18px;background:rgba(62,207,142,.06);border:1px solid rgba(62,207,142,.2);border-radius:10px;"><div style="font-family:Syne,sans-serif;font-size:13px;font-weight:700;color:var(--green);">✓ Call triggered</div><div style="font-family:Space Mono,monospace;font-size:10px;color:var(--mut);">VAPI ID: {data.get("vapi_call_id","—")}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><div class="sec">Recent Calls</div>', unsafe_allow_html=True)
        calls = GET("/calls") or []
        if not calls:
            st.markdown('<div class="empty" style="padding:30px 10px;"><div class="empty-icon">📵</div><div class="empty-title">No calls yet</div></div>', unsafe_allow_html=True)
        else:
            for c in reversed(calls[-8:]):
                cls,ic,lbl = STATUS_META.get(c["status"],("bk","?",c["status"]))
                st.markdown(f'<div style="padding:10px 0;border-bottom:1px solid var(--b);display:flex;justify-content:space-between;align-items:center;"><div><div style="font-family:Syne,sans-serif;font-size:13px;font-weight:600;color:var(--txt);">{c["name"]}</div><div style="font-family:Space Mono,monospace;font-size:10px;color:var(--mut);margin-top:2px;">{c["phone"]}</div></div><span class="badge {cls}">{ic} {lbl}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.tab == "Dashboard":
    page_header("Dashboard", "Monitor campaign progress and call statuses in real time")
    campaigns = GET("/campaigns") or []
    if not campaigns:
        st.markdown('<div class="empty"><div class="empty-icon">📊</div><div class="empty-title">No campaigns yet</div><div class="empty-desc">Launch a campaign to see live data</div></div>', unsafe_allow_html=True)
    else:
        ids    = [c["id"] for c in campaigns]
        labels = [f"{c['name']}  ·  {c['id'][:8]}" for c in campaigns]
        def_idx = 0
        if st.session_state.active_campaign_id in ids:
            def_idx = ids.index(st.session_state.active_campaign_id)
        sel    = st.selectbox("Campaign", labels, index=def_idx, label_visibility="collapsed")
        sel_id = ids[labels.index(sel)]
        camp   = GET(f"/campaign/{sel_id}")
        if not camp: st.error("Could not load campaign."); st.stop()

        stats   = camp.get("stats",{})
        running = camp.get("status") in ("running","starting")
        if running:
            st.markdown('<div style="margin-bottom:16px;"><span class="live-pill"><span class="dot dg pulse"></span>LIVE · AUTO-REFRESHING</span></div>', unsafe_allow_html=True)

        c1,c2,c3,c4,c5 = st.columns(5)
        c1.metric("Total",       f"{stats.get('total',0):,}")
        c2.metric("Dispatched",  f"{stats.get('dispatched',0):,}")
        c3.metric("✅ Done",     f"{stats.get('completed',0):,}")
        c4.metric("🔴 Failed",   f"{stats.get('failed',0):,}")
        c5.metric("🔵 Live",     f"{stats.get('dialing',0):,}")

        total = max(stats.get("total",1),1)
        done  = stats.get("completed",0)+stats.get("failed",0)+stats.get("no_answer",0)
        st.progress(done/total, text=f"{done:,} / {total:,}  ·  {round(done/total*100)}%")

        ci, ca = st.columns([4,1])
        with ci:
            s = camp.get("status",""); cls,ic,lbl = STATUS_META.get(s,("bk","?",s))
            started = (camp.get("started_at") or "")[:19] or "—"
            ended   = (camp.get("ended_at") or "")[:19] or "—"
            st.markdown(f'<div class="info-row"><span>Status <strong>{ic} {lbl}</strong></span><span>Started <strong>{started}</strong></span><span>Ended <strong>{ended}</strong></span></div>', unsafe_allow_html=True)
        with ca:
            if running:
                st.markdown('<div class="btn-red">', unsafe_allow_html=True)
                if st.button("⛔  Abort"): POST(f"/campaign/{sel_id}/abort"); st.warning("Abort sent.")
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        calls = camp.get("calls",[])
        t_all,t_ok,t_fail = st.tabs(["All Calls","✓ Completed","✗ Failed / No Answer"])

        def call_table(rows):
            if not rows:
                st.markdown('<div class="empty" style="padding:30px;"><div class="empty-desc">No calls here</div></div>', unsafe_allow_html=True); return
            df = pd.DataFrame(rows)
            cols = [c for c in ["name","phone","status","duration","error"] if c in df.columns]
            df = df[cols].copy()
            df["status"] = df["status"].map(lambda s: STATUS_META.get(s,("","?",s))[1]+" "+STATUS_META.get(s,("","?",s))[2])
            if "duration" in df.columns: df["duration"] = df["duration"].apply(lambda d: f"{int(d)}s" if d else "—")
            if "error"    in df.columns: df["error"]    = df["error"].fillna("—")
            df.columns = [c.capitalize() for c in df.columns]
            st.dataframe(df, use_container_width=True, height=360)

        with t_all:
            call_table(calls)
            if calls: st.download_button("⬇ Export CSV", pd.DataFrame(calls).to_csv(index=False), file_name=f"awaaz_{sel_id[:8]}.csv", mime="text/csv")
        with t_ok:   call_table([c for c in calls if c.get("status")=="completed"])
        with t_fail: call_table([c for c in calls if c.get("status") in ("failed","no-answer")])

        if running: time.sleep(3); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  ASSISTANTS
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.tab == "Assistants":
    page_header("Voice Assistants", "Manage all your VAPI bots")
    assistants = GET("/assistants") or []
    col_f, col_l = st.columns([2,3], gap="large")
    with col_f:
        st.markdown('<div class="sec">Add Assistant</div><div class="card-gold">', unsafe_allow_html=True)
        with st.form("add_asst"):
            aname = st.text_input("Display Name", placeholder="e.g. Sales Bot")
            asst_id_val = st.text_input("VAPI Assistant ID", placeholder="asst_…")
            adesc = st.text_input("Description", placeholder="e.g. English outbound")
            st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
            ok = st.form_submit_button("➕  Add")
            st.markdown('</div>', unsafe_allow_html=True)
            if ok:
                if not aname or not asst_id_val: st.warning("Name and ID required.")
                else:
                    data, err = POST("/assistants", {"name":aname,"assistant_id":asst_id_val,"description":adesc})
                    if err: st.error(err)
                    else: st.success(f"✅ {aname} added!"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_l:
        st.markdown(f'<div class="sec">{len(assistants)} assistant{"s" if len(assistants)!=1 else ""}</div>', unsafe_allow_html=True)
        if not assistants:
            st.markdown('<div class="empty" style="padding:40px 20px;"><div class="empty-icon">🤖</div><div class="empty-title">No assistants yet</div></div>', unsafe_allow_html=True)
        else:
            for a in assistants:
                ca, cb = st.columns([6,1])
                with ca:
                    st.markdown(f'<div class="assist-card"><div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;"><span style="font-size:20px;">🤖</span><div><div style="font-family:Syne,sans-serif;font-size:14px;font-weight:700;color:var(--txt);">{a["name"]}</div><div style="font-family:\'Instrument Sans\',sans-serif;font-size:12px;color:var(--mut2);font-style:italic;">{a.get("description") or "No description"}</div></div></div><div style="font-family:Space Mono,monospace;font-size:10px;color:var(--mut);">ID: {a["assistant_id"]}</div></div>', unsafe_allow_html=True)
                with cb:
                    st.markdown('<div style="padding-top:10px;">', unsafe_allow_html=True)
                    if st.button("🗑", key=f"da_{a['id']}"): DELETE(f"/assistants/{a['id']}"); st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SETTINGS
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.tab == "Settings":
    page_header("Settings", "Configure your VAPI and Twilio credentials")
    current = GET("/settings") or {}
    col_m, col_g = st.columns([3,2], gap="large")
    with col_m:
        st.markdown('<div class="sec">API Credentials</div>', unsafe_allow_html=True)
        with st.form("settings_form"):
            st.markdown('<div class="sec" style="margin-top:0;">VAPI</div>', unsafe_allow_html=True)
            g1,g2 = st.columns(2)
            with g1: vapi_key  = st.text_input("API Key", value=current.get("vapi_api_key",""), type="password", placeholder="vapi_…")
            with g2: vapi_asst = st.text_input("Default Assistant ID", value=current.get("vapi_assistant_id",""), placeholder="asst_…")
            st.markdown('<div class="sec">Twilio / Phone</div>', unsafe_allow_html=True)
            twilio = st.text_input("VAPI Phone Number ID", value=current.get("twilio_phone_number",""), placeholder="Phone Number ID from VAPI dashboard")
            st.markdown('<div class="sec">Rate Limiting</div>', unsafe_allow_html=True)
            cpm = st.slider("Calls per minute", 1, 60, int(current.get("calls_per_minute",10)))
            st.markdown('<div class="btn-gold" style="margin-top:8px;">', unsafe_allow_html=True)
            saved = st.form_submit_button("💾  Save Settings")
            st.markdown('</div>', unsafe_allow_html=True)
            if saved:
                _, err = POST("/settings", {"vapi_api_key":vapi_key,"vapi_assistant_id":vapi_asst,
                                            "twilio_phone_number":twilio,"calls_per_minute":cpm})
                if err: st.error(err)
                else: st.success("✅ Settings saved!")
    with col_g:
        st.markdown('<div class="sec">Setup Guide</div>', unsafe_allow_html=True)
        with st.expander("🔑 VAPI API Key", expanded=True):
            st.markdown("1. Go to **[vapi.ai](https://vapi.ai)** → API Keys\n2. Copy your key → paste above")
        with st.expander("📞 Phone Number ID"):
            st.markdown("1. VAPI → **Phone Numbers**\n2. Import your Twilio number\n3. Copy the **Phone Number ID** (not `+91…`)")
        with st.expander("🔔 Webhook for live status"):
            st.markdown("VAPI → Assistant → **Server URL**:\n```\nhttps://your-domain.com/api/webhook/vapi\n```")

# ─── Footer ───────────────────────────────────────────────────────────────────

st.markdown("""
<div style="margin-top:40px;padding-top:18px;border-top:1px solid var(--b);display:flex;justify-content:space-between;align-items:center;">
  <span style="font-family:'Syne',sans-serif;font-size:11px;font-weight:800;letter-spacing:.1em;color:var(--mut);">आवाज़ · AWAAZ</span>
  <span style="font-family:'Space Mono',monospace;font-size:10px;color:var(--mut);">VAPI + TWILIO + PYTHON</span>
  <a href="https://docs.vapi.ai" target="_blank" style="font-family:'Syne',sans-serif;font-size:11px;font-weight:600;color:var(--gold);text-decoration:none;letter-spacing:.06em;">VAPI DOCS →</a>
</div>
""", unsafe_allow_html=True)
