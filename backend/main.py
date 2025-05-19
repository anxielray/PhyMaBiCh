from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# Allow CORS from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/chat"

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    messages = data.get("messages", [])

    payload = {
        "model": "mistral",
        "messages": messages,
        "stream": True,
    }

    async def ollama_stream():
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", OLLAMA_URL, json=payload, timeout=60) as response:
                async for chunk in response.aiter_text():
                    yield chunk
    return StreamingResponse(ollama_stream(), media_type="text/event-stream")
