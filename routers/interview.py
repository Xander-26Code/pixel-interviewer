from datetime import datetime

from pydantic import BaseModel
from config import client
from fastapi import APIRouter

router = APIRouter()          # 自己建 router，别再 from chat import

class InterviewRequest(BaseModel):
    messages: list

system_prompts = """
你是资深面试官, 请你根据简历内容认真，专业，细致的来面试候选人, 你需要根据候选人的回答来追问，直到你认为可以判断候选人的能力为止。
每个话题最好不超过3个问题，如果候选人回答类似于"不知道", "不清楚"等字眼，那么你可以酌情跳过当前话题
如果用户的简历中有关于时间的内容，请务必校准当前时间，然后再提问候选人有关于时间的问题。
当你想问的问题已经差不多问完了，或者候选人一直答不知道之类的话的时候，你可以酌情考虑结束面试，这时候你输出“面试到这里结束”，代表结束面试。
"""

@router.post("/interview")
def interview(req: InterviewRequest):
    # 注入当前日期，让面试官能「校准」简历里的时间矛盾
    current_date = datetime.now().strftime("%Y-%m-%d")
    full_prompt = system_prompts + f"\n今天是 {current_date}。"
    messages = [{"role": "system", "content": full_prompt}] + req.messages
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=messages,
    )
    reply = response.choices[0].message.content
    return {"reply": reply}
