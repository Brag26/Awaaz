"""
Volant - VoiceBot Platform — Python Backend
Handles VAPI call dispatch, status tracking, and data persistence.
Run: uvicorn backend:app --reload --port 4000
"""

import os
import json
import time
import threading
import uuid
from datetime import datetime
from typing import Optional
import requests
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Volant - VoiceBot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── In-memory store (replace with Supabase/Postgres in production) ───────────
DB = {
    "campaigns": {},   # campaign_id -> campaign data
    "calls": {},       # call_id -> call data
    "settings": {
        "vapi_api_key": "",
        "vapi_assistant_id": "",
        "twilio_phone_number": "",
        "calls_per_minute": 10,
    },
    "assistants": {},  # assistant_id -> {id, name, assistant_id, description}
}

# ─── Models ───────────────────────────────────────────────────────────────────

class Settings(BaseModel):
    vapi_api_key: str
    vapi_assistant_id: str
    twilio_phone_number: str
    calls_per_minute: int = 10

class BulkCallRequest(BaseModel):
    campaign_name: str
    contacts: list[dict]  # [{name, phone}]
    assistant_id: Optional[str] = None

class SingleCallRequest(BaseModel):
    name: str
    phone: str
    assistant_id: Optional[str] = None

class VAPIWebhook(BaseModel):
    call: Optional[dict] = None
    type: Optional[str] = None

class Assistant(BaseModel):
    name: str
    assistant_id: str
    description: Optional[str] = ""

# ─── Settings ─────────────────────────────────────────────────────────────────

@app.get("/api/settings")
def get_settings():
    return DB["settings"]

@app.post("/api/settings")
def save_settings(s: Settings):
    DB["settings"].update(s.dict())
    return {"ok": True}

# ─── Assistants CRUD ──────────────────────────────────────────────────────────

@app.get("/api/assistants")
def list_assistants():
    return list(DB["assistants"].values())

@app.post("/api/assistants")
def add_assistant(a: Assistant):
    record_id = str(uuid.uuid4())
    DB["assistants"][record_id] = {
        "id": record_id,
        "name": a.name,
        "assistant_id": a.assistant_id,
        "description": a.description,
        "created_at": datetime.utcnow().isoformat(),
    }
    return DB["assistants"][record_id]

@app.delete("/api/assistants/{record_id}")
def delete_assistant(record_id: str):
    if record_id not in DB["assistants"]:
        raise HTTPException(404, "Not found")
    del DB["assistants"][record_id]
    return {"ok": True}

@app.put("/api/assistants/{record_id}")
def update_assistant(record_id: str, a: Assistant):
    if record_id not in DB["assistants"]:
        raise HTTPException(404, "Not found")
    DB["assistants"][record_id].update({
        "name": a.name,
        "assistant_id": a.assistant_id,
        "description": a.description,
    })
    return DB["assistants"][record_id]

# ─── VAPI Call Helper ─────────────────────────────────────────────────────────

