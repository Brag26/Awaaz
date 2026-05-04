# Volant - VoiceBot Platform 📞

A full-stack voice bot campaign platform built with **Streamlit + FastAPI + VAPI + Twilio**.

## What it does

- **Bulk calling** — upload a CSV/Excel of contacts, click start, it calls everyone automatically
- **Single call** — test a number instantly from the UI
- **Live dashboard** — real-time campaign progress, call statuses, export logs
- **Webhook support** — VAPI pushes live call status updates back to your backend

---

## Project Structure

```
voicebot/
├── app.py           # Streamlit frontend (run this)
├── backend.py       # FastAPI backend (run this too)
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the backend

```bash
uvicorn backend:app --reload --port 4000
```

### 3. Start Streamlit

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## Configuration (in the UI → Settings tab)

| Field | Where to get it |
|---|---|
| VAPI API Key | [vapi.ai](https://vapi.ai) → API Keys |
| Assistant ID | VAPI → Assistants → your bot → copy ID |
| Phone Number ID | VAPI → Phone Numbers → your Twilio number → copy ID |
| Calls per minute | Set based on your VAPI plan limits |

---

## CSV Format

Your contact file needs at least a phone column. Name is optional.

```csv
name,phone
Alex Kumar,+919876543210
Priya Sharma,+919123456789
```

Phone numbers should be in E.164 format: `+[country code][number]`
India example: `+919876543210`

---

## VAPI Webhook Setup

For live call status (completed, failed, transcript):

1. In VAPI Dashboard → Assistants → your assistant → **Server URL**:
   ```
   https://your-server.com/api/webhook/vapi
   ```

2. For local dev, use [ngrok](https://ngrok.com):
   ```bash
   ngrok http 4000
   ```
   Then paste the ngrok URL into VAPI.

---

## Production Deployment

### Backend (FastAPI)
- Deploy to **Railway**, **Render**, or a VPS (DigitalOcean/EC2)
- Use `gunicorn` with uvicorn workers:
  ```bash
  gunicorn backend:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:4000
  ```

### Frontend (Streamlit)
- Deploy to **Streamlit Community Cloud** (free): https://streamlit.io/cloud
- Or deploy alongside the backend on any server

### Database
- The backend currently uses in-memory storage (resets on restart)
- For production, swap in **Supabase** (free Postgres):
  ```bash
  pip install supabase
  ```
  Replace the `DB` dict in `backend.py` with Supabase calls

---

## Architecture

```
Streamlit App (UI)
     │
     ▼ HTTP
FastAPI Backend (port 4000)
     │              │
     ▼              ▼
  VAPI API     In-memory DB
     │          (→ Supabase)
     ▼
 Twilio PSTN
     │
     ▼
 Phone rings!
```

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/settings` | Get current config |
| POST | `/api/settings` | Save config |
| POST | `/api/campaign/start` | Start bulk campaign |
| GET | `/api/campaign/{id}` | Get campaign + call statuses |
| POST | `/api/campaign/{id}/abort` | Stop a running campaign |
| GET | `/api/campaigns` | List all campaigns |
| POST | `/api/call/single` | Trigger one call |
| POST | `/api/webhook/vapi` | VAPI status webhook |
| GET | `/health` | Health check |
