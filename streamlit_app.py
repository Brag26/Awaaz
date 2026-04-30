"""
VoiceBot Platform — Streamlit Frontend
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import requests
import time
import io
from datetime import datetime

# ─── Config ───────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="VoiceBot Platform",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded",
)

API = "http://localhost:4000/api"

# ─── Styling ──────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Dark base */
.stApp {
    background: #0d0f14;
    color: #e2ddd6;
}

.block-container {
    padding-top: 2rem;
    max-width: 1400px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #111318 !important;
    border-right: 1px solid rgba(255,255,255,0.07);
}
[data-testid="stSidebar"] .stMarkdown p {
    color: #9ca3af;
    font-size: 12px;
    letter-spacing: 0.05em;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 16px 20px;
}
[data-testid="stMetricLabel"] {
    font-size: 11px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #6b7280 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 28px !important;
    color: #f0ede8 !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'DM Mono', monospace !important;
}

/* Buttons */
.stButton > button {
    background: #e8c547;
    color: #0d0f14;
    border: none;
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 14px;
    padding: 10px 22px;
    transition: all 0.2s;
    width: 100%;
}
.stButton > button:hover {
    background: #f0d060;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(232,197,71,0.3);
}

/* Danger button override */
.danger-btn button {
    background: rgba(239,68,68,0.15) !important;
    color: #ef4444 !important;
    border: 1px solid rgba(239,68,68,0.3) !important;
}
.danger-btn button:hover {
    background: rgba(239,68,68,0.25) !important;
    box-shadow: 0 4px 16px rgba(239,68,68,0.2) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    color: #f0ede8 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background: #e8c547;
}

/* Dataframe */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    gap: 4px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #6b7280 !important;
    border: none !important;
    font-size: 14px;
    padding: 10px 20px;
}
.stTabs [aria-selected="true"] {
    color: #e8c547 !important;
    border-bottom: 2px solid #e8c547 !important;
}

/* Status badges */
.badge {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    padding: 3px 10px;
    border-radius: 20px;
}

/* Section headers */
.section-title {
    font-size: 13px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 12px;
    margin-top: 4px;
}

/* Upload area */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.02);
    border: 2px dashed rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 8px;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(232,197,71,0.4);
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.08);
    margin: 20px 0;
}

/* Expander */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

/* Alert/info boxes */
.stAlert {
    border-radius: 10px;
}

/* Logo / header */
.platform-logo {
    font-family: 'DM Mono', monospace;
    font-size: 20px;
    font-weight: 500;
    color: #e8c547;
    letter-spacing: -0.02em;
}

.call-row-completed { color: #10b981; }
.call-row-failed    { color: #ef4444; }
.call-row-dialing   { color: #3b82f6; }
.call-row-pending   { color: #6b7280; }

/* Pulse animation for live indicator */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}
.live-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: #10b981;
    border-radius: 50%;
    animation: pulse 1.5s ease-in-out infinite;
    margin-right: 6px;
}
</style>
""", unsafe_allow_html=True)

# ─── State ────────────────────────────────────────────────────────────────────

