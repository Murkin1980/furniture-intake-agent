from fastapi import APIRouter, HTTPException
from app.core.supabase import get_supabase
from app.models.schemas import LeadCreate, LeadResponse
from typing import List

router = APIRouter()


@router.get("/", response_model=List[LeadResponse])
async def get_leads(company_id: str):
    supabase = get_supabase()
    result = supabase.table("leads").select("*").eq("company_id", company_id).execute()
    return result.data


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(lead_id: str):
    supabase = get_supabase()
    result = supabase.table("leads").select("*").eq("id", lead_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Lead not found")
    return result.data[0]


@router.post("/", response_model=LeadResponse)
async def create_lead(lead: LeadCreate):
    supabase = get_supabase()
    result = supabase.table("leads").insert(lead.model_dump()).execute()
    return result.data[0]


@router.patch("/{lead_id}", response_model=LeadResponse)
async def update_lead(lead_id: str, updates: dict):
    supabase = get_supabase()
    result = supabase.table("leads").update(updates).eq("id", lead_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Lead not found")
    return result.data[0]
