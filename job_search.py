from pathlib import Path
from dotenv import load_dotenv
from fastapi import APIRouter
from pydantic import BaseModel

from config import firecrawl
load_dotenv(Path(__file__).with_name(".env"))




router = APIRouter()

class JobSearchRequest(BaseModel):
    position: str


@router.post("/search")
def search_jds(request: JobSearchRequest):
    position = request.position.strip()
    results = firecrawl.search(
        query=f'"{position}" "岗位职责" "任职要求"',
        limit=15,
        scrape_options={
            "formats": ["markdown"],
        },
    )

    markdowns = []

    for result in results.web:
        markdown = getattr(result, "markdown", "") or ""

        if is_valid_jd(markdown):
            markdowns.append(markdown)

    return {
        "position": position,
        "count": len(markdowns),
        "documents": markdowns,
    }

DUTY_MARKERS = [
    "岗位职责",
    "职位描述",
    "工作职责",
    "职责描述",
    "工作内容",
    "主要职责",
]

REQUIREMENT_MARKERS = [
    "岗位要求",
    "任职要求",
    "职位要求",
    "任职资格",
    "任职条件",
    "岗位资格",
    "基本要求",
]

BONUS_MARKERS = [
    "加分项",
    "优先条件",
    "优先考虑",
]

EXCLUSION_MARKERS = [
    "立即绑定",
    "猜你想问",
    "CSDN",
    "相关文章",
    "热门推荐",
    "版权声明",
    "登录后",
    "学习路线",
    "岗位认知",
    "转行",
    "小白",
    "课程",
    "培训",
    "薪资",
    "职业前景",
    "面试题",
]
def has_any_marker(text: str, markers: list[str]) -> bool:
    return any(marker in text for marker in markers)

def is_valid_jd(markdown: str) -> bool:
    if not markdown.strip():
        return False

    # 先排除明显不是招聘 JD 的网页内容
    if has_any_marker(markdown, EXCLUSION_MARKERS):
        return False

    has_duty = has_any_marker(markdown, DUTY_MARKERS)
    has_requirement = has_any_marker(markdown, REQUIREMENT_MARKERS)

    # 真正收录的最低标准：同时有职责和任职要求
    return has_duty and has_requirement
