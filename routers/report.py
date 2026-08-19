import json

from fastapi import APIRouter
from pydantic import BaseModel
from config import client

router = APIRouter()

class Report(BaseModel):
    messages: list

system_prompt = """你是资深技术面试官。下面是一段完整的面试对话记录（面试官和候选人的多轮问答）。请你站在面试官的角度，对候选人的表现进行专业、客观的评估。

请从以下 4 个维度打分（每个维度 1-10 分，10 分为满分）：
1. 技术深度：回答是否深入原理，还是停留在表面概念
2. 项目真实性：项目细节能否讲清，简历是否存在包装水分
3. 表达能力：逻辑是否清晰、表述是否简洁准确
4. 临场反应：被追问或质疑时能否保持稳定、从容应对

关键要求：
- 每个维度的分数，必须附一句「evidence（依据）」，引用对话里的具体内容，说明为什么给这个分。禁止空泛的「表现不错」「回答一般」。
- 最后给出 overall_score（总体分 1-10，可带一位小数）、summary（一句话总评）、weaknesses（薄弱点列表）、suggestions（改进建议列表）。

只输出一个 JSON 对象，结构如下：
{
  "scores": [
    {"dimension": "技术深度", "score": 7, "evidence": "..."},
    {"dimension": "项目真实性", "score": 6, "evidence": "..."},
    {"dimension": "表达能力", "score": 8, "evidence": "..."},
    {"dimension": "临场反应", "score": 5, "evidence": "..."}
  ],
  "overall_score": 6.5,
  "summary": "...",
  "weaknesses": ["...", "..."],
  "suggestions": ["...", "..."]
}
不要输出 JSON 以外的任何内容。"""

@router.post("/report")
def report(req: Report):
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(req.messages)},
        ],
        response_format = {"type": "json_object"},
    )
    reply = response.choices[0].message.content
    return json.loads(reply)  # 字符串 → dict，返回真正的结构化 JSON

