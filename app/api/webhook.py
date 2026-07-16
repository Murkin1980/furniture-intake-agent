from fastapi import APIRouter, Request, HTTPException
from app.core.supabase import get_supabase
import hashlib
import hmac

router = APIRouter()


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    body = await request.json()

    if "object" not in body:
        raise HTTPException(status_code=400, detail="Invalid payload")

    for entry in body.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            messages = value.get("messages", [])

            for message in messages:
                await process_whatsapp_message(message)

    return {"status": "ok"}


async def process_whatsapp_message(message: dict):
    supabase = get_supabase()

    phone = message.get("from")
    text = message.get("text", {}).get("body")
    message_id = message.get("id")

    if not phone or not text:
        return

    leads_result = supabase.table("leads").select("*").eq("phone", phone).execute()

    if leads_result.data:
        lead = leads_result.data[0]
        await handle_existing_lead(lead, text, message_id)
    else:
        await handle_new_lead(phone, text, message_id)


async def handle_new_lead(phone: str, text: str, message_id: str):
    supabase = get_supabase()

    lead_data = {
        "phone": phone,
        "status": "new",
        "source": "whatsapp"
    }
    lead_result = supabase.table("leads").insert(lead_data).execute()
    lead = lead_result.data[0]

    conversation_data = {
        "lead_id": lead["id"],
        "mode": "ai_mode",
        "status": "active"
    }
    conv_result = supabase.table("conversations").insert(conversation_data).execute()
    conversation = conv_result.data[0]

    message_data = {
        "conversation_id": conversation["id"],
        "sender_type": "client",
        "content": text,
        "message_type": "text",
        "external_id": message_id
    }
    supabase.table("messages").insert(message_data).execute()


async def handle_existing_lead(lead: dict, text: str, message_id: str):
    supabase = get_supabase()

    conv_result = supabase.table("conversations").select("*").eq("lead_id", lead["id"]).eq("status", "active").execute()

    if conv_result.data:
        conversation = conv_result.data[0]
    else:
        conversation_data = {
            "lead_id": lead["id"],
            "mode": "ai_mode",
            "status": "active"
        }
        conv_result = supabase.table("conversations").insert(conversation_data).execute()
        conversation = conv_result.data[0]

    message_data = {
        "conversation_id": conversation["id"],
        "sender_type": "client",
        "content": text,
        "message_type": "text",
        "external_id": message_id
    }
    supabase.table("messages").insert(message_data).execute()
