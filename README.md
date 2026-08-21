# 像素面试官 · AI 拷打模拟器

> 一个用大模型扮演「真面试官」的 AI 应用：上传简历 → 联网检索目标岗位 JD → RAG 定制提问 → 多轮「拷打式」追问 → 多维评分 + 段位称号。

不只是「温柔问答机器人」——它会像真实面试官一样，专挑你简历里**模糊、包装、没量化**的地方，追着你往死里问。答不上来？它判断出这个点你确实不会，就果断换下一个拷打点，绝不在一处死磕。

---

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| 📄 简历找茬 | 上传 PDF，AI 分析出技术栈、项目经历、以及所有「可拷打的点」 |
| 🎭 多轮拷打 | 面试官基于找茬结果逐条追问，能接住上下文，也能判断何时该换话题 |
| 📊 多维评分 | 技术深度 / 项目真实性 / 表达能力 / 临场反应，每个分数都带「依据」 |
| 🌐 联网 JD-RAG | 输入目标岗位后，通过 Firecrawl 搜索公开 JD，筛选、切块、向量检索后，让面试问题贴近岗位要求 |
| 🏆 段位称号 | 游戏结算式评级：人上人 / 大佬 / 夯 / 及格 / 有点悬 / 拉完了 |
| 🕹️ 像素风 UI | 复古街机像素风，等待回答时像素小人会「翻简历、冒泡思考、嘴巴开合」 |

---

## 🖼️ 界面展示

**面试对话界面**：

![面试界面](assets/interview.png)

**面试复盘报告**（段位称号 + 多维评分卡）：

![评分报告](assets/report.png)

---

## 🛠️ 技术栈

- **后端**：Python + FastAPI + Uvicorn
- **大模型**：DeepSeek（OpenAI 兼容接口，`deepseek-chat` 系列）
- **联网检索**：Firecrawl Search（搜索公开岗位 JD 并返回 Markdown）
- **RAG 检索**：SentenceTransformers + `BAAI/bge-small-zh-v1.5`（本地向量化与余弦相似度检索）
- **PDF 解析**：pypdf
- **前端**：原生 HTML + CSS + JS（像素风，无框架，由 FastAPI 静态托管）

---

## 📁 项目结构

```
.
├── main.py                  # 入口：注册路由 + 挂载静态页面
├── config.py                # DeepSeek / Firecrawl client（读环境变量）
├── job_search.py            # Firecrawl 搜索与 JD 质量筛选（/search）
├── rag_test.py              # 文本切块、Embedding 与相似度检索（/rag）
├── evaluate_rag.py          # RAG A/B 评测脚本
├── evaluation_dataset.json  # 岗位技能评测集
├── requirements.txt         # 依赖清单
├── routers/
│   ├── chat.py              # 对话接口（/chat）
│   ├── resumeAnalyze.py     # 简历分析接口（/analyze）
│   ├── interview.py         # 多轮面试接口（/interview）
│   └── report.py            # 评分报告接口（/report）
├── static/
│   └── index.html           # 像素风前端（单页，含全部 CSS/JS）
└── assets/                  # README 展示图
```

---

## 🚀 部署使用教程

### 第一步：准备环境

需要 **Python 3.13+**（本机已有）。确认版本：

```bash
python3 --version
```

### 第二步：获取 API Keys

需要配置两个 key：

