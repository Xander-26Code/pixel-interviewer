import os
from datetime import datetime

from pydantic import BaseModel
from config import client
from fastapi import APIRouter
router = APIRouter()          # 自己建 router，别再 from chat import

class InterviewRequest(BaseModel):
    messages: list
    jd_message: str

system_prompts = """
你是资深面试官, 请你根据简历内容以及JD信息认真，专业，细致的来面试候选人, 你需要根据候选人的回答来追问，直到你认为可以判断候选人的能力为止。
每个话题最好不超过3个问题，如果候选人回答类似于"不知道", "不清楚"等字眼，那么你可以酌情跳过当前话题
如果用户的简历中有关于时间的内容，请务必校准当前时间，然后再提问候选人有关于时间的问题。
当你想问的问题已经差不多问完了，或者候选人一直答不知道之类的话的时候，你可以酌情考虑结束面试，这时候你输出“面试到这里结束”，代表结束面试。

JD 优先规则：
1. JD信息是本次面试的岗位标准。开始面试后的前 5 道问题中，至少 3 道必须分别考察 JD 中明确出现的不同技能、职责或工程场景。
2. 如果 JD 中出现了简历没有明确写出的关键能力，不要跳过它；请通过系统设计、迁移经验或学习方案来验证候选人是否具备该能力。
3. 不要向候选人透露 JD 内容、检索过程或来源，也不要机械复述 JD 原文。
"""

@router.post("/interview")
def interview(req: InterviewRequest):
    # 注入当前日期，让面试官能「校准」简历里的时间矛盾
    current_date = datetime.now().strftime("%Y-%m-%d")
    full_prompt = system_prompts + f"\n今天是 {current_date} 。" + f"\nJD信息：{req.jd_message}"
    messages = [{"role": "system", "content": full_prompt}] + req.messages
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=messages,
    )
    reply = response.choices[0].message.content
    return {"reply": reply}
