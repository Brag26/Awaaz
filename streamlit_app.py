"""
Olivos AI — Voice Bot Platform
Minimal Luxury SaaS · Deep Olive · Matte Black · Soft Gold
"""

import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(
    page_title="Olivos AI",
    page_icon="🫒",
    layout="wide",
    initial_sidebar_state="expanded"
)

API = "http://127.0.0.1:4000/api"

# ══════════════════════════════════════════════════════════════════════════════
#  OLIVOS AI — BRAND CSS
#  Cormorant Garamond (luxury serif) + DM Mono + Jost (clean body)
#  Palette: Matte Black · Deep Olive · Soft Gold · Silver
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=DM+Mono:wght@300;400;500&family=Jost:wght@200;300;400;500;600&display=swap');

:root {
  /* Core palette */
  --black:    #0a0a08;
  --black2:   #0f0f0c;
  --black3:   #141410;
  --black4:   #1a1a15;
  --black5:   #212118;

  /* Olive family */
  --olive:    #4a5c2a;
  --olive2:   #5c7234;
  --olive3:   #6b8540;
  --olive4:   #3d4d22;
  --olive-glow: rgba(74,92,42,0.18);

  /* Gold / Silver accents */
  --gold:     #c9a84c;
  --gold2:    #e0c068;
  --gold-dim: rgba(201,168,76,0.12);
  --silver:   #9ea8a0;
  --silver2:  #c4cec6;
  --silver-dim: rgba(158,168,160,0.1);

  /* Text */
  --txt:      #e8e4dc;
  --txt2:     #a8a49c;
  --txt3:     #5c5c54;
  --txt4:     #38382e;

  /* Borders */
  --b0:  rgba(255,255,255,0.04);
  --b1:  rgba(255,255,255,0.07);
  --b2:  rgba(255,255,255,0.11);
  --b3:  rgba(255,255,255,0.18);
  --bo:  rgba(74,92,42,0.25);   /* olive border */
  --bg:  rgba(201,168,76,0.15); /* gold border */

  /* Status */
  --s-green:  #7aad5a;
  --s-amber:  #c9a84c;
  --s-red:    #b85c4a;
  --s-blue:   #5a8c9e;

  --r:   12px;
  --rs:  8px;
}

/* ── Reset & Base ── */
html, body, [class*="css"] {
  font-family: 'Jost', sans-serif !important;
  background: var(--black) !important;
  color: var(--txt) !important;
}

.stApp {
  background: var(--black) !important;
  background-image:
    radial-gradient(ellipse 100% 50% at 50% 0%, rgba(74,92,42,0.08) 0%, transparent 65%),
    radial-gradient(ellipse 50% 60% at 0% 100%, rgba(74,92,42,0.05) 0%, transparent 50%);
  min-height: 100vh;
}

/* Subtle noise texture overlay */
.stApp::after {
  content: '';
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 0;
  opacity: 0.4;
}

.block-container {
  padding: 0 3rem 5rem !important;
  max-width: 1440px !important;
  position: relative;
  z-index: 1;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--black2) !important;
  border-right: 1px solid var(--b1) !important;
}
[data-testid="stSidebar"]::after {
  content: '';
  position: absolute;
  top: 20%; right: 0;
  width: 1px; height: 60%;
  background: linear-gradient(180deg, transparent, var(--olive), transparent);
  opacity: 0.3;
}
section[data-testid="stSidebar"] .block-container { padding: 0 !important; }
#MainMenu, footer, header, [data-testid="stToolbar"], .stDeployButton {
  visibility: hidden; display: none;
}

/* ── Buttons ── */
.stButton > button {
  font-family: 'Jost', sans-serif !important;
  font-weight: 400 !important;
  font-size: 13px !important;
  letter-spacing: 0.08em !important;
  border-radius: var(--rs) !important;
  border: 1px solid var(--b2) !important;
  background: var(--b0) !important;
  color: var(--txt2) !important;
  transition: all 0.22s ease !important;
  padding: 10px 22px !important;
  width: 100% !important;
}
.stButton > button:hover {
  background: var(--b1) !important;
  border-color: var(--b3) !important;
  color: var(--txt) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 20px rgba(0,0,0,0.5) !important;
}

/* Primary olive button */
.btn-olive .stButton > button {
  background: linear-gradient(135deg, var(--olive), var(--olive4)) !important;
  border: 1px solid rgba(74,92,42,0.6) !important;
  color: #d8e4c8 !important;
  font-weight: 500 !important;
  box-shadow: 0 4px 20px rgba(74,92,42,0.25), inset 0 1px 0 rgba(255,255,255,0.08) !important;
}
.btn-olive .stButton > button:hover {
  background: linear-gradient(135deg, var(--olive2), var(--olive)) !important;
  box-shadow: 0 6px 30px rgba(74,92,42,0.4), inset 0 1px 0 rgba(255,255,255,0.1) !important;
  transform: translateY(-2px) !important;
}

