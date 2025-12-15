import os
from dotenv import load_dotenv

load_dotenv()  # 自动加载 .env

class Settings:
    ITAD_API_KEY: str = os.getenv("IsThereAnyDeal_API_KEY", "")
    STEAM_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")

settings = Settings()
