from fastapi import APIRouter, Request, HTTPException, Query
from app.core.supabase import get_supabase
from app.services.intake import KitchenIntake
from app.services.whatsapp import send_whatsapp_message, parse_webhook_entry

router = APIRouter()


@router.get("/whatsapp")
async def whatsapp_verify(
    hub_mode: str = Query(alias="hub.mode"),
    hub_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge"),
):
    if hub_mode == "subscribe" and hub_token:
        from app.core.config import settings
        if hub_token == settings.WHATSAPP_VERIFY_TOKEN:
            return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Forbidden")


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    body = await request.json()

    if "object" not in body:
        raise HTTPException(status_code=400, detail="Invalid payload")

    for entry in body.get("entry", []):
        messages = parse_webhook_entry(entry)
        for msg in messages:
            if msg.get("text"):
                await process_whatsapp_message(msg)

    return {"status": "ok"}


async def process_whatsapp_message(message: dict):
    supabase = get_supabase()

    phone = message.get("from")
    text = message.get("text")
    message_id = message.get("id")

    if not phone or not text:
        return

    leads_result = supabase.table("leads").select("*").eq("phone", phone).execute()

    if leads_result.data:
        lead = leads_result.data[0]
        response = await handle_existing_lead(lead, text, message_id)
    else:
        response = await handle_new_lead(phone, text, message_id)

    if response:
        await send_whatsapp_message(phone, response)


async def handle_new_lead(phone: str, text: str, message_id: str) -> str | None:
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

    intake = KitchenIntake(lead["id"], conversation["id"])
    response = intake.process_message(text)

    response_data = {
        "conversation_id": conversation["id"],
        "sender_type": "ai",
        "content": response,
        "message_type": "text"
    }
    supabase.table("messages").insert(response_data).execute()

    return response


async def handle_existing_lead(lead: dict, text: str, message_id: str) -> str | None:
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

    intake = KitchenIntake(lead["id"], conversation["id"])
    response = intake.process_message(text)

    response_data = {
        "conversation_id": conversation["id"],
        "sender_type": "ai",
        "content": response,
        "message_type": "text"
    }
    supabase.table("messages").insert(response_data).execute()

    return response
