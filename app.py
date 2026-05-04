"""
Volant — Voice Bot Platform
Premium Streamlit UI · VAPI + Twilio + Python
"""

import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# ─── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Volant",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

API = "http://localhost:4000/api"

# ─── Premium CSS ──────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Instrument+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:        #080b10;
  --bg2:       #0d1117;
  --bg3:       #111720;
  --border:    rgba(255,255,255,0.07);
  --border2:   rgba(255,255,255,0.12);
  --text:      #e8e3da;
  --muted:     #5a6478;
  --muted2:    #8892a4;
  --gold:      #e8b84b;
  --gold2:     #f5d07a;
  --gold-glow: rgba(232,184,75,0.15);
  --teal:      #3ecfb2;
  --red:       #e85555;
  --blue:      #4d9fff;
  --green:     #3ecf8e;
  --radius:    14px;
  --radius-sm: 8px;
}

html, body, [class*="css"] {
  font-family: 'Instrument Sans', sans-serif;
  background: var(--bg) !important;
  color: var(--text);
}

.stApp {
  background: var(--bg) !important;
  background-image:
    radial-gradient(ellipse 80% 50% at 50% -20%, rgba(232,184,75,0.06), transparent),
    radial-gradient(ellipse 60% 40% at 80% 80%, rgba(62,207,178,0.04), transparent);
  min-height: 100vh;
}

.block-container {
  padding: 0 2rem 3rem 2rem !important;
  max-width: 1440px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--bg2) !important;
  border-right: 1px solid var(--border) !important;
  padding: 0 !important;
}
[data-testid="stSidebar"] > div:first-child {
  padding: 0;
}
section[data-testid="stSidebar"] .block-container {
  padding: 0 !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.stDeployButton { display: none; }

/* ── Buttons ── */
.stButton > button {
  font-family: 'Syne', sans-serif !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  letter-spacing: 0.04em !important;
  border-radius: var(--radius-sm) !important;
  border: 1px solid var(--border2) !important;
  background: rgba(255,255,255,0.04) !important;
  color: var(--text) !important;
  transition: all 0.18s ease !important;
  padding: 10px 20px !important;
  width: 100% !important;
}
.stButton > button:hover {
  background: rgba(255,255,255,0.08) !important;
  border-color: rgba(255,255,255,0.2) !important;
  transform: translateY(-1px) !important;
}

/* Primary gold button */
.btn-primary .stButton > button {
  background: var(--gold) !important;
  color: #080b10 !important;
  border-color: var(--gold) !important;
  font-weight: 700 !important;
  box-shadow: 0 0 24px rgba(232,184,75,0.25) !important;
}
.btn-primary .stButton > button:hover {
  background: var(--gold2) !important;
  box-shadow: 0 0 36px rgba(232,184,75,0.4) !important;
  transform: translateY(-2px) !important;
}

/* Danger button */
.btn-danger .stButton > button {
  background: rgba(232,85,85,0.1) !important;
  color: var(--red) !important;
  border-color: rgba(232,85,85,0.3) !important;
}
.btn-danger .stButton > button:hover {
  background: rgba(232,85,85,0.2) !important;
  box-shadow: 0 0 20px rgba(232,85,85,0.2) !important;
}

/* Ghost nav button */
.nav-btn .stButton > button {
  background: transparent !important;
  border: none !important;
  text-align: left !important;
  justify-content: flex-start !important;
  color: var(--muted2) !important;
  font-family: 'Instrument Sans', sans-serif !important;
  font-size: 14px !important;
  font-weight: 400 !important;
  padding: 10px 20px !important;
  border-radius: 0 !important;
  letter-spacing: 0 !important;
  transition: all 0.15s !important;
}
.nav-btn .stButton > button:hover {
  background: rgba(255,255,255,0.04) !important;
  color: var(--text) !important;
  transform: none !important;
}
.nav-btn-active .stButton > button {
  background: rgba(232,184,75,0.08) !important;
  color: var(--gold) !important;
  border-left: 2px solid var(--gold) !important;
  border-radius: 0 !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
  background: var(--bg3) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text) !important;
  font-family: 'Space Mono', monospace !important;
  font-size: 12px !important;
  padding: 10px 14px !important;
  transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 3px rgba(232,184,75,0.1) !important;
}
.stTextInput label, .stNumberInput label, .stSelectbox label,
.stSlider label, .stFileUploader label {
  font-family: 'Syne', sans-serif !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
  color: var(--muted2) !important;
}

/* Selectbox */
.stSelectbox > div > div {
  background: var(--bg3) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text) !important;
  font-family: 'Space Mono', monospace !important;
  font-size: 12px !important;
}

/* Slider */
.stSlider > div > div > div > div {
  background: var(--gold) !important;
}

