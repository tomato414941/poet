from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Poet",
    description="An autonomous thinking system",
    version="0.1.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開発段階では全てのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Poet API is running"}

@app.get("/api/thoughts")
async def list_thoughts():
    return {"thoughts": []}  # 仮の実装

@app.get("/api/thoughts/{thought_id}")
async def get_thought(thought_id: str):
    return {"thought_id": thought_id, "content": "Sample thought"}  # 仮の実装
