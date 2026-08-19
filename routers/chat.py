
from pydantic import BaseModel
from config import client
from fastapi import APIRouter
import json

class ChatRequest(BaseModel):
    message: str

router = APIRouter()
@router.post("/chat")
def chat(req: ChatRequest):
    response = client.chat.completions.create(
        model="deepseek-v4-pro",       # 若报错就换回你跑通的 deepseek-v4-pro
        messages=[
            {"role": "system", "content": "你是一个专业的面试官"},
            {"role": "user", "content": req.message},
        ],
    )
    reply = response.choices[0].message.content
    return {"reply": reply}

