from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LeadBase(BaseModel):
    phone: Optional[str] = None
    name: Optional[str] = None
    city: Optional[str] = None
    source: Optional[str] = None


class LeadCreate(LeadBase):
    company_id: str
    channel_id: Optional[str] = None


class LeadResponse(LeadBase):
    id: str
    company_id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConversationBase(BaseModel):
    lead_id: str
    channel_id: Optional[str] = None


class ConversationCreate(ConversationBase):
    pass


class ConversationResponse(ConversationBase):
    id: str
    mode: str
    status: str
    started_at: datetime
    last_message_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    content: str
    sender_type: str
    message_type: str = "text"


class MessageCreate(MessageBase):
    conversation_id: str


class MessageResponse(MessageBase):
    id: str
    conversation_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class IntakeSessionBase(BaseModel):
    lead_id: str
    conversation_id: str
    furniture_type: str


class IntakeSessionCreate(IntakeSessionBase):
    pass


class IntakeSessionResponse(IntakeSessionBase):
    id: str
    status: str
    summary: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class IntakeAnswerBase(BaseModel):
    question_key: str
    question_text: str
    answer_text: Optional[str] = None
    answer_data: Optional[dict] = None


class IntakeAnswerCreate(IntakeAnswerBase):
    session_id: str


class IntakeAnswerResponse(IntakeAnswerBase):
    id: str
    session_id: str
    is_confirmed: bool
    created_at: datetime

    class Config:
        from_attributes = True
