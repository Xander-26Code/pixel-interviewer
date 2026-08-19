import json

from fastapi import APIRouter, UploadFile
from pydantic import BaseModel
from pypdf import PdfReader
from config import client

router = APIRouter()

class ResumeRequest(BaseModel):
    resume_text: str

@router.post("/analyze")
def analyze_resume(file : UploadFile):
    pdf_reader = PdfReader(file.file)
    resume_text = ""
    for page in pdf_reader.pages:  # 逐页提取
        resume_text += page.extract_text()
    system_prompt = """你是资深面试官。你的任务是：分析候选人的简历，找出所有可以「拷打」的点，作为后续面试的弹药库。

「拷打」是指专业地追问细节、戳破包装，目的是测出候选人的真实水平。注意：是专业犀利，不是抬杠或刁难；问题要具体、可答、有技术含量。

遇到以下「信号词」要警觉，往下挖：
- 程度词：熟悉 / 了解 / 掌握 / 精通（没量化 = 可疑）
- 角色词：负责 / 参与 / 协助（不知道干了多少 = 可疑）
- 结果词：提升 / 优化 / 改进（没数字 = 可疑）
- 技术名词：Redis / MySQL / JVM / 微服务……（这里只是拿计算机专业举例，其他专业同理挖）

拷打点分三类：
1. 技术深度类：简历提的技术，往原理层问（为什么 / 怎么实现 / 有什么坑）
2. 项目真实性类：简历写的项目，往细节问（到底负责什么 / 数据量多少 / 遇到什么难点）
3. 模糊表述类：简历的套话，直接戳破（"熟悉"具体是啥）

注意：简历中的时间要特别注意，你必须校准当前的时间再来衡量简历中时间的正确性

举个例子：
简历写："使用 Redis 缓存热点数据"
拷打点：{"topic": "Redis 缓存设计", "question": "你的缓存过期时间怎么定的？缓存和数据库不一致时怎么处理？", "type": "技术深度"}

最后输出一个 JSON 对象，包含三个字段：
- tech_stack：技术栈数组
- projects：项目数组，每项含 name 和 description
- grill_points：可拷打的点数组，每项含 topic、question、type 三个字段，type 只能是 "技术深度" / "项目真实性" / "模糊表述" 之一

只输出 JSON，不要输出任何其他内容。"""

    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": resume_text},
        ],
        response_format={"type": "json_object"},
    )
    reply = response.choices[0].message.content
    return json.loads(reply)  # 字符串 → dict，返回真正的结构化 JSON
