from fastapi import APIRouter, Request, HTTPException
from app.core.supabase import get_supabase
from app.services.telegram import answer_callback_query, edit_message_reply_markup

router = APIRouter()


@router.post("/webhook")
async def telegram_webhook(request: Request):
    body = await request.json()

    if "callback_query" in body:
        await handle_callback_query(body["callback_query"])

    return {"status": "ok"}


async def handle_callback_query(callback_query: dict):
    data = callback_query.get("data", "")
    chat_id = callback_query["message"]["chat"]["id"]
    message_id = callback_query["message"]["message_id"]
    callback_query_id = callback_query["id"]

    if ":" not in data:
        return

    action, lead_id = data.split(":", 1)
    supabase = get_supabase()

    if action == "take":
        await handle_take_lead(supabase, lead_id, callback_query_id, chat_id, message_id)

    elif action == "request":
        await handle_request_data(supabase, lead_id, callback_query_id, chat_id, message_id)

    elif action == "measure":
        await handle_schedule_measure(supabase, lead_id, callback_query_id, chat_id, message_id)


async def handle_take_lead(supabase, lead_id: str, callback_query_id: str, chat_id: int, message_id: int):
    supabase.table("leads").update({"status": "manager_review"}).eq("id", lead_id).execute()

    supabase.table("conversations").update({"mode": "human_mode"}).eq("lead_id", lead_id).eq("status", "active").execute()

    await answer_callback_query(callback_query_id, "✅ Заявка взята в работу")

    await edit_message_reply_markup(chat_id, message_id, {"inline_keyboard": []})

    supabase.table("activities").insert({
        "lead_id": lead_id,
        "type": "status_change",
        "description": "Менеджер взял заявку в работу",
    }).execute()


async def handle_request_data(supabase, lead_id: str, callback_query_id: str, chat_id: int, message_id: int):
    supabase.table("leads").update({"status": "waiting_for_client"}).eq("id", lead_id).execute()

    await answer_callback_query(callback_query_id, "💬 Запрос данных отправлен клиенту")


async def handle_schedule_measure(supabase, lead_id: str, callback_query_id: str, chat_id: int, message_id: int):
    supabase.table("leads").update({"status": "measurement_scheduled"}).eq("id", lead_id).execute()

    await answer_callback_query(callback_query_id, "📏 Замер назначен")

    supabase.table("tasks").insert({
        "lead_id": lead_id,
        "type": "measurement",
        "status": "pending",
        "priority": "normal",
    }).execute()
