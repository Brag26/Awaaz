"""
Volant — Backend API
Roles: super_admin | customer_admin | customer_user
Storage: SQLite (file-based, persists across restarts)
Run: uvicorn backend:app --reload --port 4000
"""

import os, uuid, time, sqlite3, hashlib, threading
from datetime import datetime
from typing import Optional
import requests
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

app = FastAPI(title="Awaaz API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DB_PATH = "awaaz.db"
security = HTTPBearer(auto_error=False)

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS customers (
        id TEXT PRIMARY KEY, name TEXT NOT NULL, created_at TEXT,
        is_active INTEGER DEFAULT 1, vapi_api_key TEXT DEFAULT '',
        vapi_assistant_id TEXT DEFAULT '', twilio_phone_number TEXT DEFAULT '',
        calls_per_minute INTEGER DEFAULT 10
    );
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY, customer_id TEXT, username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL, role TEXT NOT NULL, display_name TEXT,
        created_at TEXT, is_active INTEGER DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS sessions (
        token TEXT PRIMARY KEY, user_id TEXT NOT NULL, created_at TEXT
    );
    CREATE TABLE IF NOT EXISTS assistants (
        id TEXT PRIMARY KEY, customer_id TEXT, name TEXT NOT NULL,
        assistant_id TEXT NOT NULL, description TEXT DEFAULT '', created_at TEXT
    );
    CREATE TABLE IF NOT EXISTS campaigns (
        id TEXT PRIMARY KEY, customer_id TEXT, name TEXT NOT NULL,
        status TEXT DEFAULT 'starting', total INTEGER DEFAULT 0,
        dispatched INTEGER DEFAULT 0, created_by TEXT, created_at TEXT,
        started_at TEXT, ended_at TEXT, abort INTEGER DEFAULT 0, assistant_id TEXT DEFAULT ''
    );
    CREATE TABLE IF NOT EXISTS calls (
        id TEXT PRIMARY KEY, campaign_id TEXT, customer_id TEXT,
        name TEXT, phone TEXT, status TEXT DEFAULT 'pending',
        vapi_call_id TEXT, started_at TEXT, ended_at TEXT,
        duration REAL, transcript TEXT, error TEXT
    );
    """)
    # Seed super admin
    if not conn.execute("SELECT id FROM users WHERE role='super_admin' LIMIT 1").fetchone():
        conn.execute(
            "INSERT INTO users VALUES (?,NULL,?,?,'super_admin','Super Admin',?,1)",
            (str(uuid.uuid4()), "superadmin",
             hashlib.sha256(b"admin123").hexdigest(), datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

init_db()

def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()
def row_dict(row): return dict(row) if row else None
def rows_list(rows): return [dict(r) for r in rows]

def get_user_by_token(token):
    conn = get_db()
    s = row_dict(conn.execute("SELECT user_id FROM sessions WHERE token=?", (token,)).fetchone())
    if not s:
        conn.close(); return None
    u = row_dict(conn.execute("SELECT * FROM users WHERE id=?", (s["user_id"],)).fetchone())
    conn.close(); return u

def require_auth(cred: HTTPAuthorizationCredentials = Depends(security)):
    if not cred: raise HTTPException(401, "Not authenticated")
    u = get_user_by_token(cred.credentials)
    if not u or not u["is_active"]: raise HTTPException(401, "Invalid session")
    return u

def require_super(u=Depends(require_auth)):
    if u["role"] != "super_admin": raise HTTPException(403, "Super admin only")
    return u

def require_admin(u=Depends(require_auth)):
    if u["role"] not in ("super_admin","customer_admin"): raise HTTPException(403, "Admin required")
    return u

# ─── Models ───────────────────────────────────────────────────────────────────

class LoginReq(BaseModel):
    username: str; password: str

class CustomerReq(BaseModel):
    name: str

class UserReq(BaseModel):
    username: str; password: str; display_name: str; role: str

class SettingsReq(BaseModel):
    vapi_api_key: str; vapi_assistant_id: str
    twilio_phone_number: str; calls_per_minute: int = 10

class AssistantReq(BaseModel):
    name: str; assistant_id: str; description: Optional[str] = ""

class BulkCallReq(BaseModel):
    campaign_name: str; contacts: list[dict]; assistant_id: Optional[str] = None

class SingleCallReq(BaseModel):
    name: str; phone: str; assistant_id: Optional[str] = None

# ─── Auth ─────────────────────────────────────────────────────────────────────

@app.post("/api/auth/login")
def login(req: LoginReq):
    conn = get_db()
    u = row_dict(conn.execute(
        "SELECT * FROM users WHERE username=? AND is_active=1", (req.username,)).fetchone())
    conn.close()
    if not u or u["password_hash"] != hash_pw(req.password):
        raise HTTPException(401, "Invalid credentials")
    token = str(uuid.uuid4())
    conn = get_db()
    conn.execute("INSERT INTO sessions VALUES (?,?,?)",
                 (token, u["id"], datetime.utcnow().isoformat()))
    conn.commit(); conn.close()
    return {"token": token,
            "user": {k: u[k] for k in ("id","username","role","display_name","customer_id")}}

@app.post("/api/auth/logout")
def logout(cred: HTTPAuthorizationCredentials = Depends(security)):
    if cred:
        conn = get_db()
        conn.execute("DELETE FROM sessions WHERE token=?", (cred.credentials,))
        conn.commit(); conn.close()
    return {"ok": True}

@app.get("/api/auth/me")
def me(u=Depends(require_auth)):
    return {k: u[k] for k in ("id","username","role","display_name","customer_id")}

# ─── Customers ────────────────────────────────────────────────────────────────

@app.get("/api/customers")
def list_customers(u=Depends(require_super)):
    conn = get_db()
    rows = rows_list(conn.execute("SELECT * FROM customers ORDER BY created_at DESC").fetchall())
    for r in rows:
        r["user_count"] = conn.execute(
            "SELECT COUNT(*) FROM users WHERE customer_id=?", (r["id"],)).fetchone()[0]
        r["campaign_count"] = conn.execute(
            "SELECT COUNT(*) FROM campaigns WHERE customer_id=?", (r["id"],)).fetchone()[0]
    conn.close(); return rows

@app.post("/api/customers")
def create_customer(req: CustomerReq, u=Depends(require_super)):
    cid = str(uuid.uuid4())
    conn = get_db()
    conn.execute("INSERT INTO customers (id,name,created_at,is_active) VALUES (?,?,?,1)",
                 (cid, req.name, datetime.utcnow().isoformat()))
    conn.commit(); conn.close()
    return {"id": cid, "name": req.name}

@app.delete("/api/customers/{cid}")
def delete_customer(cid: str, u=Depends(require_super)):
    conn = get_db()
    conn.execute("UPDATE customers SET is_active=0 WHERE id=?", (cid,))
    conn.commit(); conn.close(); return {"ok": True}

# ─── Users ────────────────────────────────────────────────────────────────────

@app.get("/api/customers/{cid}/users")
def list_users(cid: str, u=Depends(require_admin)):
    if u["role"] == "customer_admin" and u["customer_id"] != cid:
        raise HTTPException(403, "Access denied")
    conn = get_db()
    rows = rows_list(conn.execute(
        "SELECT id,username,role,display_name,created_at,is_active FROM users WHERE customer_id=?",
        (cid,)).fetchall())
    conn.close(); return rows

@app.post("/api/customers/{cid}/users")
def create_user(cid: str, req: UserReq, u=Depends(require_admin)):
    if u["role"] == "customer_admin" and u["customer_id"] != cid:
        raise HTTPException(403, "Access denied")
    if req.role not in ("customer_admin","customer_user"):
        raise HTTPException(400, "Role must be customer_admin or customer_user")
    uid = str(uuid.uuid4())
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users VALUES (?,?,?,?,?,?,?,1)",
            (uid, cid, req.username, hash_pw(req.password),
             req.role, req.display_name, datetime.utcnow().isoformat()))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close(); raise HTTPException(400, "Username already taken")
    conn.close(); return {"id": uid}

@app.delete("/api/customers/{cid}/users/{uid}")
def delete_user(cid: str, uid: str, u=Depends(require_admin)):
    conn = get_db()
    conn.execute("UPDATE users SET is_active=0 WHERE id=? AND customer_id=?", (uid, cid))
    conn.commit(); conn.close(); return {"ok": True}

# ─── Settings ─────────────────────────────────────────────────────────────────

@app.get("/api/settings")
def get_settings(u=Depends(require_auth)):
    cid = u["customer_id"]
    if not cid: return {}
    conn = get_db()
    r = row_dict(conn.execute("SELECT * FROM customers WHERE id=?", (cid,)).fetchone())
    conn.close(); return r or {}

@app.post("/api/settings")
def save_settings(req: SettingsReq, u=Depends(require_admin)):
    conn = get_db()
    conn.execute("""UPDATE customers SET vapi_api_key=?,vapi_assistant_id=?,
                    twilio_phone_number=?,calls_per_minute=? WHERE id=?""",
                 (req.vapi_api_key, req.vapi_assistant_id,
                  req.twilio_phone_number, req.calls_per_minute, u["customer_id"]))
    conn.commit(); conn.close(); return {"ok": True}

# ─── Assistants ───────────────────────────────────────────────────────────────

@app.get("/api/assistants")
def list_assistants(u=Depends(require_auth)):
    conn = get_db()
    rows = rows_list(conn.execute(
        "SELECT * FROM assistants WHERE customer_id=? ORDER BY created_at DESC",
        (u["customer_id"],)).fetchall())
    conn.close(); return rows

@app.post("/api/assistants")
def add_assistant(req: AssistantReq, u=Depends(require_admin)):
    rid = str(uuid.uuid4())
    conn = get_db()
    conn.execute("INSERT INTO assistants VALUES (?,?,?,?,?,?)",
                 (rid, u["customer_id"], req.name, req.assistant_id,
                  req.description, datetime.utcnow().isoformat()))
    conn.commit(); conn.close(); return {"id": rid}

@app.delete("/api/assistants/{rid}")
def delete_assistant(rid: str, u=Depends(require_admin)):
    conn = get_db()
    conn.execute("DELETE FROM assistants WHERE id=? AND customer_id=?", (rid, u["customer_id"]))
    conn.commit(); conn.close(); return {"ok": True}

# ─── VAPI + Campaign ──────────────────────────────────────────────────────────

def vapi_call(phone, name, asst_id, api_key, phone_num_id):
    r = requests.post("https://api.vapi.ai/call",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"assistantId": asst_id, "customer": {"number": phone, "name": name},
              "phoneNumberId": phone_num_id}, timeout=15)
    r.raise_for_status(); return r.json()

def run_campaign(camp_id, customer_id):
    conn = get_db()
    cust = row_dict(conn.execute("SELECT * FROM customers WHERE id=?", (customer_id,)).fetchone())
    camp = row_dict(conn.execute("SELECT * FROM campaigns WHERE id=?", (camp_id,)).fetchone())
    contacts = rows_list(conn.execute("SELECT * FROM calls WHERE campaign_id=?", (camp_id,)).fetchall())
    conn.close()

    api_key   = cust["vapi_api_key"]
    asst_id   = camp["assistant_id"] or cust["vapi_assistant_id"]
    phone_num = cust["twilio_phone_number"]
    delay     = 60.0 / max(cust["calls_per_minute"], 1)

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
def start_campaign(req: BulkCallReq, u=Depends(require_admin)):
    conn = get_db()
    cust = row_dict(conn.execute("SELECT * FROM customers WHERE id=?", (u["customer_id"],)).fetchone())
    conn.close()
    if not cust or not cust["vapi_api_key"]:
        raise HTTPException(400, "Configure VAPI API key in Settings first")
    camp_id = str(uuid.uuid4())
    conn = get_db()
    conn.execute("""INSERT INTO campaigns (id,customer_id,name,status,total,dispatched,
                    created_by,created_at,assistant_id) VALUES (?,?,?,'starting',?,?,?,?,?)""",
                 (camp_id, u["customer_id"], req.campaign_name, len(req.contacts), 0,
                  u["id"], datetime.utcnow().isoformat(), req.assistant_id or ""))
    for c in req.contacts:
        conn.execute("""INSERT INTO calls (id,campaign_id,customer_id,name,phone,status,started_at)
                        VALUES (?,?,?,?,?,'pending',?)""",
                     (str(uuid.uuid4()), camp_id, u["customer_id"],
                      c.get("name",""), c["phone"], datetime.utcnow().isoformat()))
    conn.commit(); conn.close()
    threading.Thread(target=run_campaign, args=(camp_id, u["customer_id"]), daemon=True).start()
    return {"campaign_id": camp_id}

@app.get("/api/campaigns")
def list_campaigns(u=Depends(require_auth)):
    conn = get_db()
    rows = rows_list(conn.execute(
        "SELECT * FROM campaigns WHERE customer_id=? ORDER BY created_at DESC",
        (u["customer_id"],)).fetchall())
    conn.close(); return rows

@app.get("/api/campaign/{cid}")
def get_campaign(cid: str, u=Depends(require_auth)):
    conn = get_db()
    camp  = row_dict(conn.execute("SELECT * FROM campaigns WHERE id=?", (cid,)).fetchone())
    calls = rows_list(conn.execute("SELECT * FROM calls WHERE campaign_id=?", (cid,)).fetchall())
    conn.close()
    if not camp: raise HTTPException(404, "Not found")
    camp["calls"]  = calls
    camp["stats"]  = {
        "total":     camp["total"],
        "dispatched":camp["dispatched"],
        "completed": sum(1 for c in calls if c["status"]=="completed"),
        "failed":    sum(1 for c in calls if c["status"]=="failed"),
        "no_answer": sum(1 for c in calls if c["status"]=="no-answer"),
        "dialing":   sum(1 for c in calls if c["status"] in ("dialing","in-progress","queued")),
    }
    return camp

@app.post("/api/campaign/{cid}/abort")
def abort_campaign(cid: str, u=Depends(require_admin)):
    conn = get_db()
    conn.execute("UPDATE campaigns SET abort=1 WHERE id=?", (cid,))
    conn.commit(); conn.close(); return {"ok": True}

@app.post("/api/call/single")
def single_call(req: SingleCallReq, u=Depends(require_admin)):
    conn = get_db()
    cust = row_dict(conn.execute("SELECT * FROM customers WHERE id=?", (u["customer_id"],)).fetchone())
    conn.close()
    asst = req.assistant_id or cust["vapi_assistant_id"]
    try:
        res = vapi_call(req.phone, req.name, asst, cust["vapi_api_key"], cust["twilio_phone_number"])
        cid = str(uuid.uuid4())
        conn = get_db()
        conn.execute("""INSERT INTO calls (id,campaign_id,customer_id,name,phone,status,vapi_call_id,started_at)
                        VALUES (?,NULL,?,?,?,'dialing',?,?)""",
                     (cid, u["customer_id"], req.name, req.phone,
                      res.get("id"), datetime.utcnow().isoformat()))
        conn.commit(); conn.close()
        return {"ok": True, "vapi_call_id": res.get("id")}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/api/calls")
def list_calls(u=Depends(require_auth)):
    conn = get_db()
    rows = rows_list(conn.execute(
        "SELECT * FROM calls WHERE customer_id=? AND campaign_id IS NULL ORDER BY started_at DESC LIMIT 20",
        (u["customer_id"],)).fetchall())
    conn.close(); return rows

@app.post("/api/webhook/vapi")
async def vapi_webhook(payload: dict):
    vid = payload.get("call",{}).get("id")
    evt = payload.get("type","")
    conn = get_db()
    call = row_dict(conn.execute("SELECT id FROM calls WHERE vapi_call_id=?", (vid,)).fetchone())
    if call:
        if evt == "call-start":
            conn.execute("UPDATE calls SET status='in-progress' WHERE id=?", (call["id"],))
        elif evt == "call-end":
            er = payload.get("call",{}).get("endedReason","completed")
            s  = "completed" if er not in ("no-answer","failed") else er
            conn.execute("UPDATE calls SET status=?,ended_at=?,duration=?,transcript=? WHERE id=?",
                         (s, datetime.utcnow().isoformat(),
                          payload.get("call",{}).get("duration"),
                          payload.get("call",{}).get("transcript"), call["id"]))
    conn.commit(); conn.close(); return {"ok": True}

@app.get("/health")
def health(): return {"status": "ok"}