/* Gold launch button */
.btn-gold .stButton > button {
  background: linear-gradient(135deg, var(--gold), #b8923a) !important;
  border: none !important;
  color: #1a1a0a !important;
  font-weight: 600 !important;
  font-size: 13px !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  box-shadow: 0 4px 24px rgba(201,168,76,0.3), inset 0 1px 0 rgba(255,255,255,0.2) !important;
}
.btn-gold .stButton > button:hover {
  background: linear-gradient(135deg, var(--gold2), var(--gold)) !important;
  box-shadow: 0 8px 36px rgba(201,168,76,0.45) !important;
  transform: translateY(-2px) !important;
}

/* Red abort */
.btn-red .stButton > button {
  background: rgba(184,92,74,0.08) !important;
  border: 1px solid rgba(184,92,74,0.3) !important;
  color: var(--s-red) !important;
}
.btn-red .stButton > button:hover {
  background: rgba(184,92,74,0.15) !important;
  box-shadow: 0 0 20px rgba(184,92,74,0.2) !important;
}

/* Nav */
.nav-btn .stButton > button {
  background: transparent !important;
  border: none !important;
  color: var(--txt3) !important;
  font-family: 'Jost', sans-serif !important;
  font-size: 13px !important;
  font-weight: 300 !important;
  padding: 12px 28px !important;
  border-radius: 0 !important;
  letter-spacing: 0.05em !important;
  text-align: left !important;
  justify-content: flex-start !important;
  transition: all 0.15s !important;
}
.nav-btn .stButton > button:hover {
  background: var(--b0) !important;
  color: var(--txt2) !important;
  transform: none !important;
  box-shadow: none !important;
}
.nav-active .stButton > button {
  background: linear-gradient(90deg, var(--olive-glow), transparent) !important;
  color: #a8c878 !important;
  border-left: 1px solid var(--olive2) !important;
  border-radius: 0 !important;
  font-weight: 500 !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
  background: var(--black3) !important;
  border: 1px solid var(--b1) !important;
  border-radius: var(--rs) !important;
  color: var(--txt) !important;
  font-family: 'DM Mono', monospace !important;
  font-size: 12px !important;
  padding: 11px 16px !important;
  transition: all 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
  border-color: rgba(74,92,42,0.6) !important;
  box-shadow: 0 0 0 3px rgba(74,92,42,0.1) !important;
  background: var(--black4) !important;
}
.stTextInput label, .stNumberInput label,
.stSelectbox label, .stSlider label, .stFileUploader label {
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 11px !important;
  font-weight: 500 !important;
  letter-spacing: 0.18em !important;
  text-transform: uppercase !important;
  color: var(--txt3) !important;
}

/* Selectbox */
.stSelectbox > div > div {
  background: var(--black3) !important;
  border: 1px solid var(--b1) !important;
  border-radius: var(--rs) !important;
  color: var(--txt) !important;
  font-family: 'DM Mono', monospace !important;
  font-size: 12px !important;
}

/* Slider */
.stSlider > div > div > div > div { background: var(--olive2) !important; }
.stSlider > div > div > div { background: var(--b1) !important; }

/* Progress */
.stProgress > div > div > div > div {
  background: linear-gradient(90deg, var(--olive2), var(--gold)) !important;
  border-radius: 99px !important;
}
.stProgress > div > div > div {
  background: var(--b1) !important;
  border-radius: 99px !important;
}

/* Metrics */
[data-testid="stMetric"] {
  background: var(--black2) !important;
  border: 1px solid var(--b1) !important;
  border-radius: var(--r) !important;
  padding: 22px 24px !important;
  position: relative;
  overflow: hidden;
  transition: all 0.3s !important;
}
[data-testid="stMetric"]::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, var(--olive2), transparent);
  opacity: 0.5;
}
[data-testid="stMetric"]:hover {
  border-color: var(--bo) !important;
  box-shadow: 0 0 30px rgba(74,92,42,0.08) !important;
}
[data-testid="stMetricLabel"] > div {
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 10px !important;
  font-weight: 500 !important;
  letter-spacing: 0.22em !important;
  text-transform: uppercase !important;
  color: var(--txt3) !important;
}
[data-testid="stMetricValue"] > div {
  font-family: 'DM Mono', monospace !important;
  font-size: 30px !important;
  font-weight: 400 !important;
  color: var(--txt) !important;
  line-height: 1.1 !important;
}

/* Dataframe */
.stDataFrame {
  border: 1px solid var(--b1) !important;
  border-radius: var(--r) !important;
  overflow: hidden !important;
  box-shadow: 0 8px 32px rgba(0,0,0,0.4) !important;
}

/* Form */
[data-testid="stForm"] {
  border: 1px solid var(--b1) !important;
  border-radius: var(--r) !important;
  background: var(--black2) !important;
  padding: 28px !important;
}

/* Expander */
.streamlit-expanderHeader {
  background: var(--black2) !important;
  border: 1px solid var(--b1) !important;
  border-radius: var(--rs) !important;
  font-family: 'Jost', sans-serif !important;
  font-size: 13px !important;
}
.streamlit-expanderContent {
  background: var(--black3) !important;
  border: 1px solid var(--b1) !important;
  border-top: none !important;
}

/* Download button */
.stDownloadButton > button {
  font-family: 'Jost', sans-serif !important;
  font-size: 12px !important;
  font-weight: 400 !important;
  background: transparent !important;
  border: 1px solid var(--b2) !important;
  color: var(--txt3) !important;
  border-radius: var(--rs) !important;
  padding: 8px 18px !important;
  letter-spacing: 0.06em !important;
}
.stDownloadButton > button:hover {
  border-color: var(--bo) !important;
  color: #a8c878 !important;
}

/* Divider */
hr {
  border: none !important;
  border-top: 1px solid var(--b1) !important;
  margin: 28px 0 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  background: transparent !important;
  gap: 0 !important;
  border-bottom: 1px solid var(--b1) !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--txt3) !important;
  border: none !important;
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 11px !important;
  font-weight: 500 !important;
  letter-spacing: 0.18em !important;
  padding: 12px 28px !important;
  border-bottom: 1px solid transparent !important;
  text-transform: uppercase !important;
}
.stTabs [aria-selected="true"] {
  color: #a8c878 !important;
  border-bottom: 1px solid var(--olive2) !important;
}

