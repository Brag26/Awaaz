"""
Volant — Backend API (No Auth)
Storage: SQLite
Run: python -m uvicorn backend:app --reload --port 4000 --host 0.0.0.0
"""

import uuid, time, sqlite3, threading
from datetime import datetime
from typing import Optional
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Olivos AI API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DB_PATH = "olivos.db"

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY DEFAULT 1,
        vapi_api_key TEXT DEFAULT '',
        vapi_assistant_id TEXT DEFAULT '',
        twilio_phone_number TEXT DEFAULT '',
        calls_per_minute INTEGER DEFAULT 10
    );
    CREATE TABLE IF NOT EXISTS assistants (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        assistant_id TEXT NOT NULL,
        description TEXT DEFAULT '',
        created_at TEXT
    );
    CREATE TABLE IF NOT EXISTS campaigns (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        status TEXT DEFAULT 'starting',
        total INTEGER DEFAULT 0,
        dispatched INTEGER DEFAULT 0,
        created_at TEXT,
        started_at TEXT,
        ended_at TEXT,
        abort INTEGER DEFAULT 0,
        assistant_id TEXT DEFAULT ''
    );
    CREATE TABLE IF NOT EXISTS calls (
        id TEXT PRIMARY KEY,
        campaign_id TEXT,
        name TEXT,
        phone TEXT,
        status TEXT DEFAULT 'pending',
        vapi_call_id TEXT,
        started_at TEXT,
        ended_at TEXT,
        duration REAL,
        transcript TEXT,
        error TEXT
    );
    """)
    if not conn.execute("SELECT id FROM settings WHERE id=1").fetchone():
        conn.execute("INSERT INTO settings (id) VALUES (1)")
    conn.commit()
    conn.close()

init_db()

def row_dict(row): return dict(row) if row else None
def rows_list(rows): return [dict(r) for r in rows]

class SettingsReq(BaseModel):
    vapi_api_key: str
    vapi_assistant_id: str
    twilio_phone_number: str
    calls_per_minute: int = 10

class AssistantReq(BaseModel):
    name: str
    assistant_id: str
    description: Optional[str] = ""

class BulkCallReq(BaseModel):
    campaign_name: str
    contacts: list[dict]
    assistant_id: Optional[str] = None

class SingleCallReq(BaseModel):
    name: str
    phone: str
    assistant_id: Optional[str] = None

@app.get("/api/settings")
def get_settings():
    conn = get_db()
    r = row_dict(conn.execute("SELECT * FROM settings WHERE id=1").fetchone())
    conn.close(); return r or {}

@app.post("/api/settings")
def save_settings(req: SettingsReq):
    conn = get_db()
    conn.execute("""UPDATE settings SET vapi_api_key=?,vapi_assistant_id=?,
                    twilio_phone_number=?,calls_per_minute=? WHERE id=1""",
                 (req.vapi_api_key, req.vapi_assistant_id,
                  req.twilio_phone_number, req.calls_per_minute))
    conn.commit(); conn.close(); return {"ok": True}

@app.get("/api/assistants")
def list_assistants():
    conn = get_db()
    rows = rows_list(conn.execute("SELECT * FROM assistants ORDER BY created_at DESC").fetchall())
    conn.close(); return rows

@app.post("/api/assistants")
def add_assistant(req: AssistantReq):
    rid = str(uuid.uuid4())
    conn = get_db()
    conn.execute("INSERT INTO assistants VALUES (?,?,?,?,?)",
                 (rid, req.name, req.assistant_id, req.description, datetime.utcnow().isoformat()))
    conn.commit(); conn.close(); return {"id": rid}

@app.delete("/api/assistants/{rid}")
def delete_assistant(rid: str):
    conn = get_db()
    conn.execute("DELETE FROM assistants WHERE id=?", (rid,))
    conn.commit(); conn.close(); return {"ok": True}

def vapi_call(phone, name, asst_id, api_key, phone_num_id):
    r = requests.post("https://api.vapi.ai/call",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"assistantId": asst_id, "customer": {"number": phone, "name": name},
              "phoneNumberId": phone_num_id}, timeout=15)
    r.raise_for_status(); return r.json()

def run_campaign(camp_id: str):
    conn = get_db()
    cfg      = row_dict(conn.execute("SELECT * FROM settings WHERE id=1").fetchone())
    camp     = row_dict(conn.execute("SELECT * FROM campaigns WHERE id=?", (camp_id,)).fetchone())
    contacts = rows_list(conn.execute("SELECT * FROM calls WHERE campaign_id=?", (camp_id,)).fetchall())
    conn.close()

    api_key   = cfg["vapi_api_key"]
    asst_id   = camp["assistant_id"] or cfg["vapi_assistant_id"]
    phone_num = cfg["twilio_phone_number"]
    delay     = 60.0 / max(cfg["calls_per_minute"], 1)

    conn = get_db()
    conn.execute("UPDATE campaigns SET status='running',started_at=? WHERE id=?",
                 (datetime.utcnow().isoformat(), camp_id))
    conn.commit(); conn.close()

    for c in contacts:
        conn = get_db()
        abort = conn.execute("SELECT abort FROM campaigns WHERE id=?", (camp_id,)).fetchone()[0]
        conn.close()
        if abort: break
        try:
            res = vapi_call(c["phone"], c["name"], asst_id, api_key, phone_num)
            conn = get_db()
            conn.execute("UPDATE calls SET status='dialing',vapi_call_id=? WHERE id=?",
                         (res.get("id"), c["id"]))
        except Exception as e:
            conn = get_db()
            conn.execute("UPDATE calls SET status='failed',error=? WHERE id=?", (str(e), c["id"]))
        conn.execute("UPDATE campaigns SET dispatched=dispatched+1 WHERE id=?", (camp_id,))
        conn.commit(); conn.close()
        time.sleep(delay)

    conn = get_db()
    abort = conn.execute("SELECT abort FROM campaigns WHERE id=?", (camp_id,)).fetchone()[0]
    conn.execute("UPDATE campaigns SET status=?,ended_at=? WHERE id=?",
                 ("aborted" if abort else "completed", datetime.utcnow().isoformat(), camp_id))
    conn.commit(); conn.close()

@app.post("/api/campaign/start")
def start_campaign(req: BulkCallReq):
    conn = get_db()
    cfg = row_dict(conn.execute("SELECT * FROM settings WHERE id=1").fetchone())
    conn.close()
    if not cfg or not cfg["vapi_api_key"]:
        raise HTTPException(400, "Configure VAPI API key in Settings first")
    camp_id = str(uuid.uuid4())
    conn = get_db()
    conn.execute("""INSERT INTO campaigns (id,name,status,total,dispatched,created_at,assistant_id)
                    VALUES (?,?,'starting',?,?,?,?)""",
                 (camp_id, req.campaign_name, len(req.contacts), 0,
                  datetime.utcnow().isoformat(), req.assistant_id or ""))
    for c in req.contacts:
        conn.execute("""INSERT INTO calls (id,campaign_id,name,phone,status,started_at)
                        VALUES (?,?,?,?,'pending',?)""",
                     (str(uuid.uuid4()), camp_id, c.get("name",""), c["phone"],
                      datetime.utcnow().isoformat()))
    conn.commit(); conn.close()
    threading.Thread(target=run_campaign, args=(camp_id,), daemon=True).start()
    return {"campaign_id": camp_id}

@app.get("/api/campaigns")
def list_campaigns():
    conn = get_db()
    rows = rows_list(conn.execute("SELECT * FROM campaigns ORDER BY created_at DESC").fetchall())
    conn.close(); return rows

@app.get("/api/campaign/{camp_id}")
def get_campaign(camp_id: str):
    conn = get_db()
    camp  = row_dict(conn.execute("SELECT * FROM campaigns WHERE id=?", (camp_id,)).fetchone())
    calls = rows_list(conn.execute("SELECT * FROM calls WHERE campaign_id=?", (camp_id,)).fetchall())
    conn.close()
    if not camp: raise HTTPException(404, "Not found")
    camp["calls"] = calls
    camp["stats"] = {
        "total":      camp["total"],
        "dispatched": camp["dispatched"],
        "completed":  sum(1 for c in calls if c["status"] == "completed"),
        "failed":     sum(1 for c in calls if c["status"] == "failed"),
        "no_answer":  sum(1 for c in calls if c["status"] == "no-answer"),
        "dialing":    sum(1 for c in calls if c["status"] in ("dialing","in-progress","queued")),
    }
    return camp

@app.post("/api/campaign/{camp_id}/abort")
def abort_campaign(camp_id: str):
    conn = get_db()
    conn.execute("UPDATE campaigns SET abort=1 WHERE id=?", (camp_id,))
    conn.commit(); conn.close(); return {"ok": True}

@app.post("/api/call/single")
def single_call(req: SingleCallReq):
    conn = get_db()
    cfg = row_dict(conn.execute("SELECT * FROM settings WHERE id=1").fetchone())
    conn.close()
    asst = req.assistant_id or cfg["vapi_assistant_id"]
    try:
        res = vapi_call(req.phone, req.name, asst, cfg["vapi_api_key"], cfg["twilio_phone_number"])
        call_id = str(uuid.uuid4())
        conn = get_db()
        conn.execute("""INSERT INTO calls (id,campaign_id,name,phone,status,vapi_call_id,started_at)
                        VALUES (?,NULL,?,?,'dialing',?,?)""",
                     (call_id, req.name, req.phone, res.get("id"), datetime.utcnow().isoformat()))
        conn.commit(); conn.close()
        return {"ok": True, "vapi_call_id": res.get("id")}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/api/calls")
def list_calls():
    conn = get_db()
    rows = rows_list(conn.execute(
        "SELECT * FROM calls WHERE campaign_id IS NULL ORDER BY started_at DESC LIMIT 20").fetchall())
    conn.close(); return rows

@app.post("/api/webhook/vapi")
async def vapi_webhook(payload: dict):
    vid = payload.get("call", {}).get("id")
    evt = payload.get("type", "")
    conn = get_db()
    call = row_dict(conn.execute("SELECT id FROM calls WHERE vapi_call_id=?", (vid,)).fetchone())
    if call:
        if evt == "call-start":
            conn.execute("UPDATE calls SET status='in-progress' WHERE id=?", (call["id"],))
        elif evt == "call-end":
            er = payload.get("call", {}).get("endedReason", "completed")
            s  = "completed" if er not in ("no-answer","failed") else er
            conn.execute("UPDATE calls SET status=?,ended_at=?,duration=?,transcript=? WHERE id=?",
                         (s, datetime.utcnow().isoformat(),
                          payload.get("call",{}).get("duration"),
                          payload.get("call",{}).get("transcript"), call["id"]))
    conn.commit(); conn.close(); return {"ok": True}

@app.get("/health")
def health(): return {"status": "ok"}