def vapi_create_call(phone: str, name: str, assistant_id: str, api_key: str, twilio_number: str) -> dict:
    """Trigger a single outbound call via VAPI."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "assistantId": assistant_id,
        "customer": {
            "number": phone,
            "name": name,
        },
        "phoneNumberId": twilio_number,  # Your VAPI phone number ID linked to Twilio
    }
    resp = requests.post("https://api.vapi.ai/call", headers=headers, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()


def vapi_get_call(call_id: str, api_key: str) -> dict:
    """Fetch call status from VAPI."""
    headers = {"Authorization": f"Bearer {api_key}"}
    resp = requests.get(f"https://api.vapi.ai/call/{call_id}", headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()


# ─── Background bulk caller ───────────────────────────────────────────────────

def run_bulk_campaign(campaign_id: str):
    """Background thread: dispatches calls with rate limiting."""
    campaign = DB["campaigns"][campaign_id]
    settings = DB["settings"]
    api_key = settings["vapi_api_key"]
    assistant_id = campaign.get("assistant_id") or settings["vapi_assistant_id"]
    twilio_number = settings["twilio_phone_number"]
    calls_per_minute = settings["calls_per_minute"]
    delay = 60.0 / max(calls_per_minute, 1)

    campaign["status"] = "running"
    campaign["started_at"] = datetime.utcnow().isoformat()

    for contact in campaign["contacts"]:
        if campaign.get("abort"):
            break

        call_id = str(uuid.uuid4())
        call_record = {
            "id": call_id,
            "campaign_id": campaign_id,
            "name": contact["name"],
            "phone": contact["phone"],
            "status": "queued",
            "vapi_call_id": None,
            "started_at": datetime.utcnow().isoformat(),
            "ended_at": None,
            "duration": None,
            "transcript": None,
            "error": None,
        }
        DB["calls"][call_id] = call_record
        contact["call_id"] = call_id

        try:
            result = vapi_create_call(
                phone=contact["phone"],
                name=contact["name"],
                assistant_id=assistant_id,
                api_key=api_key,
                twilio_number=twilio_number,
            )
            call_record["vapi_call_id"] = result.get("id")
            call_record["status"] = "dialing"
        except Exception as e:
            call_record["status"] = "failed"
            call_record["error"] = str(e)

        campaign["dispatched"] = campaign.get("dispatched", 0) + 1
        time.sleep(delay)

    if not campaign.get("abort"):
        campaign["status"] = "completed"
    else:
        campaign["status"] = "aborted"

    campaign["ended_at"] = datetime.utcnow().isoformat()


# ─── Campaign endpoints ───────────────────────────────────────────────────────

@app.post("/api/campaign/start")
def start_campaign(req: BulkCallRequest, background_tasks: BackgroundTasks):
    settings = DB["settings"]
    if not settings["vapi_api_key"]:
        raise HTTPException(400, "VAPI API key not configured")
    if not settings["vapi_assistant_id"] and not req.assistant_id:
        raise HTTPException(400, "Assistant ID not configured")

    campaign_id = str(uuid.uuid4())
    DB["campaigns"][campaign_id] = {
        "id": campaign_id,
        "name": req.campaign_name,
        "contacts": [{"name": c.get("name", ""), "phone": c["phone"], "call_id": None} for c in req.contacts],
        "assistant_id": req.assistant_id,
        "status": "starting",
        "total": len(req.contacts),
        "dispatched": 0,
        "created_at": datetime.utcnow().isoformat(),
        "started_at": None,
        "ended_at": None,
        "abort": False,
    }
    background_tasks.add_task(run_bulk_campaign, campaign_id)
    return {"campaign_id": campaign_id}


@app.get("/api/campaign/{campaign_id}")
def get_campaign(campaign_id: str):
    c = DB["campaigns"].get(campaign_id)
    if not c:
        raise HTTPException(404, "Campaign not found")
    calls = [DB["calls"][cid["call_id"]] for cid in c["contacts"] if cid.get("call_id") and cid["call_id"] in DB["calls"]]
    stats = {
        "total": c["total"],
        "dispatched": c["dispatched"],
        "completed": sum(1 for x in calls if x["status"] == "completed"),
        "failed": sum(1 for x in calls if x["status"] == "failed"),
        "dialing": sum(1 for x in calls if x["status"] in ("dialing", "in-progress", "queued")),
        "no_answer": sum(1 for x in calls if x["status"] == "no-answer"),
    }
    return {**c, "stats": stats, "calls": calls}


@app.post("/api/campaign/{campaign_id}/abort")
def abort_campaign(campaign_id: str):
    c = DB["campaigns"].get(campaign_id)
    if not c:
        raise HTTPException(404, "Not found")
    c["abort"] = True
    return {"ok": True}


@app.get("/api/campaigns")
def list_campaigns():
    return list(DB["campaigns"].values())


# ─── Single call ──────────────────────────────────────────────────────────────

@app.post("/api/call/single")
def single_call(req: SingleCallRequest):
    settings = DB["settings"]
    if not settings["vapi_api_key"]:
        raise HTTPException(400, "VAPI API key not configured")

    try:
        result = vapi_create_call(
            phone=req.phone,
            name=req.name,
            assistant_id=req.assistant_id or settings["vapi_assistant_id"],
            api_key=settings["vapi_api_key"],
            twilio_number=settings["twilio_phone_number"],
        )
        call_id = str(uuid.uuid4())
        DB["calls"][call_id] = {
            "id": call_id,
            "campaign_id": None,
            "name": req.name,
            "phone": req.phone,
            "status": "dialing",
            "vapi_call_id": result.get("id"),
            "started_at": datetime.utcnow().isoformat(),
            "ended_at": None,
            "duration": None,
            "transcript": None,
            "error": None,
        }
        return {"ok": True, "call_id": call_id, "vapi_call_id": result.get("id")}
    except Exception as e:
        raise HTTPException(500, str(e))


# ─── VAPI Webhook (status updates) ───────────────────────────────────────────

@app.post("/api/webhook/vapi")
async def vapi_webhook(payload: dict):
    """
    VAPI sends status updates here. Configure this URL in your VAPI dashboard:
    https://yourdomain.com/api/webhook/vapi
    """
    call_data = payload.get("call", {})
    vapi_call_id = call_data.get("id")
    status = payload.get("type", "")  # call-start, call-end, transcript, etc.

    # Find matching call record
    for call in DB["calls"].values():
        if call.get("vapi_call_id") == vapi_call_id:
            if status == "call-start":
                call["status"] = "in-progress"
            elif status == "call-end":
                ended = call_data.get("endedReason", "completed")
                call["status"] = "completed" if ended not in ("no-answer", "failed") else ended
                call["ended_at"] = datetime.utcnow().isoformat()
                call["duration"] = call_data.get("duration")
                call["transcript"] = call_data.get("transcript")
            break

    return {"ok": True}


# ─── Sync call status from VAPI (polling fallback) ───────────────────────────

@app.post("/api/sync/{call_id}")
def sync_call(call_id: str):
    call = DB["calls"].get(call_id)
    if not call or not call.get("vapi_call_id"):
        raise HTTPException(404, "Call not found")
    try:
        data = vapi_get_call(call["vapi_call_id"], DB["settings"]["vapi_api_key"])
        call["status"] = data.get("status", call["status"])
        call["duration"] = data.get("duration", call["duration"])
        call["transcript"] = data.get("transcript", call["transcript"])
        return call
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/api/calls")
def list_calls():
    return list(DB["calls"].values())


@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}
