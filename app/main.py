from fastapi import FastAPI, HTTPException
from loguru import logger
from .models import AskRequest, AskResponse
from .agent import Agent

app = FastAPI(title="Evolusis – AI Reasoning Agent", version="1.0.0")
agent = Agent()

@app.get("/", tags=["health"])
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