/* ── Progress bar ── */
.stProgress > div > div > div > div {
  background: linear-gradient(90deg, var(--gold), var(--teal)) !important;
  border-radius: 99px !important;
}
.stProgress > div > div > div {
  background: rgba(255,255,255,0.06) !important;
  border-radius: 99px !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
  background: var(--bg2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  padding: 20px 22px !important;
  position: relative;
  overflow: hidden;
}
[data-testid="stMetric"]::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
  opacity: 0.4;
}
[data-testid="stMetricLabel"] > div {
  font-family: 'Syne', sans-serif !important;
  font-size: 10px !important;
  font-weight: 700 !important;
  letter-spacing: 0.14em !important;
  text-transform: uppercase !important;
  color: var(--muted) !important;
}
[data-testid="stMetricValue"] > div {
  font-family: 'Space Mono', monospace !important;
  font-size: 30px !important;
  font-weight: 700 !important;
  color: var(--text) !important;
  line-height: 1.1 !important;
}

/* ── Dataframe ── */
.stDataFrame {
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  overflow: hidden !important;
}
.stDataFrame [data-testid="stDataFrameResizable"] {
  background: var(--bg2) !important;
}

/* ── Expander ── */
details summary {
  font-family: 'Syne', sans-serif !important;
  font-size: 13px !important;
  font-weight: 600 !important;
}
.streamlit-expanderHeader {
  background: var(--bg2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
}
.streamlit-expanderContent {
  background: var(--bg3) !important;
  border: 1px solid var(--border) !important;
  border-top: none !important;
}

/* ── Alerts ── */
.stAlert {
  border-radius: var(--radius-sm) !important;
  border: 1px solid !important;
  font-family: 'Instrument Sans', sans-serif !important;
  font-size: 13px !important;
}
div[data-baseweb="notification"] {
  border-radius: var(--radius-sm) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
  background: var(--bg3) !important;
  border: 2px dashed var(--border2) !important;
  border-radius: var(--radius) !important;
  transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
  border-color: var(--gold) !important;
}
[data-testid="stFileUploaderDropzone"] {
  background: transparent !important;
}

/* ── Form ── */
[data-testid="stForm"] {
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  background: var(--bg2) !important;
  padding: 24px !important;
}

/* ── Download button ── */
.stDownloadButton > button {
  font-family: 'Syne', sans-serif !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  background: transparent !important;
  border: 1px solid var(--border2) !important;
  color: var(--muted2) !important;
  border-radius: var(--radius-sm) !important;
  padding: 8px 16px !important;
}
.stDownloadButton > button:hover {
  border-color: var(--gold) !important;
  color: var(--gold) !important;
  background: var(--gold-glow) !important;
}

/* ── Divider ── */
hr {
  border: none !important;
  border-top: 1px solid var(--border) !important;
  margin: 28px 0 !important;
}

/* ── Custom classes ── */
.Volant-logo {
  font-family: 'Syne', sans-serif;
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.03em;
  background: linear-gradient(135deg, var(--gold), var(--gold2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
}

.Volant-tagline {
  font-family: 'Instrument Sans', sans-serif;
  font-size: 11px;
  color: var(--muted);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-top: 2px;
}

.page-title {
  font-family: 'Syne', sans-serif;
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--text);
  line-height: 1;
}

.page-sub {
  font-family: 'Instrument Sans', sans-serif;
  font-size: 14px;
  color: var(--muted2);
  margin-top: 6px;
  font-weight: 300;
  font-style: italic;
}

.section-label {
  font-family: 'Syne', sans-serif;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 12px;
  margin-top: 4px;
}

.card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
  position: relative;
  overflow: hidden;
}

.card-glow {
  background: var(--bg2);
  border: 1px solid rgba(232,184,75,0.2);
  border-radius: var(--radius);
  padding: 24px;
  box-shadow: 0 0 40px rgba(232,184,75,0.06), inset 0 1px 0 rgba(232,184,75,0.12);
}

.status-dot {
  display: inline-block;
  width: 7px; height: 7px;
  border-radius: 50%;
  margin-right: 7px;
  vertical-align: middle;
}
.dot-green  { background: var(--green); box-shadow: 0 0 6px var(--green); }
.dot-gold   { background: var(--gold);  box-shadow: 0 0 6px var(--gold); }
.dot-red    { background: var(--red);   box-shadow: 0 0 6px var(--red); }
.dot-blue   { background: var(--blue);  box-shadow: 0 0 6px var(--blue); }
.dot-grey   { background: var(--muted); }

.badge {
  display: inline-flex; align-items: center; gap: 5px;
  font-family: 'Space Mono', monospace;
  font-size: 10px;
  padding: 3px 10px;
  border-radius: 99px;
  font-weight: 400;
}
.badge-green { background: rgba(62,207,142,0.1);  color: var(--green); border: 1px solid rgba(62,207,142,0.2); }
.badge-gold  { background: rgba(232,184,75,0.1);  color: var(--gold);  border: 1px solid rgba(232,184,75,0.2); }
.badge-red   { background: rgba(232,85,85,0.1);   color: var(--red);   border: 1px solid rgba(232,85,85,0.2); }
.badge-blue  { background: rgba(77,159,255,0.1);  color: var(--blue);  border: 1px solid rgba(77,159,255,0.2); }
.badge-grey  { background: rgba(90,100,120,0.15); color: var(--muted2);border: 1px solid rgba(90,100,120,0.2); }
.badge-teal  { background: rgba(62,207,178,0.1);  color: var(--teal);  border: 1px solid rgba(62,207,178,0.2); }

.assistant-card {
  background: var(--bg3);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 16px 20px;
  margin-bottom: 10px;
  transition: border-color 0.2s;
}
.assistant-card:hover {
  border-color: var(--border2);
}
.assistant-name {
  font-family: 'Syne', sans-serif;
  font-size: 15px;
  font-weight: 700;
  color: var(--text);
}
.assistant-id {
  font-family: 'Space Mono', monospace;
  font-size: 11px;
  color: var(--muted);
  margin-top: 3px;
}
.assistant-desc {
  font-family: 'Instrument Sans', sans-serif;
  font-size: 12px;
  color: var(--muted2);
  font-style: italic;
  margin-top: 4px;
}

.stat-label {
  font-family: 'Syne', sans-serif;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--muted);
}

