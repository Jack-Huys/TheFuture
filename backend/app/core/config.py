import os
from dotenv import load_dotenv

load_dotenv()

# MiniMax API配置
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "your-api-key-here")
MINIMAX_BASE_URL = os.getenv("MINIMAX_BASE_URL", "https://api.minimax.chat/v")
MODEL_NAME = os.getenv("MODEL_NAME", "abab6.5s-chat")

# AI SDK类型: "anthropic" 或 "openai"
AI_SDK_TYPE = os.getenv("AI_SDK_TYPE", "openai")

# 服务配置
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# CORS配置
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "*"  # 开发环境，生产环境应限制具体域名
]

# Skill文件路径（相对路径，从backend目录）
# 目录结构: backend/zhangxuefeng-skill/SKILL.md
# config.py -> core -> app -> backend
_config_dir = os.path.dirname(os.path.abspath(__file__))    # app/core
_app_dir = os.path.dirname(_config_dir)                    # app
_backend_dir = os.path.dirname(_app_dir)                   # backend
SKILL_FILE_PATH = os.path.join(_backend_dir, "zhangxuefeng-skill", "SKILL.md")