1. **DeepSeek API Key**：打开 [platform.deepseek.com](https://platform.deepseek.com)，注册登录后进入「API Keys」创建 key。
2. **Firecrawl API Key**：注册 [Firecrawl](https://www.firecrawl.dev/) 后，在 Dashboard 创建 API key。Firecrawl 的 Python SDK 使用环境变量 `FIRECRAWL_API_KEY`，key 通常以 `fc-` 开头；可参考 [官方 Python Quickstart](https://docs.firecrawl.dev/quickstarts/python)。

### 第三步：克隆项目并安装依赖

```bash
git clone https://github.com/<你的用户名>/ai-interviewer.git
cd ai-interviewer

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate      # Windows 用 .venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 第四步：配置 API Key

复制 `.env.example` 为 `.env`，填入你的 key：

```bash
cp .env.example .env
```

编辑 `.env`，同时填入两个 key：

```
DEEPSEEK_API_KEY=sk-你的key
FIRECRAWL_API_KEY=fc-你的key
```

> ⚠️ **`.env` 已加入 `.gitignore`，绝不要把真实 key 提交到 GitHub。** 两个 key 都只应存在于本地环境变量文件中。

### 第五步：启动后端

```bash
uvicorn main:app --port 8000 --reload
```

看到这行说明启动成功：

```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

> `--reload` 让改代码后自动重启。**这个终端窗口保持开启，别关。**

### 第六步：打开前端

浏览器地址栏访问：

```
http://localhost:8000
```

> ⚠️ **必须通过 `http://localhost:8000` 访问，不要双击 `index.html` 文件打开！** 否则会报 CORS 错误（`file://` 协议无法请求后端）。

---

## 🎮 使用教程

1. **上传简历并输入目标岗位**：例如“AI 应用开发工程师”。
2. **联网检索 JD**：Firecrawl 搜索公开岗位页面；后端会排除教程、泛职业介绍等噪声内容。
3. **RAG 检索与简历分析**：JD 被切成片段并向量化，命中的岗位要求会作为面试上下文；页面会显示检索状态。
4. **开始面试**：面试官优先依据 JD 和简历提问（每次一个问题）。
5. **回答追问并结束面试**：结束后生成复盘报告。

---

## 📈 RAG 评测结果

项目提供 [`evaluate_rag.py`](evaluate_rag.py) 对同一份简历、同一目标岗位进行 A/B 对照：

- **Baseline**：仅向模型提供岗位名称与简历；
- **JD-RAG**：通过 Firecrawl 搜索并筛选 JD，对 JD 切块、向量化并取 Top-3 片段后再生成面试题；
- 两组均生成 5 道题，并用 [`evaluation_dataset.json`](evaluation_dataset.json) 中预先定义的岗位技能标准评分。

在“AI 应用开发工程师”测试用例上的一次真实运行结果：

| 指标 | 无 RAG | JD-RAG | 含义 |
|------|:---:|:---:|------|
| 检索 Recall@3 | - | 50.0% | Top-3 JD 片段覆盖的岗位标准技能比例 |
| 面试问题技能覆盖率 | 33.3% | 66.7% | 5 道题覆盖的岗位标准技能比例 |
| 岗位专属问题比例 | 20.0% | 40.0% | 明确考察岗位标准技能的问题占比 |
| JD 新增技能覆盖率 | 0.0% | 66.7% | 仅统计“JD 有、简历未明确写”的技能 |

本次 JD-RAG 使面试问题技能覆盖率提升 **33.4 个百分点**，并开始考察简历中未明确出现的 **RAG 工程链路、Embedding 与向量检索、效果评测与优化**。


```bash
python evaluate_rag.py \
  --case ai_application_engineer \
  --resume /path/to/resume.pdf
```

---

## 🔌 API 接口说明

| 方法 | 路径 | 功能 | 请求体 |
|------|------|------|--------|
| POST | `/chat` | 单轮对话 | `{"message": "..."}` |
| POST | `/analyze` | 上传简历 PDF，找茬 | `FormData(file=PDF)` |
| POST | `/search` | 用 Firecrawl 搜索并筛选目标岗位 JD | `{"position": "AI 应用开发工程师"}` |
| POST | `/rag` | 对 JD Markdown 列表执行本地向量检索 | `{"question": "...", "markdowns": [...], "top_k": 3}` |
| POST | `/interview` | 多轮面试（前端带全量历史和 RAG 上下文） | `{"messages": [...], "jd_message": "..."}` |
| POST | `/report` | 评分报告（前端带全量历史） | `{"messages": [...]}` |

**多轮对话的架构**：后端是无状态的——前端（网页）负责保存对话历史，每次请求把「完整历史」传给后端，后端拼上 system prompt 调一次 LLM 返回回复。这就是所有聊天应用（ChatGPT 等）的通用模式。

---

## ❓ 常见问题

**Q：访问报 CORS / `file:///analyze` 错误？**
A：你双击了 HTML 文件。必须通过 `http://localhost:8000` 访问，且后端在跑。

**Q：`Connection refused`？**
A：后端没启动。先跑 `uvicorn main:app --port 8000 --reload`。

**Q：报 `Missing credentials` 或提示没有 Firecrawl API key？**
A：确认项目根目录的 `.env` 同时包含 `DEEPSEEK_API_KEY` 和 `FIRECRAWL_API_KEY`。修改后重启 Uvicorn；不要把 key 写在前端 JavaScript 中。

**Q：联网检索很慢，或者没有找到 JD？**
A：Firecrawl 搜索是外部网络请求，通常比本地向量检索慢。可换一个更具体的岗位名称重试；如果返回的页面大多是教程，继续在 `job_search.py` 的 `EXCLUSION_MARKERS` 中补充噪声特征。

**Q：模型一直揪着一个话题不放？**
A：system prompt 里已有「换话题规则」（同一话题最多追问 2~3 次）。若还想更强，可加大这个约束的措辞。

---

## 🚧 后续规划
- [ ] 面试历史存档 + 多次面试对比
- [x] 联网岗位 JD 检索 + RAG 定制提问
- [x] RAG 多轮 A/B 评测结果汇总
- [ ] 云端一键部署（Zeabur / Railway）

---

## 📄 License

MIT