.stat-value {
  font-family: 'Space Mono', monospace;
  font-size: 32px;
  font-weight: 700;
  color: var(--text);
  line-height: 1;
  margin-top: 6px;
}

.live-pill {
  display: inline-flex; align-items: center; gap: 7px;
  background: rgba(62,207,142,0.08);
  border: 1px solid rgba(62,207,142,0.2);
  border-radius: 99px;
  padding: 5px 14px;
  font-family: 'Syne', sans-serif;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--green);
}

.info-row {
  display: flex; gap: 24px;
  font-family: 'Instrument Sans', sans-serif;
  font-size: 13px;
  color: var(--muted2);
  margin: 16px 0;
  flex-wrap: wrap;
}
.info-row span { display: flex; align-items: center; gap: 6px; }
.info-row strong { color: var(--text); font-weight: 500; }

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.85); }
}
.pulse { animation: pulse 2s ease-in-out infinite; }

@keyframes shimmer {
  0% { background-position: -200% center; }
  100% { background-position: 200% center; }
}

.waveform {
  display: flex; align-items: center; gap: 3px; height: 24px;
}
.waveform span {
  display: inline-block; width: 3px; border-radius: 2px;
  background: var(--gold);
  animation: wave 1.2s ease-in-out infinite;
}
.waveform span:nth-child(1) { height: 6px;  animation-delay: 0s; }
.waveform span:nth-child(2) { height: 14px; animation-delay: 0.1s; }
.waveform span:nth-child(3) { height: 20px; animation-delay: 0.2s; }
.waveform span:nth-child(4) { height: 14px; animation-delay: 0.3s; }
.waveform span:nth-child(5) { height: 8px;  animation-delay: 0.4s; }
.waveform span:nth-child(6) { height: 16px; animation-delay: 0.5s; }
.waveform span:nth-child(7) { height: 10px; animation-delay: 0.6s; }
@keyframes wave {
  0%, 100% { transform: scaleY(0.4); opacity: 0.5; }
  50% { transform: scaleY(1); opacity: 1; }
}

.sidebar-section {
  padding: 20px 16px 8px 16px;
}
.sidebar-nav-item {
  padding: 2px 0;
}
.sidebar-divider {
  height: 1px;
  background: var(--border);
  margin: 12px 16px;
}
.sidebar-footer {
  padding: 16px;
  margin-top: auto;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--muted);
}
.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}
.empty-title {
  font-family: 'Syne', sans-serif;
  font-size: 16px;
  font-weight: 700;
  color: var(--muted2);
  margin-bottom: 8px;
}
.empty-desc {
  font-size: 13px;
  font-style: italic;
  font-family: 'Instrument Sans', sans-serif;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
  background: transparent !important;
  gap: 0 !important;
  border-bottom: 1px solid var(--border) !important;
  padding-bottom: 0 !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--muted) !important;
  border: none !important;
  font-family: 'Syne', sans-serif !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  letter-spacing: 0.06em !important;
  padding: 10px 20px !important;
  border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
  color: var(--gold) !important;
  border-bottom: 2px solid var(--gold) !important;
}

/* Code blocks */
code {
  font-family: 'Space Mono', monospace !important;
  font-size: 11px !important;
  background: rgba(255,255,255,0.06) !important;
  padding: 2px 6px !important;
  border-radius: 4px !important;
  color: var(--teal) !important;
}