def init_state():
    defaults = {
        "contacts": None,
        "file_name": None,
        "active_campaign_id": None,
        "campaign_log": [],
        "tab": "Campaign",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── API helpers ─────────────────────────────────────────────────────────────

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
    """Returns list of (label, assistant_id) tuples for selectbox."""
    assistants = api_get("/assistants", [])
    settings = api_get("/settings", {})
    default_id = settings.get("vapi_assistant_id", "")
    options = [("⭐ Default" + (f" ({default_id[:14]}...)" if default_id else " (not set)"), default_id)]
    for a in assistants:
        lbl = f"🤖 {a['name']}"
        if a.get("description"):
            lbl += f"  ·  {a['description']}"
        options.append((lbl, a["assistant_id"]))
    return options

def assistant_selectbox(label, key):
    options = get_assistant_options()
    labels = [o[0] for o in options]
    idx = st.selectbox(label, range(len(labels)), format_func=lambda i: labels[i], key=key)
    return options[idx][1]


# ─── Status color mapping ──────────────────────────────────────────────────

STATUS_EMOJI = {
    "pending": "⬜",
    "queued": "🟡",
    "dialing": "🔵",
    "in-progress": "🟢",
    "completed": "✅",
    "failed": "🔴",
    "no-answer": "🟠",
    "starting": "🟡",
    "running": "🟢",
    "aborted": "🔴",
}

# ─── Sidebar ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown('<div class="platform-logo">📞 VoiceBot</div>', unsafe_allow_html=True)
    st.markdown("**Platform**")
    st.markdown("---")

    # Backend status
    alive = backend_alive()
    if alive:
        st.markdown('<span class="live-dot"></span> **Backend connected**', unsafe_allow_html=True)
    else:
        st.error("⚠️ Backend offline\n\nRun: `uvicorn backend:app --port 4000`")

    st.markdown("---")
    st.markdown('<p class="section-title">Navigation</p>', unsafe_allow_html=True)

    pages = ["🚀 Campaign", "📞 Single Call", "📊 Dashboard", "🤖 Assistants", "⚙️ Settings"]
    for p in pages:
        label = p.split(" ", 1)[1]
        if st.button(p, key=f"nav_{label}", use_container_width=True):
            st.session_state.tab = label

    st.markdown("---")
    st.markdown('<p style="font-size:11px;color:#4b5563;">VAPI + Twilio + Python</p>', unsafe_allow_html=True)

# ─── Settings page ────────────────────────────────────────────────────────────

if st.session_state.tab == "Settings":
    st.markdown("## ⚙️ Settings")
    st.markdown("Configure your VAPI and Twilio credentials.")
    st.markdown("---")

    current = api_get("/settings", {})

    with st.form("settings_form"):
        st.markdown('<p class="section-title">VAPI Configuration</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            vapi_key = st.text_input("VAPI API Key", value=current.get("vapi_api_key",""), type="password", placeholder="vapi_...")
        with col2:
            vapi_asst = st.text_input("Default Assistant ID", value=current.get("vapi_assistant_id",""), placeholder="asst_...")

        st.markdown('<p class="section-title">Twilio</p>', unsafe_allow_html=True)
        twilio_num = st.text_input(
            "VAPI Phone Number ID (linked to Twilio)",
            value=current.get("twilio_phone_number",""),
            placeholder="The Phone Number ID from VAPI dashboard",
            help="In VAPI → Phone Numbers → copy the ID (not the actual number)"
        )

        st.markdown('<p class="section-title">Rate Limiting</p>', unsafe_allow_html=True)
        cpm = st.slider("Calls per minute", min_value=1, max_value=60, value=int(current.get("calls_per_minute", 10)))

        submitted = st.form_submit_button("💾 Save Settings")
        if submitted:
            data, err = api_post("/settings", {
                "vapi_api_key": vapi_key,
                "vapi_assistant_id": vapi_asst,
                "twilio_phone_number": twilio_num,
                "calls_per_minute": cpm,
            })
            if err:
                st.error(f"Failed to save: {err}")
            else:
                st.success("✅ Settings saved!")

    st.markdown("---")
    st.markdown("### 📌 Setup Guide")
    with st.expander("How to get your VAPI credentials"):
        st.markdown("""
1. Go to [vapi.ai](https://vapi.ai) → **API Keys** → copy your key
2. Go to **Assistants** → open your bot → copy the **Assistant ID**
3. Go to **Phone Numbers** → your Twilio number → copy the **Phone Number ID**
4. Paste all three above and save
        """)
    with st.expander("Webhook setup (for live call status)"):
        st.markdown("""
In VAPI Dashboard → **Assistants** → your assistant → **Server URL**:

```
http://YOUR_SERVER_IP:4000/api/webhook/vapi
```

This lets VAPI push real-time call status updates to your backend.
Use [ngrok](https://ngrok.com) for local dev: `ngrok http 4000`
        """)

# ─── Campaign page ────────────────────────────────────────────────────────────

elif st.session_state.tab == "Campaign":
    st.markdown("## 🚀 Bulk Call Campaign")
    st.markdown("Upload a contact list and trigger outbound calls to everyone at once.")
    st.markdown("---")

    col_left, col_right = st.columns([3, 2], gap="large")

    with col_left:
        st.markdown('<p class="section-title">1 · Upload Contact List</p>', unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "CSV or Excel file",
            type=["csv", "xlsx", "xls"],
            help="File must have columns: phone (required), name (optional)",
            label_visibility="collapsed",
        )

        if uploaded:
            try:
                if uploaded.name.endswith(".csv"):
                    df = pd.read_csv(uploaded)
                else:
                    df = pd.read_excel(uploaded)

                # Normalize column names
                df.columns = [c.strip().lower() for c in df.columns]

                # Find phone column
                phone_col = next((c for c in df.columns if "phone" in c or "mobile" in c or "number" in c), df.columns[0])
                name_col = next((c for c in df.columns if "name" in c), None)

                df = df.rename(columns={phone_col: "phone"})
                if name_col and name_col != "phone":
                    df = df.rename(columns={name_col: "name"})
                else:
                    df["name"] = [f"Contact {i+1}" for i in range(len(df))]

                df["phone"] = df["phone"].astype(str).str.strip()
                df = df[df["phone"].str.len() > 5][["name", "phone"]].reset_index(drop=True)

                st.session_state.contacts = df
                st.session_state.file_name = uploaded.name

                st.success(f"✅ Loaded **{len(df)} contacts** from `{uploaded.name}`")

            except Exception as e:
                st.error(f"Could not parse file: {e}")

        # Download sample CSV
        sample = "name,phone\nAlex Kumar,+919876543210\nPriya Sharma,+919123456789\nRaj Patel,+917890123456"
        st.download_button(
            "⬇️ Download sample CSV",
            data=sample,
            file_name="sample_contacts.csv",
            mime="text/csv",
        )

    with col_right:
        st.markdown('<p class="section-title">2 · Campaign Settings</p>', unsafe_allow_html=True)

        campaign_name = st.text_input("Campaign Name", placeholder="e.g. April Follow-up")
        selected_asst_id = assistant_selectbox("Select Assistant", key="campaign_asst")

        settings = api_get("/settings", {})
        cpm = settings.get("calls_per_minute", 10)

        if st.session_state.contacts is not None:
            n = len(st.session_state.contacts)
            est_min = round(n / max(cpm, 1), 1)
            st.info(f"📋 **{n} contacts** · ~{est_min} min at {cpm} calls/min")

        st.markdown("---")
        start_disabled = (st.session_state.contacts is None or not campaign_name)

        if st.button("▶ Start Campaign", disabled=start_disabled):
            if not alive:
                st.error("Backend is offline. Start the backend first.")
            else:
                contacts = st.session_state.contacts.to_dict("records")
                data, err = api_post("/campaign/start", {
                    "campaign_name": campaign_name,
                    "contacts": contacts,
                    "assistant_id": selected_asst_id or None,
                })
                if err:
                    st.error(f"Failed: {err}")
                else:
                    st.session_state.active_campaign_id = data["campaign_id"]
                    st.success(f"🚀 Campaign started! ID: `{data['campaign_id'][:8]}...`")
                    st.session_state.tab = "Dashboard"
                    st.rerun()

    # Preview table
    if st.session_state.contacts is not None:
        st.markdown("---")
        st.markdown('<p class="section-title">Contact Preview</p>', unsafe_allow_html=True)
        preview = st.session_state.contacts.head(20).copy()
        preview.index = preview.index + 1
        st.dataframe(preview, use_container_width=True, height=300)
        if len(st.session_state.contacts) > 20:
            st.caption(f"Showing 20 of {len(st.session_state.contacts)} contacts")

# ─── Single Call page ─────────────────────────────────────────────────────────

elif st.session_state.tab == "Single Call":
    st.markdown("## 📞 Single Call")
    st.markdown("Trigger a test call to one number.")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Contact Name", placeholder="e.g. Rahul Verma")
        phone = st.text_input("Phone Number", placeholder="+919876543210")
    with col2:
        single_asst_id = assistant_selectbox("Select Assistant", key="single_asst")
        st.markdown("<br>", unsafe_allow_html=True)
        call_btn = st.button("📞 Call Now")

    if call_btn:
        if not phone:
            st.warning("Phone number is required.")
        elif not alive:
            st.error("Backend offline.")
        else:
            data, err = api_post("/call/single", {
                "name": name or "Test Contact",
                "phone": phone,
                "assistant_id": single_asst_id or None,
            })
            if err:
                st.error(f"Call failed: {err}")
            else:
                st.success(f"✅ Call triggered! VAPI Call ID: `{data.get('vapi_call_id','N/A')}`")

    st.markdown("---")
    st.markdown("### Recent Individual Calls")
    calls = api_get("/calls", [])
    solo = [c for c in calls if not c.get("campaign_id")]
    if solo:
        df = pd.DataFrame(solo)[["name","phone","status","duration","started_at"]]
        df["status"] = df["status"].map(lambda s: f"{STATUS_EMOJI.get(s,'❓')} {s}")
        df["duration"] = df["duration"].apply(lambda d: f"{int(d)}s" if d else "—")
        df.columns = ["Name","Phone","Status","Duration","Started"]
        st.dataframe(df, use_container_width=True)
    else:
        st.caption("No individual calls yet.")

# ─── Dashboard page ───────────────────────────────────────────────────────────

elif st.session_state.tab == "Dashboard":
    st.markdown("## 📊 Dashboard")

    # Campaign selector
    campaigns = api_get("/campaigns", [])

    if not campaigns:
        st.info("No campaigns yet. Go to **Campaign** to start one.")
    else:
        campaign_ids = [c["id"] for c in campaigns]
        campaign_labels = [f"{c['name']} ({c['id'][:8]}) — {STATUS_EMOJI.get(c['status'],'')} {c['status']}" for c in campaigns]

        # Default to active campaign if set
        default_idx = 0
        if st.session_state.active_campaign_id in campaign_ids:
            default_idx = campaign_ids.index(st.session_state.active_campaign_id)

        selected_label = st.selectbox("Select Campaign", campaign_labels, index=default_idx)
        selected_id = campaign_ids[campaign_labels.index(selected_label)]

        campaign = api_get(f"/campaign/{selected_id}", {})
        if not campaign:
            st.error("Could not load campaign.")
        else:
            stats = campaign.get("stats", {})
            is_running = campaign.get("status") in ("running", "starting")

            # Auto-refresh when running
            if is_running:
                st.markdown('<span class="live-dot"></span> **Live — auto-refreshing**', unsafe_allow_html=True)

            # ── KPI row
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Total", stats.get("total", 0))
            c2.metric("Dispatched", stats.get("dispatched", 0))
            c3.metric("✅ Completed", stats.get("completed", 0))
            c4.metric("🔴 Failed", stats.get("failed", 0))
            c5.metric("🔵 Dialing", stats.get("dialing", 0))

            # ── Progress bar
            total = stats.get("total", 1)
            done = stats.get("completed", 0) + stats.get("failed", 0) + stats.get("no_answer", 0)
            st.progress(done / total, text=f"{done}/{total} calls finished")

            # ── Campaign info row
            col_a, col_b, col_c = st.columns(3)
            col_a.markdown(f"**Status:** {STATUS_EMOJI.get(campaign['status'],'')} `{campaign['status']}`")
            col_b.markdown(f"**Started:** {campaign.get('started_at','—')[:19] if campaign.get('started_at') else '—'}")
            col_c.markdown(f"**Rate:** {api_get('/settings',{}).get('calls_per_minute',10)} calls/min")

            # ── Abort button
            if is_running:
                st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
                if st.button("⛔ Abort Campaign"):
                    api_post(f"/campaign/{selected_id}/abort")
                    st.warning("Abort signal sent. Current dial will finish then stop.")
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("---")

            # ── Calls table
            st.markdown('<p class="section-title">Call Log</p>', unsafe_allow_html=True)
            calls = campaign.get("calls", [])
            if calls:
                df = pd.DataFrame(calls)
                display_cols = ["name","phone","status","duration","error"]
                df = df[[c for c in display_cols if c in df.columns]]
                df["status"] = df["status"].map(lambda s: f"{STATUS_EMOJI.get(s,'❓')} {s}")
                df["duration"] = df["duration"].apply(lambda d: f"{int(d)}s" if d else "—")
                df["error"] = df.get("error","").fillna("—")
                df.columns = [c.capitalize() for c in df.columns]
                st.dataframe(df, use_container_width=True, height=400)

                # Export
                csv = pd.DataFrame(calls).to_csv(index=False)
                st.download_button(
                    "⬇️ Export call log CSV",
                    data=csv,
                    file_name=f"campaign_{selected_id[:8]}_calls.csv",
                    mime="text/csv",
                )
            else:
                st.caption("No calls dispatched yet.")

            # ── Auto-refresh
            if is_running:
                time.sleep(3)
                st.rerun()

elif st.session_state.tab == "Assistants":
    st.markdown("## 🤖 Assistants")
    st.markdown("Add and manage all your VAPI assistants. Select any one per campaign or call.")
    st.markdown("---")

    assistants = api_get("/assistants", [])

    with st.expander("➕ Add New Assistant", expanded=len(assistants) == 0):
        with st.form("add_assistant_form"):
            st.markdown('<p class="section-title">New Assistant</p>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                new_name = st.text_input("Display Name", placeholder="e.g. Sales Bot, Support Bot")
                new_asst_id = st.text_input("VAPI Assistant ID", placeholder="asst_...")
            with c2:
                new_desc = st.text_input("Description (optional)", placeholder="e.g. Handles product inquiries")
                st.markdown("<br>", unsafe_allow_html=True)
                add_btn = st.form_submit_button("➕ Add Assistant")
            if add_btn:
                if not new_name or not new_asst_id:
                    st.warning("Name and Assistant ID are required.")
                else:
                    data, err = api_post("/assistants", {
                        "name": new_name,
                        "assistant_id": new_asst_id,
                        "description": new_desc,
                    })
                    if err:
                        st.error(f"Failed: {err}")
                    else:
                        st.success(f"✅ **{new_name}** added!")
                        st.rerun()

    st.markdown("---")

    if not assistants:
        st.info("No assistants yet. Add your first one above.")
    else:
        st.markdown(f'<p class="section-title">{len(assistants)} assistant{"s" if len(assistants) != 1 else ""}</p>', unsafe_allow_html=True)
        for a in assistants:
            col_name, col_id, col_desc, col_del = st.columns([2, 3, 3, 1])
            with col_name:
                st.markdown(f"**{a['name']}**")
            with col_id:
                st.code(a["assistant_id"], language=None)
            with col_desc:
                st.caption(a.get("description") or "—")
            with col_del:
                if st.button("🗑️", key=f"del_{a['id']}", help="Delete"):
                    try:
                        requests.delete(f"{API}/assistants/{a['id']}", timeout=5)
                        st.success("Deleted.")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
            st.markdown('<hr style="margin:6px 0;border-color:rgba(255,255,255,0.05)">', unsafe_allow_html=True)

    st.markdown("---")
    st.info("💡 **Tip:** Each client or use case can have its own assistant. They all share the same Twilio number.")


# ─── Floating help ─────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown(
    '<p style="font-size:12px;color:#374151;text-align:center;">VoiceBot Platform · VAPI + Twilio + Python · '
    '<a href="https://docs.vapi.ai" style="color:#e8c547;text-decoration:none;">VAPI Docs</a></p>',
    unsafe_allow_html=True
)
