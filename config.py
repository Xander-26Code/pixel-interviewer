# config.py —— 专门放共用的东西
import os
from dotenv import load_dotenv
from firecrawl import Firecrawl
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))