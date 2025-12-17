from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from mcp_tools.tools import chat_with_llm

load_dotenv()

app = FastAPI(title="MCP Ollama Server")

# -----------------------
# CORS
# -----------------------
origins = os.getenv("CORS_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/aa")
async def test():
    return {"msg": "hello"}

# -----------------------
# MCP Tool Endpoint
# -----------------------
@app.post("/mcp/tools/llm_chat")
async def llm_chat(payload: dict):
    """
    MCP-compatible Tool Endpoint
    """
    prompt = payload.get("prompt")
    return await chat_with_llm(prompt)