</style>
""", unsafe_allow_html=True)

# ─── State ────────────────────────────────────────────────────────────────────

def init_state():
    for k, v in {
        "contacts": None,
        "file_name": None,
        "active_campaign_id": None,
        "tab": "Campaign",
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── API ──────────────────────────────────────────────────────────────────────

def api_get(path, default=None):
    try:
        r = requests.get(f"{API}{path}", timeout=5)
        r.raise_for_status()
        return r.json()
    except:
        return default

def api_post(path, data=None):
    try:
        r = requests.post(f"{API}{path}", json=data or {}, timeout=10)
        r.raise_for_status()
        return r.json(), None
    except Exception as e:
        return None, str(e)

def backend_alive():
    try:
        requests.get(f"{API.replace('/api','')}/health", timeout=2)
        return True
    except:
        return False

def get_assistant_options():
    assistants = api_get("/assistants", [])
    settings   = api_get("/settings", {})
    default_id = settings.get("vapi_assistant_id", "")
    short = default_id[:16] + "…" if len(default_id) > 16 else default_id
    options = [("⭐  Default" + (f"  ·  {short}" if default_id else "  ·  not set"), default_id)]
    for a in assistants:
        lbl = f"🤖  {a['name']}"
        if a.get("description"):
            lbl += f"  ·  {a['description']}"
        options.append((lbl, a["assistant_id"]))
    return options

def assistant_selectbox(label, key):
    options = get_assistant_options()
    labels  = [o[0] for o in options]
    idx = st.selectbox(label, range(len(labels)), format_func=lambda i: labels[i], key=key)
    return options[idx][1]

STATUS_META = {
    "pending":     ("grey",  "⬡", "Pending"),
    "queued":      ("gold",  "◔", "Queued"),
    "dialing":     ("blue",  "◑", "Dialing"),
    "in-progress": ("teal",  "●", "Live"),
    "completed":   ("green", "✓", "Completed"),
    "failed":      ("red",   "✗", "Failed"),
    "no-answer":   ("gold",  "⊘", "No Answer"),
    "starting":    ("gold",  "◔", "Starting"),
    "running":     ("green", "●", "Running"),
    "aborted":     ("red",   "✗", "Aborted"),
}

def status_badge(status):
    c, ic, lbl = STATUS_META.get(status, ("grey", "?", status))
    return f'<span class="badge badge-{c}">{ic} {lbl}</span>'

# ─── Sidebar ─────────────────────────────────────────────────────────────────

with st.sidebar:
    alive = backend_alive()

    # Logo
    st.markdown("""
    <div style="padding: 28px 20px 20px 20px; border-bottom: 1px solid var(--border);">
      <div class="Volant-logo">आवाज़</div>
      <div style="font-family:'Syne',sans-serif;font-size:11px;font-weight:700;letter-spacing:0.2em;color:var(--muted);margin-top:2px;text-transform:uppercase;">Volant</div>
      <div class="Volant-tagline" style="margin-top:6px;">Voice Bot Platform</div>
    </div>
    """, unsafe_allow_html=True)

    # Backend status
    st.markdown(f"""
    <div style="padding:12px 20px;border-bottom:1px solid var(--border);">
      <span class="status-dot {'dot-green pulse' if alive else 'dot-red'}"></span>
      <span style="font-family:'Syne',sans-serif;font-size:11px;font-weight:600;letter-spacing:0.06em;color:{'var(--green)' if alive else 'var(--red)'};">
        {'BACKEND LIVE' if alive else 'BACKEND OFFLINE'}
      </span>
    </div>
    """, unsafe_allow_html=True)

    if not alive:
        st.markdown("""
        <div style="padding:10px 20px;">
          <div style="font-family:'Space Mono',monospace;font-size:10px;color:var(--muted);background:rgba(255,255,255,0.04);padding:10px;border-radius:6px;border:1px solid var(--border);">
            uvicorn backend:app \\<br>&nbsp;&nbsp;--port 4000
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Nav
    st.markdown('<div style="padding:16px 0 8px 0;">', unsafe_allow_html=True)

    nav_items = [
        ("Campaign",   "🚀", "Bulk call campaigns"),
        ("Single Call","📞", "One-off test calls"),
        ("Dashboard",  "📊", "Live call tracking"),
        ("Assistants", "🤖", "Manage voice bots"),
        ("Settings",   "⚙️", "API credentials"),
    ]
    for tab, icon, desc in nav_items:
        active = st.session_state.tab == tab
        css_class = "nav-btn-active nav-btn" if active else "nav-btn"
        st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
        if st.button(f"{icon}  {tab}", key=f"nav_{tab}", use_container_width=True):
            st.session_state.tab = tab
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar footer
    st.markdown("""
    <div style="position:fixed;bottom:0;left:0;width:inherit;padding:16px 20px;border-top:1px solid var(--border);background:var(--bg2);">
      <div style="display:flex;align-items:center;gap:8px;">
        <div class="waveform">
          <span></span><span></span><span></span><span></span><span></span><span></span><span></span>
        </div>
        <span style="font-family:'Syne',sans-serif;font-size:10px;font-weight:700;color:var(--muted);letter-spacing:0.1em;">VAPI · TWILIO</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
#  PAGES
# ════════════════════════════════════════════════════════════════════════════════

# ─── Campaign ─────────────────────────────────────────────────────────────────

if st.session_state.tab == "Campaign":

    st.markdown("""
    <div style="padding: 32px 0 24px 0;">
      <div class="page-title">Bulk Campaign</div>
      <div class="page-sub">Upload contacts, pick a voice bot, launch calls at scale</div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        st.markdown('<div class="section-label">01 · Upload Contact List</div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Drop CSV or Excel here",
            type=["csv", "xlsx", "xls"],
            label_visibility="collapsed",
            help="Columns needed: phone (required), name (optional)"
        )

        if uploaded:
            try:
                if uploaded.name.endswith(".csv"):
                    df = pd.read_csv(uploaded)
                else:
                    df = pd.read_excel(uploaded)

                df.columns = [c.strip().lower() for c in df.columns]
                phone_col = next((c for c in df.columns if any(k in c for k in ["phone","mobile","number"])), df.columns[0])
                name_col  = next((c for c in df.columns if "name" in c), None)

                df = df.rename(columns={phone_col: "phone"})
                if name_col and name_col != "phone":
                    df = df.rename(columns={name_col: "name"})
                else:
                    df["name"] = [f"Contact {i+1}" for i in range(len(df))]

                df["phone"] = df["phone"].astype(str).str.strip()
                df = df[df["phone"].str.len() > 5][["name", "phone"]].reset_index(drop=True)

                st.session_state.contacts = df
                st.session_state.file_name = uploaded.name

                st.markdown(f"""
                <div style="margin-top:12px;padding:14px 18px;background:rgba(62,207,142,0.06);border:1px solid rgba(62,207,142,0.15);border-radius:8px;display:flex;align-items:center;gap:10px;">
                  <span style="font-size:20px;">✅</span>
                  <div>
                    <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:var(--green);">{len(df)} contacts loaded</div>
                    <div style="font-family:'Space Mono',monospace;font-size:10px;color:var(--muted);margin-top:2px;">{uploaded.name}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Parse error: {e}")

        st.markdown("""
        <div style="margin-top:14px;font-family:'Space Mono',monospace;font-size:10px;color:var(--muted);">
          Accepted: .csv · .xlsx · .xls &nbsp;|&nbsp; Columns: name, phone
        </div>
        """, unsafe_allow_html=True)

        sample = "name,phone\nAlex Kumar,+919876543210\nPriya Sharma,+919123456789\nRaj Patel,+917890123456"
        st.download_button("⬇ Download sample CSV", data=sample, file_name="sample_contacts.csv", mime="text/csv")

        st.markdown('</div>', unsafe_allow_html=True)

        # Preview
        if st.session_state.contacts is not None:
            st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Contact Preview</div>', unsafe_allow_html=True)
            preview = st.session_state.contacts.head(15).copy()
            preview.index = preview.index + 1
            st.dataframe(preview, use_container_width=True, height=280)
            if len(st.session_state.contacts) > 15:
                st.markdown(f'<div style="font-family:\'Space Mono\',monospace;font-size:10px;color:var(--muted);margin-top:6px;">+{len(st.session_state.contacts)-15} more contacts not shown</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-label">02 · Campaign Settings</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-glow">', unsafe_allow_html=True)

        campaign_name   = st.text_input("Campaign Name", placeholder="e.g. April Follow-up Drive")
        selected_asst   = assistant_selectbox("Voice Assistant", key="campaign_asst")

        settings = api_get("/settings", {})
        cpm      = settings.get("calls_per_minute", 10)

        if st.session_state.contacts is not None:
            n       = len(st.session_state.contacts)
            est_min = round(n / max(cpm, 1), 1)
            st.markdown(f"""
            <div style="margin:16px 0;padding:14px 18px;background:var(--bg3);border-radius:8px;border:1px solid var(--border);">
              <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                <span style="font-family:'Syne',sans-serif;font-size:10px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--muted);">Contacts</span>
                <span style="font-family:'Space Mono',monospace;font-size:13px;font-weight:700;color:var(--text);">{n:,}</span>
              </div>
              <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                <span style="font-family:'Syne',sans-serif;font-size:10px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--muted);">Rate</span>
                <span style="font-family:'Space Mono',monospace;font-size:13px;font-weight:700;color:var(--text);">{cpm}/min</span>
              </div>
              <div style="display:flex;justify-content:space-between;">
                <span style="font-family:'Syne',sans-serif;font-size:10px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--muted);">Est. Duration</span>
                <span style="font-family:'Space Mono',monospace;font-size:13px;font-weight:700;color:var(--gold);">~{est_min} min</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        disabled = st.session_state.contacts is None or not campaign_name
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("▶  Launch Campaign", disabled=disabled):
            if not alive:
                st.error("Backend is offline. Start it first.")
            else:
                data, err = api_post("/campaign/start", {
                    "campaign_name": campaign_name,
                    "contacts": st.session_state.contacts.to_dict("records"),
                    "assistant_id": selected_asst or None,
                })
                if err:
                    st.error(f"Error: {err}")
                else:
                    st.session_state.active_campaign_id = data["campaign_id"]
                    st.session_state.tab = "Dashboard"
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Tips card
        st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);padding:20px;">
          <div style="font-family:'Syne',sans-serif;font-size:10px;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:var(--muted);margin-bottom:12px;">💡 Quick Tips</div>
          <div style="font-family:'Instrument Sans',sans-serif;font-size:13px;color:var(--muted2);line-height:1.8;">
            · Phone numbers in E.164 format: <code>+91XXXXXXXXXX</code><br>
            · Max 60 calls/min per VAPI plan<br>
            · All calls logged in Dashboard<br>
            · Set up webhook for live status
          </div>
        </div>
        """, unsafe_allow_html=True)


# ─── Single Call ──────────────────────────────────────────────────────────────

elif st.session_state.tab == "Single Call":

    st.markdown("""
    <div style="padding: 32px 0 24px 0;">
      <div class="page-title">Single Call</div>
      <div class="page-sub">Trigger a one-off call — great for testing your assistant</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2], gap="large")
    with col1:
        st.markdown('<div class="card-glow">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Call Details</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            name  = st.text_input("Contact Name", placeholder="e.g. Rahul Verma")
        with c2:
            phone = st.text_input("Phone Number", placeholder="+919876543210")

        asst_id = assistant_selectbox("Voice Assistant", key="single_asst")

        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        call_btn = st.button("📞  Call Now")
        st.markdown('</div>', unsafe_allow_html=True)

        if call_btn:
            if not phone:
                st.warning("A phone number is required.")
            elif not alive:
                st.error("Backend offline.")
            else:
                data, err = api_post("/call/single", {
                    "name": name or "Test Contact",
                    "phone": phone,
                    "assistant_id": asst_id or None,
                })
                if err:
                    st.error(f"Call failed: {err}")
                else:
                    st.markdown(f"""
                    <div style="margin-top:16px;padding:16px 20px;background:rgba(62,207,142,0.06);border:1px solid rgba(62,207,142,0.2);border-radius:10px;">
                      <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:var(--green);margin-bottom:4px;">✓ Call triggered successfully</div>
                      <div style="font-family:'Space Mono',monospace;font-size:10px;color:var(--muted);">VAPI ID: {data.get('vapi_call_id','—')}</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Recent Solo Calls</div>', unsafe_allow_html=True)

        calls = api_get("/calls", [])
        solo  = [c for c in calls if not c.get("campaign_id")]

        if not solo:
            st.markdown("""
            <div class="empty-state" style="padding:30px 10px;">
              <div class="empty-icon">📵</div>
              <div class="empty-title">No calls yet</div>
              <div class="empty-desc">Trigger a call to see it here</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for c in reversed(solo[-8:]):
                color, icon, lbl = STATUS_META.get(c["status"], ("grey","?",c["status"]))
                st.markdown(f"""
                <div style="padding:12px 0;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;">
                  <div>
                    <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:600;color:var(--text);">{c['name']}</div>
                    <div style="font-family:'Space Mono',monospace;font-size:10px;color:var(--muted);margin-top:2px;">{c['phone']}</div>
                  </div>
                  <span class="badge badge-{color}">{icon} {lbl}</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ─── Dashboard ────────────────────────────────────────────────────────────────

elif st.session_state.tab == "Dashboard":

    st.markdown("""
    <div style="padding: 32px 0 24px 0;">
      <div class="page-title">Dashboard</div>
      <div class="page-sub">Monitor campaign progress and individual call statuses</div>
    </div>
    """, unsafe_allow_html=True)

    campaigns = api_get("/campaigns", [])

    if not campaigns:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">📊</div>
          <div class="empty-title">No campaigns yet</div>
          <div class="empty-desc">Launch a campaign to see live data here</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Campaign selector
        camp_ids    = [c["id"] for c in campaigns]
        camp_labels = [f"{c['name']}  ·  {c['id'][:8]}" for c in campaigns]
        default_idx = 0
        if st.session_state.active_campaign_id in camp_ids:
            default_idx = camp_ids.index(st.session_state.active_campaign_id)

        sel_label = st.selectbox("Select Campaign", camp_labels, index=default_idx, label_visibility="collapsed")
        sel_id    = camp_ids[camp_labels.index(sel_label)]
        campaign  = api_get(f"/campaign/{sel_id}", {})

        if not campaign:
            st.error("Could not load campaign data.")
        else:
            stats      = campaign.get("stats", {})
            is_running = campaign.get("status") in ("running", "starting")
            c_status   = campaign.get("status", "unknown")

            # Live pill
            if is_running:
                st.markdown("""
                <div style="margin-bottom:20px;">
                  <span class="live-pill"><span class="status-dot dot-green pulse"></span>LIVE · AUTO-REFRESHING</span>
                </div>
                """, unsafe_allow_html=True)

            # ── KPI Cards
            col_t, col_d, col_ok, col_fl, col_dl = st.columns(5)
            kpis = [
                (col_t,  "Total",       stats.get("total",0),       ""),
                (col_d,  "Dispatched",  stats.get("dispatched",0),  ""),
                (col_ok, "Completed",   stats.get("completed",0),   "green"),
                (col_fl, "Failed",      stats.get("failed",0),      "red"),
                (col_dl, "Live/Dialing",stats.get("dialing",0),     "blue"),
            ]
            for col, lbl, val, accent in kpis:
                col.metric(lbl, f"{val:,}")

            st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

            # ── Progress bar
            total = max(stats.get("total", 1), 1)
            done  = stats.get("completed", 0) + stats.get("failed", 0) + stats.get("no_answer", 0)
            pct   = done / total
            st.progress(pct, text=f"{done:,} / {total:,} calls finished  ·  {round(pct*100)}%")

            # ── Info row + status + abort
            col_info, col_act = st.columns([4, 1])
            with col_info:
                started = campaign.get("started_at", "")[:19] if campaign.get("started_at") else "—"
                ended   = campaign.get("ended_at", "")[:19] if campaign.get("ended_at") else "—"
                c_color, c_icon, c_lbl = STATUS_META.get(c_status, ("grey","?",c_status))
                st.markdown(f"""
                <div class="info-row">
                  <span>Status <strong>{c_icon} {c_lbl}</strong></span>
                  <span>Started <strong>{started}</strong></span>
                  <span>Ended <strong>{ended}</strong></span>
                  <span>Rate <strong>{api_get('/settings',{}).get('calls_per_minute',10)} calls/min</strong></span>
                </div>
                """, unsafe_allow_html=True)
            with col_act:
                if is_running:
                    st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
                    if st.button("⛔  Abort"):
                        api_post(f"/campaign/{sel_id}/abort")
                        st.warning("Abort signal sent.")
                    st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("---")

            # ── Call log tabs
            tab_all, tab_ok, tab_fail = st.tabs(["All Calls", "✓ Completed", "✗ Failed / No Answer"])
            calls = campaign.get("calls", [])

            def render_call_table(rows):
                if not rows:
                    st.markdown('<div class="empty-state" style="padding:30px;"><div class="empty-desc">No calls in this category</div></div>', unsafe_allow_html=True)
                    return
                df = pd.DataFrame(rows)
                cols = [c for c in ["name","phone","status","duration","error"] if c in df.columns]
                df   = df[cols].copy()
                df["status"]   = df["status"].map(lambda s: STATUS_META.get(s,("","?",s))[1] + " " + STATUS_META.get(s,("","?",s))[2])
                df["duration"] = df.get("duration", pd.Series()).apply(lambda d: f"{int(d)}s" if d else "—")
                if "error" in df.columns:
                    df["error"] = df["error"].fillna("—")
                df.columns = [c.capitalize() for c in df.columns]
                st.dataframe(df, use_container_width=True, height=380)

            with tab_all:
                render_call_table(calls)
                if calls:
                    csv = pd.DataFrame(calls).to_csv(index=False)
                    st.download_button("⬇ Export CSV", data=csv,
                        file_name=f"Volant_campaign_{sel_id[:8]}.csv", mime="text/csv")

            with tab_ok:
                render_call_table([c for c in calls if c.get("status") == "completed"])

            with tab_fail:
                render_call_table([c for c in calls if c.get("status") in ("failed","no-answer")])

            # Auto-refresh
            if is_running:
                time.sleep(3)
                st.rerun()


# ─── Assistants ───────────────────────────────────────────────────────────────

elif st.session_state.tab == "Assistants":

    st.markdown("""
    <div style="padding: 32px 0 24px 0;">
      <div class="page-title">Voice Assistants</div>
      <div class="page-sub">Manage all your VAPI bots — one per client, use case, or language</div>
    </div>
    """, unsafe_allow_html=True)

    assistants = api_get("/assistants", [])

    col_form, col_list = st.columns([2, 3], gap="large")

    with col_form:
        st.markdown('<div class="section-label">Add New Assistant</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-glow">', unsafe_allow_html=True)

        with st.form("add_assistant"):
            new_name   = st.text_input("Display Name", placeholder="e.g. Sales Bot EN")
            new_id     = st.text_input("VAPI Assistant ID", placeholder="asst_xxxxxxxxxxxx")
            new_desc   = st.text_input("Description", placeholder="e.g. English sales calls")
            add_btn    = st.form_submit_button("➕  Add Assistant")

            if add_btn:
                if not new_name or not new_id:
                    st.warning("Name and Assistant ID are required.")
                else:
                    data, err = api_post("/assistants", {
                        "name": new_name,
                        "assistant_id": new_id,
                        "description": new_desc,
                    })
                    if err:
                        st.error(f"Failed: {err}")
                    else:
                        st.success(f"✅ {new_name} added!")
                        st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
          <div class="section-label">Where to find your Assistant ID</div>
          <div style="font-family:'Instrument Sans',sans-serif;font-size:13px;color:var(--muted2);line-height:1.8;margin-top:8px;">
            1. Go to <a href="https://vapi.ai" target="_blank" style="color:var(--gold);text-decoration:none;">vapi.ai</a><br>
            2. Open <strong style="color:var(--text);">Assistants</strong><br>
            3. Click your bot<br>
            4. Copy the <strong style="color:var(--text);">Assistant ID</strong> at the top
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_list:
        st.markdown(f'<div class="section-label">{len(assistants)} assistant{"s" if len(assistants)!=1 else ""} configured</div>', unsafe_allow_html=True)

        if not assistants:
            st.markdown("""
            <div class="empty-state" style="padding:60px 20px;">
              <div class="empty-icon">🤖</div>
              <div class="empty-title">No assistants yet</div>
              <div class="empty-desc">Add your first voice bot using the form</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for a in assistants:
                col_a, col_b = st.columns([6, 1])
                with col_a:
                    st.markdown(f"""
                    <div class="assistant-card">
                      <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                        <span style="font-size:20px;">🤖</span>
                        <div>
                          <div class="assistant-name">{a['name']}</div>
                          <div class="assistant-desc">{a.get('description') or 'No description'}</div>
                        </div>
                      </div>
                      <div class="assistant-id">ID: {a['assistant_id']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_b:
                    st.markdown('<div style="padding-top:10px">', unsafe_allow_html=True)
                    if st.button("🗑", key=f"del_{a['id']}", help="Delete assistant"):
                        try:
                            requests.delete(f"{API}/assistants/{a['id']}", timeout=5)
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
                    st.markdown('</div>', unsafe_allow_html=True)


# ─── Settings ─────────────────────────────────────────────────────────────────

elif st.session_state.tab == "Settings":

    st.markdown("""
    <div style="padding: 32px 0 24px 0;">
      <div class="page-title">Settings</div>
      <div class="page-sub">Connect your VAPI and Twilio accounts</div>
    </div>
    """, unsafe_allow_html=True)

    current = api_get("/settings", {})

    col_main, col_guide = st.columns([3, 2], gap="large")

    with col_main:
        st.markdown('<div class="section-label">API Credentials</div>', unsafe_allow_html=True)

        with st.form("settings_form"):
            st.markdown('<div class="section-label" style="margin-top:0">VAPI</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                vapi_key  = st.text_input("API Key", value=current.get("vapi_api_key",""), type="password", placeholder="vapi_…")
            with c2:
                vapi_asst = st.text_input("Default Assistant ID", value=current.get("vapi_assistant_id",""), placeholder="asst_…")

            st.markdown('<div class="section-label">Twilio / Phone</div>', unsafe_allow_html=True)
            twilio_num = st.text_input(
                "VAPI Phone Number ID",
                value=current.get("twilio_phone_number",""),
                placeholder="Phone Number ID from VAPI dashboard",
                help="VAPI → Phone Numbers → copy the ID (not the +91 number)"
            )

            st.markdown('<div class="section-label">Rate Limiting</div>', unsafe_allow_html=True)
            cpm = st.slider("Calls per minute", 1, 60, int(current.get("calls_per_minute", 10)))

            st.markdown('<div class="btn-primary" style="margin-top:8px">', unsafe_allow_html=True)
            saved = st.form_submit_button("💾  Save Settings")
            st.markdown('</div>', unsafe_allow_html=True)

            if saved:
                data, err = api_post("/settings", {
                    "vapi_api_key": vapi_key,
                    "vapi_assistant_id": vapi_asst,
                    "twilio_phone_number": twilio_num,
                    "calls_per_minute": cpm,
                })
                if err:
                    st.error(f"Save failed: {err}")
                else:
                    st.success("✅ Settings saved!")

    with col_guide:
        st.markdown('<div class="section-label">Setup Guide</div>', unsafe_allow_html=True)

        with st.expander("🔑 Getting your VAPI API Key", expanded=True):
            st.markdown("""
            1. Go to **[vapi.ai](https://vapi.ai)** → sign in
            2. Click **API Keys** in the sidebar
            3. Generate or copy your key
            4. Paste it in the API Key field ←
            """)

        with st.expander("📞 Linking your Twilio number"):
            st.markdown("""
            1. In VAPI → **Phone Numbers**
            2. Import your Twilio number (or buy one)
            3. Copy the **Phone Number ID** (not `+91…`)
            4. Paste it in the field ←
            """)

        with st.expander("🔔 Webhook for live status"):
            st.markdown("""
            In VAPI → your Assistant → **Server URL**:
            ```
            https://your-domain.com/api/webhook/vapi
            ```
            For local dev use ngrok:
            ```
            ngrok http 4000
            ```
            """)


# ─── Footer ───────────────────────────────────────────────────────────────────

st.markdown("""
<div style="margin-top:40px;padding-top:20px;border-top:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;">
  <span style="font-family:'Syne',sans-serif;font-size:11px;font-weight:800;letter-spacing:0.1em;color:var(--muted);">आवाज़ · Volant</span>
  <span style="font-family:'Space Mono',monospace;font-size:10px;color:var(--muted);">VAPI + TWILIO + PYTHON</span>
  <a href="https://docs.vapi.ai" target="_blank" style="font-family:'Syne',sans-serif;font-size:11px;font-weight:600;color:var(--gold);text-decoration:none;letter-spacing:0.06em;">VAPI DOCS →</a>
</div>
""", unsafe_allow_html=True)