/* Code */
code {
  font-family: 'DM Mono', monospace !important;
  font-size: 11px !important;
  background: var(--olive-glow) !important;
  padding: 2px 8px !important;
  border-radius: 4px !important;
  color: #a8c878 !important;
  border: 1px solid var(--bo) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
  background: var(--black2) !important;
  border: 1px dashed var(--b2) !important;
  border-radius: var(--r) !important;
  transition: all 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
  border-color: var(--bo) !important;
  box-shadow: 0 0 24px rgba(74,92,42,0.08) !important;
}

/* ═══════════════════════════════════════
   OLIVOS COMPONENT SYSTEM
═══════════════════════════════════════ */

/* Logo */
.ov-logo {
  font-family: 'Cormorant Garamond', serif;
  font-size: 26px;
  font-weight: 600;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--txt);
  display: flex;
  align-items: baseline;
  gap: 8px;
}
.ov-logo-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--gold);
  display: inline-block;
  box-shadow: 0 0 8px var(--gold);
  margin-bottom: 3px;
}
.ov-ai-tag {
  font-family: 'DM Mono', monospace;
  font-size: 9px;
  font-weight: 400;
  letter-spacing: 0.2em;
  color: var(--olive2);
  text-transform: uppercase;
  padding: 2px 8px;
  border: 1px solid var(--bo);
  border-radius: 3px;
  background: var(--olive-glow);
}

/* Page header */
.ov-header {
  padding: 40px 0 32px;
  border-bottom: 1px solid var(--b1);
  margin-bottom: 36px;
}
.ov-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 38px;
  font-weight: 300;
  letter-spacing: 0.06em;
  color: var(--txt);
  line-height: 1;
  font-style: italic;
}
.ov-title strong {
  font-weight: 600;
  font-style: normal;
  color: var(--txt);
}
.ov-sub {
  font-family: 'Jost', sans-serif;
  font-size: 13px;
  font-weight: 300;
  color: var(--txt3);
  margin-top: 10px;
  letter-spacing: 0.06em;
}

/* Section label */
.ov-sec {
  font-family: 'Cormorant Garamond', serif;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: var(--txt3);
  margin-bottom: 14px;
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 14px;
}
.ov-sec::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--b1);
}

/* Cards */
.ov-card {
  background: var(--black2);
  border: 1px solid var(--b1);
  border-radius: var(--r);
  padding: 26px;
  position: relative;
  overflow: hidden;
}
.ov-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, var(--b2), transparent);
}

.ov-card-olive {
  background: linear-gradient(135deg, rgba(74,92,42,0.06), var(--black2));
  border: 1px solid var(--bo);
  border-radius: var(--r);
  padding: 26px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 0 40px rgba(74,92,42,0.06), inset 0 1px 0 rgba(74,92,42,0.12);
}
.ov-card-olive::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, var(--olive2), transparent);
  opacity: 0.5;
}
.ov-card-olive::after {
  content: '';
  position: absolute;
  bottom: -40px; right: -40px;
  width: 120px; height: 120px;
  background: radial-gradient(circle, rgba(74,92,42,0.12), transparent);
  pointer-events: none;
}

/* Status badges */
.ov-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: 'DM Mono', monospace;
  font-size: 9px;
  padding: 4px 12px;
  border-radius: 3px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.ob-green  { background: rgba(122,173,90,0.1);  color: var(--s-green); border: 1px solid rgba(122,173,90,0.2); }
.ob-amber  { background: rgba(201,168,76,0.1);  color: var(--s-amber); border: 1px solid rgba(201,168,76,0.2); }
.ob-red    { background: rgba(184,92,74,0.1);   color: var(--s-red);   border: 1px solid rgba(184,92,74,0.2); }
.ob-blue   { background: rgba(90,140,158,0.1);  color: var(--s-blue);  border: 1px solid rgba(90,140,158,0.2); }
.ob-grey   { background: rgba(58,58,48,0.3);    color: var(--txt3);    border: 1px solid var(--b1); }
.ob-olive  { background: var(--olive-glow);     color: #a8c878;        border: 1px solid var(--bo); }

/* Dot */
.ov-dot {
  display: inline-block;
  width: 6px; height: 6px;
  border-radius: 50%;
  margin-right: 8px;
  vertical-align: middle;
}
.od-green { background: var(--s-green); box-shadow: 0 0 6px var(--s-green); }
.od-red   { background: var(--s-red);   box-shadow: 0 0 6px var(--s-red); }
.od-olive { background: var(--olive2);  box-shadow: 0 0 6px var(--olive2); }
.od-amber { background: var(--s-amber); box-shadow: 0 0 6px var(--s-amber); }
.od-grey  { background: var(--txt4); }

/* Pulse */
.ov-pulse { animation: ovpulse 2.5s ease-in-out infinite; }
@keyframes ovpulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.3;transform:scale(.75)} }

/* Live indicator */
.ov-live {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: rgba(122,173,90,0.06);
  border: 1px solid rgba(122,173,90,0.18);
  border-radius: 3px;
  padding: 7px 18px;
  font-family: 'Cormorant Garamond', serif;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: 0.25em;
  color: var(--s-green);
  text-transform: uppercase;
}

/* Waveform — subtle olive */
.ov-wave {
  display: flex;
  align-items: center;
  gap: 3px;
  height: 18px;
}
.ov-wave span {
  display: inline-block;
  width: 2px;
  border-radius: 2px;
  background: var(--olive2);
  animation: ovwave 2s ease-in-out infinite;
}
.ov-wave span:nth-child(1){height:3px;animation-delay:0s}
.ov-wave span:nth-child(2){height:10px;animation-delay:.15s}
.ov-wave span:nth-child(3){height:16px;animation-delay:.3s}
.ov-wave span:nth-child(4){height:12px;animation-delay:.45s}
.ov-wave span:nth-child(5){height:5px;animation-delay:.6s}
.ov-wave span:nth-child(6){height:14px;animation-delay:.75s}
.ov-wave span:nth-child(7){height:8px;animation-delay:.9s}
@keyframes ovwave {
  0%,100%{transform:scaleY(.25);opacity:.3}
  50%{transform:scaleY(1);opacity:.8}
}

