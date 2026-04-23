from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import CORS_ORIGINS
from app.api.chat import router as chat_router

app = FastAPI(
    title="未来 - 张雪峰视角高考咨询API",
    version="1.0.0",
    description="基于张雪峰skill的高考志愿咨询服务"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(chat_router)


@app.get("/")
async def root():
    return {"message": "未来 API 服务", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    from app.core.config import HOST, PORT

    uvicorn.run(app, host=HOST, port=PORT)
