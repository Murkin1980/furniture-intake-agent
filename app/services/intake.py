import asyncio
from app.services.intent import recognize_intent
from app.services.extract import extract_facts
from app.services.questions import get_next_question, is_complete
from app.services.summary import generate_summary
from app.services.telegram import send_lead_notification
from app.core.supabase import get_supabase


class KitchenIntake:
    def __init__(self, lead_id: str, conversation_id: str):
        self.lead_id = lead_id
        self.conversation_id = conversation_id
        self.supabase = get_supabase()
        self.session = self._get_or_create_session()
        self.answers = self._load_answers()

    def _get_or_create_session(self) -> dict:
        result = self.supabase.table("intake_sessions").select("*").eq("lead_id", self.lead_id).eq("status", "in_progress").execute()

        if result.data:
            return result.data[0]

        session_data = {
            "lead_id": self.lead_id,
            "conversation_id": self.conversation_id,
            "furniture_type": "kitchen",
            "status": "in_progress",
        }
        result = self.supabase.table("intake_sessions").insert(session_data).execute()
        return result.data[0]

    def _load_answers(self) -> dict:
        result = self.supabase.table("intake_answers").select("*").eq("session_id", self.session["id"]).execute()

        answers = {}
        for row in result.data:
            answers[row["question_key"]] = row["answer_text"] or row["answer_data"]
        return answers

    def process_message(self, message: str) -> str:
        intent = recognize_intent(message)

        if intent["intent"] == "complaint":
            return "Понимаю ваше недовольство. Сейчас подключу менеджера, который поможет решить вопрос."

        if intent["intent"] == "other":
            return "Извините, я пока могу помочь только с выбором и заказом кухни. Расскажите о ваших пожеланиях?"

        facts = extract_facts(message)
        self._save_facts(facts)

        if is_complete(self.answers):
            return self._finish_session()

        next_q = get_next_question(self.answers)
        if next_q:
            return next_q["text"]

        return "Спасибо! Менеджер свяжется с вами в ближайшее время."

    def _save_facts(self, facts: dict):
        for key, value in facts.items():
            if key in ["width", "height", "depth"]:
                value = {"value": value}

            existing = self.supabase.table("intake_answers").select("*").eq("session_id", self.session["id"]).eq("question_key", key).execute()

            if existing.data:
                self.supabase.table("intake_answers").update({"answer_text": str(value)}).eq("id", existing.data[0]["id"]).execute()
            else:
                self.supabase.table("intake_answers").insert({
                    "session_id": self.session["id"],
                    "question_key": key,
                    "question_text": "",
                    "answer_text": str(value),
                }).execute()

            self.answers[key] = value

    def _finish_session(self) -> str:
        summary = generate_summary(self.answers)

        self.supabase.table("intake_sessions").update({
            "status": "completed",
            "summary": summary,
        }).eq("id", self.session["id"]).execute()

        self.supabase.table("leads").update({
            "status": "ready_for_manager",
        }).eq("id", self.lead_id).execute()

        lead = self.supabase.table("leads").select("*").eq("id", self.lead_id).execute().data[0]
        company = self.supabase.table("companies").select("*").eq("id", lead.get("company_id", "")).execute().data

        if company and company[0].get("telegram_chat_id"):
            chat_id = int(company[0]["telegram_chat_id"])
            asyncio.create_task(send_lead_notification(chat_id, lead, summary, self.lead_id))

        return f"Спасибо! Вот ваше заявка:\n\n{summary}\n\nМенеджер свяжется с вами в ближайшее время для уточнения деталей и назначения замера."
