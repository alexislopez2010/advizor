"""
adviZor - FastAPI Backend
"""

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from analyzer import analyze_client, chat_with_agent
from pdf_generator import generate_pdf
from data import CLIENT, SERVICES

app = FastAPI(title="adviZor API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []


@app.get("/api/client")
def get_client():
    return CLIENT


@app.get("/api/services")
def get_services():
    return list(SERVICES.values())


@app.get("/api/analyze")
def run_analysis():
    result = analyze_client(CLIENT)
    return result


@app.post("/api/chat")
def chat(req: ChatRequest):
    history = [{"role": m.role, "content": m.content} for m in req.history]
    reply = chat_with_agent(req.message, history)
    return {"reply": reply}


@app.get("/api/report/pdf")
def download_pdf():
    analysis = analyze_client(CLIENT)
    pdf_bytes = generate_pdf(analysis)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=adviZor-NovaPulse-Brief.pdf"}
    )