/* Info row */
.ov-info {
  display: flex;
  gap: 28px;
  font-family: 'Jost', sans-serif;
  font-size: 12px;
  color: var(--txt3);
  margin: 16px 0;
  flex-wrap: wrap;
  align-items: center;
}
.ov-info strong { color: var(--txt2); font-weight: 500; }

/* Stat block */
.ov-stat-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 0;
}
.ov-stat-block {
  padding: 14px 18px;
  text-align: center;
  border-right: 1px solid var(--b1);
}
.ov-stat-block:last-child { border-right: none; }
.ov-stat-label {
  font-family: 'Cormorant Garamond', serif;
  font-size: 9px;
  font-weight: 500;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--txt3);
  margin-bottom: 6px;
}
.ov-stat-value {
  font-family: 'DM Mono', monospace;
  font-size: 22px;
  font-weight: 400;
  color: var(--txt);
}
.ov-stat-gold { color: var(--gold) !important; }

/* Assistant card */
.ov-assist {
  background: var(--black3);
  border: 1px solid var(--b1);
  border-radius: var(--rs);
  padding: 18px 22px;
  margin-bottom: 10px;
  transition: all 0.25s;
  position: relative;
}
.ov-assist::after {
  content: '';
  position: absolute;
  left: 0; top: 20%; bottom: 20%;
  width: 1px;
  background: linear-gradient(180deg, transparent, var(--olive2), transparent);
  opacity: 0;
  transition: opacity 0.25s;
}
.ov-assist:hover {
  border-color: var(--bo);
  background: var(--black4);
}
.ov-assist:hover::after { opacity: 1; }

/* Empty state */
.ov-empty {
  text-align: center;
  padding: 60px 20px;
}
.ov-empty-icon {
  font-size: 40px;
  opacity: 0.2;
  margin-bottom: 18px;
  filter: grayscale(1);
}
.ov-empty-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 16px;
  font-weight: 400;
  letter-spacing: 0.12em;
  color: var(--txt3);
  text-transform: uppercase;
  margin-bottom: 8px;
  font-style: italic;
}
.ov-empty-desc {
  font-size: 12px;
  color: var(--txt4);
  font-family: 'Jost', sans-serif;
  font-weight: 300;
  letter-spacing: 0.04em;
}

/* Success box */
.ov-success {
  margin-top: 16px;
  padding: 16px 20px;
  background: rgba(122,173,90,0.05);
  border: 1px solid rgba(122,173,90,0.18);
  border-radius: var(--rs);
  border-left: 2px solid var(--s-green);
}

/* Divider with label */
.ov-divider {
  display: flex;
  align-items: center;
  gap: 16px;
  margin: 24px 0;
  color: var(--txt3);
  font-family: 'Cormorant Garamond', serif;
  font-size: 10px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
}
.ov-divider::before, .ov-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--b1);
}

/* Tips list */
.ov-tip {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid var(--b0);
  font-family: 'Jost', sans-serif;
  font-size: 12px;
  color: var(--txt3);
  font-weight: 300;
}
.ov-tip-icon {
  width: 22px; height: 22px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  flex-shrink: 0;
  margin-top: 1px;
}

</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  STATE & API HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def init():
    for k,v in {"tab":"Campaign","contacts":None,"active_campaign_id":None}.items():
        if k not in st.session_state: st.session_state[k] = v
init()

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
    except Exception as e: return None, str(e)

def DELETE(path):
    try: requests.delete(f"{API}{path}", timeout=6)
    except: pass

def alive():
    try: requests.get(f"{API.replace('/api','')}/health", timeout=2); return True
    except: return False

def asst_opts():
    s = GET("/settings") or {}
    a = GET("/assistants") or []
    did = s.get("vapi_assistant_id","")
    short = did[:14]+"…" if len(did)>14 else did
    opts = [("Default" + (f"  ·  {short}" if did else "  ·  not configured"), did)]
    for x in a:
        lbl = f"{x['name']}"
        if x.get("description"): lbl += f"  —  {x['description']}"
        opts.append((lbl, x["assistant_id"]))
    return opts

def asst_select(label, key):
    opts = asst_opts(); labels = [o[0] for o in opts]
    idx = st.selectbox(label, range(len(labels)), format_func=lambda i: labels[i], key=key)
    return opts[idx][1]

SM = {
    "pending":     ("ob-grey",  "○", "Pending"),
    "queued":      ("ob-amber", "◔", "Queued"),
    "dialing":     ("ob-blue",  "◑", "Dialing"),
    "in-progress": ("ob-olive", "●", "Live"),
    "completed":   ("ob-green", "✓", "Completed"),
    "failed":      ("ob-red",   "✗", "Failed"),
    "no-answer":   ("ob-amber", "⊘", "No Answer"),
    "starting":    ("ob-amber", "◔", "Starting"),
    "running":     ("ob-olive", "●", "Running"),
    "aborted":     ("ob-red",   "✗", "Aborted"),
}

