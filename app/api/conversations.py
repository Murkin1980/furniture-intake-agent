from fastapi import APIRouter, HTTPException
from app.core.supabase import get_supabase
from app.models.schemas import ConversationCreate, ConversationResponse, MessageCreate, MessageResponse
from typing import List

router = APIRouter()


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: str):
    supabase = get_supabase()
    result = supabase.table("conversations").select("*").eq("id", conversation_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return result.data[0]


@router.post("/", response_model=ConversationResponse)
async def create_conversation(conversation: ConversationCreate):
    supabase = get_supabase()
    result = supabase.table("conversations").insert(conversation.model_dump()).execute()
    return result.data[0]


@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(conversation_id: str):
    supabase = get_supabase()
    result = supabase.table("messages").select("*").eq("conversation_id", conversation_id).order("created_at").execute()
    return result.data


@router.post("/{conversation_id}/messages", response_model=MessageResponse)
async def create_message(conversation_id: str, message: MessageCreate):
    supabase = get_supabase()
    data = message.model_dump()
    data["conversation_id"] = conversation_id
    result = supabase.table("messages").insert(data).execute()
    return result.data[0]
