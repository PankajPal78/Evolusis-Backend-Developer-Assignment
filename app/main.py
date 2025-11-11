from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from loguru import logger
from .models import AskRequest, AskResponse
from .agent import Agent
import os

app = FastAPI(title="Evolusis – AI Reasoning Agent", version="1.0.0")
agent = Agent()

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "message": "Agent is running."}

@app.post("/ask", response_model=AskResponse, tags=["agent"])
async def ask(req: AskRequest):
    try:
        reasoning, answer, tools = await agent.answer(req.query)
        return AskResponse(reasoning=reasoning, answer=answer, used_tools=tools)
    except Exception as e:
        logger.exception("Unhandled error in /ask")
        raise HTTPException(status_code=500, detail=str(e))

# Serve the HTML UI
@app.get("/")
async def serve_ui():
    """Serve the HTML UI"""
    html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    else:
        return {"error": "UI not found"}
