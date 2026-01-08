from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import CompanyRequest, AgentOutput
from agent import B2BAgent
import os
import asyncio
import sys
from dotenv import load_dotenv

# Fix for Playwright/Asyncio on Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

load_dotenv()

app = FastAPI(title="B2B Lead Magnet Agent")

# Allow CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = B2BAgent()

@app.get("/")
async def root():
    return {"status": "Agent is ready"}

@app.post("/research", response_model=AgentOutput)
async def research_company(request: CompanyRequest):
    try:
        result = await agent.run(request.domain)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