def ph(title_light, title_bold, sub):
    st.markdown(f"""
    <div class="ov-header">
      <div class="ov-title">{title_light} <strong>{title_bold}</strong></div>
      <div class="ov-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

backend_live = alive()

with st.sidebar:
    # Logo
    st.markdown(f"""
    <div style="padding:32px 28px 26px;border-bottom:1px solid var(--b1);">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:18px;">
        <div style="width:8px;height:8px;border-radius:50%;background:var(--gold);box-shadow:0 0 12px var(--gold);flex-shrink:0;margin-top:1px;"></div>
        <div style="font-family:'Cormorant Garamond',serif;font-size:22px;font-weight:600;letter-spacing:0.22em;text-transform:uppercase;color:var(--txt);">Olivos</div>
        <div style="font-family:'DM Mono',monospace;font-size:8px;letter-spacing:0.18em;color:var(--olive2);border:1px solid var(--bo);padding:2px 7px;border-radius:3px;background:var(--olive-glow);">AI</div>
      </div>
      <div style="font-family:'Jost',sans-serif;font-size:10px;font-weight:300;color:var(--txt3);letter-spacing:0.12em;text-transform:uppercase;">Voice Bot Platform</div>

      <div style="margin-top:18px;display:flex;align-items:center;gap:10px;padding:10px 14px;background:var(--black3);border-radius:6px;border:1px solid var(--b1);">
        <span class="ov-dot {'od-green ov-pulse' if backend_live else 'od-red'}"></span>
        <span style="font-family:'DM Mono',monospace;font-size:9px;letter-spacing:0.12em;color:{'var(--s-green)' if backend_live else 'var(--s-red)'};">{'ONLINE' if backend_live else 'OFFLINE'}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not backend_live:
        st.markdown("""
        <div style="padding:14px 28px;">
          <div style="font-family:'DM Mono',monospace;font-size:9px;color:var(--txt3);background:var(--black3);padding:12px 14px;border-radius:6px;border:1px solid var(--b1);line-height:2;letter-spacing:0.04em;">
            python -m uvicorn backend:app<br>--port 4000 --host 0.0.0.0
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Navigation
    st.markdown('<div style="padding:20px 0 16px;">', unsafe_allow_html=True)
    nav = [
        ("Campaign",    "Campaign",    "Bulk outbound"),
        ("Single Call", "Single Call", "One-off call"),
        ("Dashboard",   "Dashboard",   "Live monitoring"),
        ("Assistants",  "Assistants",  "Voice bots"),
        ("Settings",    "Settings",    "Configuration"),
    ]
    for tab, label, desc in nav:
        active = st.session_state.tab == tab
        cls = "nav-active nav-btn" if active else "nav-btn"
        st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
        if st.button(label, key=f"n_{tab}", use_container_width=True):
            st.session_state.tab = tab; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar footer
    st.markdown("""
    <div style="position:fixed;bottom:0;left:0;width:inherit;padding:18px 28px;border-top:1px solid var(--b1);background:var(--black2);">
      <div style="display:flex;align-items:center;justify-content:space-between;">
        <div class="ov-wave">
          <span></span><span></span><span></span><span></span>
          <span></span><span></span><span></span>
        </div>
        <div style="font-family:'DM Mono',monospace;font-size:8px;color:var(--txt4);letter-spacing:0.14em;">VAPI · TWILIO</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  CAMPAIGN
# ══════════════════════════════════════════════════════════════════════════════

if st.session_state.tab == "Campaign":
    ph("Bulk", "Campaign", "Upload a contact list · select a voice assistant · launch at scale")

    col_l, col_r = st.columns([3,2], gap="large")

    with col_l:
        st.markdown('<div class="ov-sec">Contact List</div>', unsafe_allow_html=True)
        st.markdown('<div class="ov-card">', unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Upload file", type=["csv","xlsx","xls"],
            label_visibility="collapsed"
        )
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
                st.markdown(f"""
                <div style="margin-top:16px;padding:14px 18px;background:rgba(122,173,90,0.05);border:1px solid rgba(122,173,90,0.15);border-radius:8px;border-left:2px solid var(--s-green);">
                  <div style="font-family:'Jost',sans-serif;font-size:14px;font-weight:500;color:var(--s-green);">{len(df):,} contacts ready</div>
                  <div style="font-family:'DM Mono',monospace;font-size:10px;color:var(--txt3);margin-top:3px;">{uploaded.name}</div>
                </div>""", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Parse error: {e}")

        st.markdown("""
        <div style="margin-top:16px;display:flex;align-items:center;gap:16px;">
          <span style="font-family:'DM Mono',monospace;font-size:9px;color:var(--txt4);letter-spacing:0.1em;">CSV · XLSX · XLS</span>
          <span style="color:var(--b2);">·</span>
          <span style="font-family:'DM Mono',monospace;font-size:9px;color:var(--txt4);letter-spacing:0.1em;">COLUMNS: name, phone</span>
        </div>""", unsafe_allow_html=True)

        st.download_button(
            "↓  Download Sample CSV",
            data="name,phone\nAlex Kumar,+919876543210\nPriya Sharma,+919123456789",
            file_name="olivos_sample.csv", mime="text/csv"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.contacts is not None:
            st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
            st.markdown('<div class="ov-sec">Preview</div>', unsafe_allow_html=True)
            p = st.session_state.contacts.head(12).copy(); p.index += 1
            st.dataframe(p, use_container_width=True, height=280)
            if len(st.session_state.contacts) > 12:
                st.markdown(f'<div style="font-family:DM Mono,monospace;font-size:9px;color:var(--txt4);margin-top:6px;letter-spacing:0.08em;">+ {len(st.session_state.contacts)-12:,} more contacts</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="ov-sec">Campaign Settings</div>', unsafe_allow_html=True)
        st.markdown('<div class="ov-card-olive">', unsafe_allow_html=True)

        cname    = st.text_input("Campaign Name", placeholder="e.g. Q2 Outreach")
        sel_asst = asst_select("Voice Assistant", "camp_asst")

        settings = GET("/settings") or {}
        cpm = settings.get("calls_per_minute", 10)

        if st.session_state.contacts is not None:
            n = len(st.session_state.contacts)
            est = round(n/max(cpm,1),1)
            st.markdown(f"""
            <div style="margin:18px 0;padding:18px;background:var(--black3);border-radius:8px;border:1px solid var(--b1);">
              <div class="ov-stat-grid">
                <div class="ov-stat-block">
                  <div class="ov-stat-label">Contacts</div>
                  <div class="ov-stat-value">{n:,}</div>
                </div>
                <div class="ov-stat-block">
                  <div class="ov-stat-label">Rate</div>
                  <div class="ov-stat-value">{cpm}<span style="font-size:12px;color:var(--txt3);">/m</span></div>
                </div>
                <div class="ov-stat-block">
                  <div class="ov-stat-label">Est. Time</div>
                  <div class="ov-stat-value ov-stat-gold">~{est}<span style="font-size:12px;color:var(--txt3);">m</span></div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div style="height:6px"></div><div class="btn-gold">', unsafe_allow_html=True)
        launch = st.button("Launch Campaign", disabled=(st.session_state.contacts is None or not cname))
        st.markdown('</div>', unsafe_allow_html=True)

        if launch:
            if not backend_live: st.error("Backend offline.")
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

        st.markdown("""
        <div style="height:18px"></div>
        <div class="ov-card">
          <div class="ov-sec">Reference</div>
          <div class="ov-tip">
            <div class="ov-tip-icon" style="background:rgba(74,92,42,0.12);">📱</div>
            <span>Phone numbers must be E.164 format — <code>+91XXXXXXXXXX</code></span>
          </div>
          <div class="ov-tip">
            <div class="ov-tip-icon" style="background:rgba(201,168,76,0.1);">⚡</div>
            <span>Maximum 60 calls per minute on VAPI plans</span>
          </div>
          <div class="ov-tip" style="border:none;">
            <div class="ov-tip-icon" style="background:rgba(90,140,158,0.1);">🔔</div>
            <span>Configure webhook for real-time call status updates</span>
          </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SINGLE CALL
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.tab == "Single Call":
    ph("Single", "Call", "Trigger a one-off outbound call · perfect for testing your assistant")

    c1, c2 = st.columns([3,2], gap="large")
    with c1:
        st.markdown('<div class="ov-card-olive">', unsafe_allow_html=True)
        st.markdown('<div class="ov-sec">Call Details</div>', unsafe_allow_html=True)
        r1, r2 = st.columns(2)
        with r1: name  = st.text_input("Contact Name", placeholder="e.g. Rahul Verma")
        with r2: phone = st.text_input("Phone Number",  placeholder="+919876543210")
        asst_id = asst_select("Voice Assistant", "single_asst")
        st.markdown('<div style="height:10px"></div><div class="btn-gold">', unsafe_allow_html=True)
        call_btn = st.button("Initiate Call")
        st.markdown('</div>', unsafe_allow_html=True)
        if call_btn:
            if not phone: st.warning("Phone number is required.")
            elif not backend_live: st.error("Backend offline.")
            else:
                data, err = POST("/call/single", {"name":name or "Test","phone":phone,"assistant_id":asst_id or None})
                if err: st.error(err)
                else:
                    st.markdown(f"""
                    <div class="ov-success">
                      <div style="font-family:'Jost',sans-serif;font-size:13px;font-weight:500;color:var(--s-green);">Call initiated</div>
                      <div style="font-family:'DM Mono',monospace;font-size:10px;color:var(--txt3);margin-top:4px;">VAPI ID: {data.get('vapi_call_id','—')}</div>
                    </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="ov-card"><div class="ov-sec">Recent Calls</div>', unsafe_allow_html=True)
        calls = GET("/calls") or []
        if not calls:
            st.markdown('<div class="ov-empty" style="padding:28px 10px;"><div class="ov-empty-icon">📵</div><div class="ov-empty-title">No calls yet</div><div class="ov-empty-desc">History will appear here</div></div>', unsafe_allow_html=True)
        else:
            for c in reversed(calls[-8:]):
                cls,ic,lbl = SM.get(c["status"],("ob-grey","?",c["status"]))
                st.markdown(f"""
                <div style="padding:12px 0;border-bottom:1px solid var(--b0);display:flex;justify-content:space-between;align-items:center;">
                  <div>
                    <div style="font-family:'Jost',sans-serif;font-size:13px;font-weight:400;color:var(--txt);">{c['name']}</div>
                    <div style="font-family:'DM Mono',monospace;font-size:10px;color:var(--txt3);margin-top:2px;">{c['phone']}</div>
                  </div>
                  <span class="ov-badge {cls}">{ic} {lbl}</span>
                </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.tab == "Dashboard":
    ph("Live", "Dashboard", "Real-time campaign monitoring · call tracking · export logs")

    campaigns = GET("/campaigns") or []
    if not campaigns:
        st.markdown('<div class="ov-empty"><div class="ov-empty-icon">◈</div><div class="ov-empty-title">No Campaigns</div><div class="ov-empty-desc">Launch a campaign to see live data</div></div>', unsafe_allow_html=True)
    else:
        ids    = [c["id"] for c in campaigns]
        labels = [f"{c['name']}  ·  {c['id'][:8]}" for c in campaigns]
        def_idx = 0
        if st.session_state.active_campaign_id in ids:
            def_idx = ids.index(st.session_state.active_campaign_id)

        sel    = st.selectbox("Select Campaign", labels, index=def_idx, label_visibility="collapsed")
        sel_id = ids[labels.index(sel)]
        camp   = GET(f"/campaign/{sel_id}")
        if not camp: st.error("Could not load campaign."); st.stop()

        stats   = camp.get("stats",{})
        running = camp.get("status") in ("running","starting")

        if running:
            st.markdown('<div style="margin-bottom:20px;"><span class="ov-live"><span class="ov-dot od-green ov-pulse"></span>Live — Refreshing every 3 seconds</span></div>', unsafe_allow_html=True)

        # KPI row
        c1,c2,c3,c4,c5 = st.columns(5)
        c1.metric("Total",       f"{stats.get('total',0):,}")
        c2.metric("Dispatched",  f"{stats.get('dispatched',0):,}")
        c3.metric("Completed",   f"{stats.get('completed',0):,}")
        c4.metric("Failed",      f"{stats.get('failed',0):,}")
        c5.metric("Live",        f"{stats.get('dialing',0):,}")

        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)

        total = max(stats.get("total",1),1)
        done  = stats.get("completed",0)+stats.get("failed",0)+stats.get("no_answer",0)
        pct   = done/total
        st.progress(pct, text=f"{done:,} of {total:,} completed  ·  {round(pct*100)}%")

        ci, ca = st.columns([5,1])
        with ci:
            s = camp.get("status","")
            cls,ic,lbl = SM.get(s,("ob-grey","?",s))
            started = (camp.get("started_at") or "—")[:19]
            ended   = (camp.get("ended_at") or "—")[:19]
            st.markdown(f"""
            <div class="ov-info">
              <span>Status <strong><span class="ov-badge {cls}">{ic} {lbl}</span></strong></span>
              <span>Started <strong>{started}</strong></span>
              <span>Ended <strong>{ended}</strong></span>
              <span>Rate <strong>{GET('/settings',{}).get('calls_per_minute',10)}/min</strong></span>
            </div>""", unsafe_allow_html=True)
        with ca:
            if running:
                st.markdown('<div class="btn-red">', unsafe_allow_html=True)
                if st.button("Abort"):
                    POST(f"/campaign/{sel_id}/abort"); st.warning("Abort signal sent.")
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        calls = camp.get("calls",[])
        t_all, t_ok, t_fail = st.tabs(["All Calls", "Completed", "Failed / No Answer"])

        def call_table(rows):
            if not rows:
                st.markdown('<div class="ov-empty" style="padding:30px;"><div class="ov-empty-desc">No calls in this category</div></div>', unsafe_allow_html=True); return
            df = pd.DataFrame(rows)
            cols = [c for c in ["name","phone","status","duration","error"] if c in df.columns]
            df = df[cols].copy()
            df["status"] = df["status"].map(lambda s: SM.get(s,("","?",s))[1]+" "+SM.get(s,("","?",s))[2])
            if "duration" in df.columns: df["duration"] = df["duration"].apply(lambda d: f"{int(d)}s" if d else "—")
            if "error" in df.columns: df["error"] = df["error"].fillna("—")
            df.columns = [c.capitalize() for c in df.columns]
            st.dataframe(df, use_container_width=True, height=380)

        with t_all:
            call_table(calls)
            if calls:
                st.download_button("↓  Export CSV", pd.DataFrame(calls).to_csv(index=False),
                                   file_name=f"olivos_{sel_id[:8]}.csv", mime="text/csv")
        with t_ok:   call_table([c for c in calls if c.get("status")=="completed"])
        with t_fail: call_table([c for c in calls if c.get("status") in ("failed","no-answer")])

        if running: time.sleep(3); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  ASSISTANTS
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.tab == "Assistants":
    ph("Voice", "Assistants", "Manage your VAPI voice bots · one per client or use case")

    assistants = GET("/assistants") or []
    col_f, col_l = st.columns([2,3], gap="large")

    with col_f:
        st.markdown('<div class="ov-sec">Add Assistant</div>', unsafe_allow_html=True)
        st.markdown('<div class="ov-card-olive">', unsafe_allow_html=True)
        with st.form("add_asst"):
            aname = st.text_input("Display Name", placeholder="e.g. Sales Bot")
            aid   = st.text_input("VAPI Assistant ID", placeholder="asst_…")
            adesc = st.text_input("Description", placeholder="e.g. English outbound")
            st.markdown('<div class="btn-olive">', unsafe_allow_html=True)
            ok = st.form_submit_button("Add Assistant")
            st.markdown('</div>', unsafe_allow_html=True)
            if ok:
                if not aname or not aid: st.warning("Name and ID are required.")
                else:
                    data, err = POST("/assistants", {"name":aname,"assistant_id":aid,"description":adesc})
                    if err: st.error(err)
                    else: st.success(f"{aname} added."); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="height:18px"></div>
        <div class="ov-card">
          <div class="ov-sec">Finding your Assistant ID</div>
          <div style="font-family:'Jost',sans-serif;font-size:12px;color:var(--txt3);line-height:2.2;font-weight:300;">
            <div>1 &nbsp;·&nbsp; Go to <a href="https://vapi.ai" target="_blank" style="color:#a8c878;text-decoration:none;">vapi.ai</a></div>
            <div>2 &nbsp;·&nbsp; Open <strong style="color:var(--txt2);">Assistants</strong></div>
            <div>3 &nbsp;·&nbsp; Click your assistant</div>
            <div>4 &nbsp;·&nbsp; Copy the <strong style="color:var(--txt2);">Assistant ID</strong></div>
          </div>
        </div>""", unsafe_allow_html=True)

    with col_l:
        st.markdown(f'<div class="ov-sec">{len(assistants)} assistant{"s" if len(assistants)!=1 else ""}</div>', unsafe_allow_html=True)
        if not assistants:
            st.markdown('<div class="ov-empty" style="padding:60px 20px;"><div class="ov-empty-icon">🤖</div><div class="ov-empty-title">No Assistants</div><div class="ov-empty-desc">Add your first voice bot using the form</div></div>', unsafe_allow_html=True)
        else:
            for a in assistants:
                ca, cb = st.columns([7,1])
                with ca:
                    st.markdown(f"""
                    <div class="ov-assist">
                      <div style="display:flex;align-items:center;gap:14px;margin-bottom:10px;">
                        <div style="width:40px;height:40px;border-radius:8px;background:linear-gradient(135deg,rgba(74,92,42,0.2),rgba(74,92,42,0.05));border:1px solid var(--bo);display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;">🤖</div>
                        <div>
                          <div style="font-family:'Jost',sans-serif;font-size:14px;font-weight:500;color:var(--txt);">{a['name']}</div>
                          <div style="font-family:'Jost',sans-serif;font-size:12px;color:var(--txt3);font-weight:300;margin-top:1px;">{a.get('description') or 'No description'}</div>
                        </div>
                      </div>
                      <div style="font-family:'DM Mono',monospace;font-size:10px;color:var(--txt3);padding:7px 12px;background:var(--black3);border-radius:5px;border:1px solid var(--b1);letter-spacing:0.04em;">{a['assistant_id']}</div>
                    </div>""", unsafe_allow_html=True)
                with cb:
                    st.markdown('<div style="padding-top:12px;">', unsafe_allow_html=True)
                    if st.button("✕", key=f"da_{a['id']}", help="Remove"):
                        DELETE(f"/assistants/{a['id']}"); st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SETTINGS
# ══════════════════════════════════════════════════════════════════════════════

elif st.session_state.tab == "Settings":
    ph("Platform", "Settings", "Connect your VAPI and Twilio accounts · configure rate controls")

    current = GET("/settings") or {}
    col_m, col_g = st.columns([3,2], gap="large")

    with col_m:
        st.markdown('<div class="ov-sec">API Credentials</div>', unsafe_allow_html=True)
        with st.form("settings_form"):
            st.markdown('<div class="ov-sec" style="margin-top:4px;">VAPI</div>', unsafe_allow_html=True)
            g1,g2 = st.columns(2)
            with g1: vapi_key  = st.text_input("API Key", value=current.get("vapi_api_key",""), type="password", placeholder="vapi_…")
            with g2: vapi_asst = st.text_input("Default Assistant ID", value=current.get("vapi_assistant_id",""), placeholder="asst_…")
            st.markdown('<div class="ov-sec">Phone Number</div>', unsafe_allow_html=True)
            twilio = st.text_input("VAPI Phone Number ID",
                                   value=current.get("twilio_phone_number",""),
                                   placeholder="Phone Number ID from your VAPI dashboard")
            st.markdown('<div class="ov-sec">Rate Control</div>', unsafe_allow_html=True)
            cpm = st.slider("Calls per minute", 1, 60, int(current.get("calls_per_minute",10)))
            st.markdown('<div class="btn-olive" style="margin-top:14px;">', unsafe_allow_html=True)
            saved = st.form_submit_button("Save Configuration")
            st.markdown('</div>', unsafe_allow_html=True)
            if saved:
                _, err = POST("/settings", {"vapi_api_key":vapi_key,"vapi_assistant_id":vapi_asst,
                                            "twilio_phone_number":twilio,"calls_per_minute":cpm})
                if err: st.error(err)
                else: st.success("Configuration saved.")

    with col_g:
        st.markdown('<div class="ov-sec">Setup Guide</div>', unsafe_allow_html=True)
        with st.expander("VAPI API Key", expanded=True):
            st.markdown("1. Go to **[vapi.ai](https://vapi.ai)**\n2. Navigate to **API Keys**\n3. Copy your key and paste above")
        with st.expander("Twilio Phone Number ID"):
            st.markdown("1. VAPI → **Phone Numbers**\n2. Import your Twilio number\n3. Copy the **ID** — not the `+91…` number itself")
        with st.expander("Webhook — Live Call Status"):
            st.markdown("Set this URL in VAPI → Assistant → **Server URL**:\n```\nhttps://your-domain.com/api/webhook/vapi\n```")
        with st.expander("Production Deployment"):
            st.markdown("**Backend** → Railway or Render\n\n**Frontend** → Streamlit Cloud (free)\n\nUpdate the `API` variable in `streamlit_app.py` with your Railway backend URL.")

# ══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div style="margin-top:56px;padding-top:22px;border-top:1px solid var(--b1);display:flex;justify-content:space-between;align-items:center;">
  <div style="display:flex;align-items:center;gap:10px;">
    <div style="width:6px;height:6px;border-radius:50%;background:var(--gold);box-shadow:0 0 8px var(--gold);"></div>
    <span style="font-family:'Cormorant Garamond',serif;font-size:13px;font-weight:500;letter-spacing:0.22em;text-transform:uppercase;color:var(--txt3);">Olivos AI</span>
  </div>
  <span style="font-family:'DM Mono',monospace;font-size:9px;color:var(--txt4);letter-spacing:0.12em;">VAPI · TWILIO · PYTHON</span>
  <a href="https://docs.vapi.ai" target="_blank" style="font-family:'DM Mono',monospace;font-size:9px;color:var(--olive2);text-decoration:none;letter-spacing:0.1em;">VAPI DOCS →</a>
</div>
""", unsafe_allow_html=True)
