from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.api import leads, conversations, webhook, telegram
from app.core.config import settings

app = FastAPI(
    title="Furniture Intake Agent",
    description="AI-приёмная для мебельных компаний",
    version="0.1.0",
)

app.include_router(leads.router, prefix="/api/leads", tags=["leads"])
app.include_router(conversations.router, prefix="/api/conversations", tags=["conversations"])
app.include_router(webhook.router, prefix="/webhook", tags=["webhook"])
app.include_router(telegram.router, prefix="/telegram", tags=["telegram"])

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("app/static/index.html", "r") as f:
        return HTMLResponse(content=f.read())


@app.get("/health")
async def health():
    return {"status": "ok"}
