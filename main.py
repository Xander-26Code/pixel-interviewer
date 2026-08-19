from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import chat, resumeAnalyze, interview, report

load_dotenv()

app = FastAPI(title="AI 面试官")

app.include_router(chat.router)
app.include_router(resumeAnalyze.router)

app.include_router(interview.router)

app.include_router(report.router)

# 挂载前端静态页面（放在所有 API 路由之后，避免拦截 /chat 等接口）
app.mount("/", StaticFiles(directory="static", html=True), name="static")