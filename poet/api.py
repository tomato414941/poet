import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import asyncio
from typing import List, Optional
from asyncio import Lock
from dotenv import load_dotenv

from .poet import Poet

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Poet API",
    description="""
    A philosophical thinking system API.
    
    The system automatically generates new philosophical thoughts every 10 minutes.
    Each thought builds upon the previous one, creating a continuous chain of philosophical exploration.
    
    The thought generation starts automatically when the server starts.
    Use these endpoints to access the generated thoughts.
    """,
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hold Poet instance as a singleton
poet = Poet("思考とは何だろうか")
thoughts_history: List[dict] = []  # Store thought history
thinking_lock = Lock()  # Lock for synchronizing thought generation

class ThoughtResponse(BaseModel):
    id: int
    timestamp: str
    input: str
    thought: str
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "timestamp": "2025-01-19 18:30:00",
                "input": "思考とは何だろうか",
                "thought": "思考とは、意識が自己を認識する過程かもしれない。"
            }
        }

@app.get("/thoughts", response_model=List[ThoughtResponse], tags=["thoughts"])
async def get_thoughts():
    """
    Get the complete history of all generated thoughts.
    
    Returns a list of thoughts in chronological order, from oldest to newest.
    Each thought includes its ID, timestamp, input (previous thought), and the generated thought.
    """
    return thoughts_history

@app.get("/thoughts/latest", response_model=ThoughtResponse, tags=["thoughts"])
async def get_latest_thought():
    """
    Get the most recent thought.
    
    Returns the latest generated thought, including its ID, timestamp, input (previous thought),
    and the generated thought. If no thoughts have been generated yet, returns a 404 error.
    """
    if not thoughts_history:
        raise HTTPException(status_code=404, detail="No thoughts in history")
    return thoughts_history[-1]

async def record_thought(thought: str):
    """Record a new thought in the history"""
    async with thinking_lock:  # Ensure thread-safe access to thoughts_history
        thought_record = {
            "id": len(thoughts_history) + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "input": poet.prompt,
            "thought": thought
        }
        thoughts_history.append(thought_record)
        print(f"New thought recorded: {thought[:50]}...")

@app.on_event("startup")
async def startup_event():
    """Start the continuous thought generation when the server starts"""
    # Set up thought recording
    poet.on_thought_generated = record_thought
    
    # Start the continuous thinking process
    asyncio.create_task(poet.think_forever())

# Mount static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")
